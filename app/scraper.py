# app/scraper.py
from datetime import datetime, timedelta
from typing import Any, Dict, List


async def scrape_linkedin_page(page_id: str) -> Dict[str, Any]:
    """
    Dummy scraper.
    Replace with Playwright-based scraping that logs into LinkedIn and extracts real data.
    """
    # Example: synthesize data for demo
    page = {
        "linkedin_page_id": page_id,
        "linkedin_platform_id": "1234567890",
        "name": f"Demo Company {page_id}",
        "url": f"https://www.linkedin.com/company/{page_id}",
        "profile_image_url": "https://example.com/profile.png",
        "description": "Demo company description for testing.",
        "website": "https://example.com",
        "industry": "Software",
        "follower_count": 25000,
        "headcount": 120,
        "specialities": "SaaS,Cloud,AI",
    }

    now = datetime.utcnow()
    posts: List[Dict[str, Any]] = []
    for i in range(1, 6):
        posts.append(
            {
                "linkedin_post_id": f"{page_id}-post-{i}",
                "content_text": f"Demo post {i} for {page_id}",
                "media_url": None,
                "like_count": 10 * i,
                "comment_count": 2 * i,
                "share_count": i,
                "posted_at": now - timedelta(days=i),
            }
        )

    followers: List[Dict[str, Any]] = []
    for i in range(1, 6):
        followers.append(
            {
                "linkedin_user_id": f"user-{i}",
                "name": f"Follower User {i}",
                "headline": "Software Engineer",
            }
        )

    return {
        "page": page,
        "posts": posts,
        "followers": followers,
    }
