# app/cache.py
from typing import Any, Dict, Optional


# Internal cache store
_page_cache: Dict[str, Dict[str, Any]] = {}


async def fetch_page_from_cache(page_id: str) -> Optional[Dict[str, Any]]:
    
    return _page_cache.get(page_id)


async def save_page_to_cache(page_id: str, page_data: Dict[str, Any]) -> None:
    
    _page_cache[page_id] = page_data
