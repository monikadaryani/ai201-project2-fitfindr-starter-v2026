"""
Semantic search for FitFindr. ← CAPSTONE

Keyword search (tools.py) only finds a listing that shares an exact word with
the query. This ranks listings by embedding similarity instead, so a query can
match on meaning: "band shirt" can find a listing written as "graphic tee".

    rank(description, listings)  → [(score, listing), ...] best first

Listing vectors are embedded once and cached to disk. The cache is keyed on the
model, the vector size and the listing text, so editing a listing or changing
the model recomputes it instead of serving stale vectors. The query is embedded
fresh on every call.
"""

import hashlib
import json
import math

import config
from generate import embed

_CACHE_FILE = config.CACHE_DIR / "listing_embeddings.json"


def listing_text(listing: dict) -> str:
    """The text a listing is searched on. Shared by both strategies."""
    return " ".join([
        listing.get("title", ""),
        listing.get("description", ""),
        " ".join(listing.get("style_tags", [])),
        " ".join(listing.get("colors", [])),
        listing.get("category", ""),
    ])


def _normalize(vector: list[float]) -> list[float]:
    # Reduced-size vectors from the embedding model are not unit length, so
    # normalize here; cosine similarity is then a plain dot product.
    norm = math.sqrt(sum(v * v for v in vector)) or 1.0
    return [v / norm for v in vector]


def _fingerprint(listing: dict) -> str:
    key = f"{config.EMBEDDING_MODEL}|{config.EMBEDDING_DIMENSIONS}|{listing_text(listing)}"
    return hashlib.sha256(key.encode("utf-8")).hexdigest()


def _load_cache() -> dict:
    try:
        return json.loads(_CACHE_FILE.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def listing_vectors(listings: list[dict]) -> dict[str, list[float]]:
    """
    Unit vectors for these listings, keyed by listing id.

    Embeds only the listings that aren't cached yet, in one call, and writes
    them back to the cache.
    """
    cache = _load_cache()
    missing = [l for l in listings if _fingerprint(l) not in cache]
    if missing:
        vectors = embed([listing_text(l) for l in missing], "RETRIEVAL_DOCUMENT")
        for listing, vector in zip(missing, vectors):
            cache[_fingerprint(listing)] = _normalize(vector)
        config.CACHE_DIR.mkdir(exist_ok=True)
        _CACHE_FILE.write_text(json.dumps(cache), encoding="utf-8")
    return {l["id"]: cache[_fingerprint(l)] for l in listings}


def rank(description: str, listings: list[dict]) -> list[tuple[float, dict]]:
    """
    Score every listing by cosine similarity to the description, best first.

    Does not apply SEMANTIC_MIN_SCORE or the result limit — search_listings
    does, so it can treat both strategies the same way.
    """
    if not description.strip() or not listings:
        return []
    vectors = listing_vectors(listings)
    query = _normalize(embed([description], "RETRIEVAL_QUERY")[0])
    scored = [
        (sum(q * v for q, v in zip(query, vectors[l["id"]])), l)
        for l in listings
    ]
    scored.sort(key=lambda item: (-item[0], item[1].get("price", 0)))
    return scored
