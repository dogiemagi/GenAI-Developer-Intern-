# app/cache.py
from typing import Any, Optional

# Simple in-memory cache for development (no Redis required)
_cache: dict[str, dict[str, Any]] = {}


async def get_cached_page(page_id: str) -> Optional[dict[str, Any]]:
    """
    Get cached data for a page_id.
    Returns the stored dict or None if not present.
    """
    return _cache.get(page_id)


async def set_cached_page(page_id: str, value: dict[str, Any]):
    """
    Store page data for a page_id in the in-memory cache.
    """
    _cache[page_id] = value
