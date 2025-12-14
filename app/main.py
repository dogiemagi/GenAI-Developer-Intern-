# app/main.py
from typing import List, Optional
from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from .database import init_db
from .deps import get_db
from . import crud, schemas
from .scraper import scrape_linkedin_page
from .cache import get_cached_page, set_cached_page
from .config import settings
from .models import Page, Post, SocialMediaUser, PageFollower

app = FastAPI(title="LinkedIn Insights Service")


@app.on_event("startup")
async def on_startup():
    await init_db()


@app.post("/pages/{page_id}/sync", response_model=schemas.Page)
async def sync_page(
    page_id: str,
    db: AsyncSession = Depends(get_db),
):
    # scrape + save to DB
    scraped = await scrape_linkedin_page(page_id)
    page = await crud.create_or_update_page_from_scrape(db, scraped)

    # explicitly load posts (avoid accessing page.posts lazily)
    stmt = (
        select(Post)
        .where(Post.page_id == page.id)
        .order_by(Post.posted_at.desc().nullslast())
    )
    res = await db.execute(stmt)
    posts = res.scalars().all()

    page_schema = schemas.Page(
        id=page.id,
        linkedin_page_id=page.linkedin_page_id,
        linkedin_platform_id=page.linkedin_platform_id,
        name=page.name,
        url=page.url,
        profile_image_url=page.profile_image_url,
        description=page.description,
        website=page.website,
        industry=page.industry,
        follower_count=page.follower_count,
        headcount=page.headcount,
        specialities=page.specialities,
        posts=[schemas.Post.model_validate(p) for p in posts],
    )

    data = page_schema.model_dump()
    await set_cached_page(page_id, data)
    return data


@app.get("/pages/{page_id}", response_model=schemas.Page)
async def get_page(
    page_id: str,
    db: AsyncSession = Depends(get_db),
):
    # check cache first
    cached = await get_cached_page(page_id)
    if cached:
        return cached

    page = await crud.get_page_by_slug(db, page_id)
    if not page:
        scraped = await scrape_linkedin_page(page_id)
        page = await crud.create_or_update_page_from_scrape(db, scraped)

    # explicitly load posts
    stmt = (
        select(Post)
        .where(Post.page_id == page.id)
        .order_by(Post.posted_at.desc().nullslast())
    )
    res = await db.execute(stmt)
    posts = res.scalars().all()

    page_schema = schemas.Page(
        id=page.id,
        linkedin_page_id=page.linkedin_page_id,
        linkedin_platform_id=page.linkedin_platform_id,
        name=page.name,
        url=page.url,
        profile_image_url=page.profile_image_url,
        description=page.description,
        website=page.website,
        industry=page.industry,
        follower_count=page.follower_count,
        headcount=page.headcount,
        specialities=page.specialities,
        posts=[schemas.Post.model_validate(p) for p in posts],
    )

    data = page_schema.model_dump()
    await set_cached_page(page_id, data)
    return data


@app.get("/pages", response_model=schemas.PaginatedPages)
async def list_pages(
    name: Optional[str] = Query(default=None),
    industry: Optional[str] = Query(default=None),
    followers_min: Optional[int] = Query(default=None, alias="followersMin"),
    followers_max: Optional[int] = Query(default=None, alias="followersMax"),
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=10, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    total, items = await crud.search_pages(
        db, name, industry, followers_min, followers_max, page, limit
    )
    return {
        "total": total,
        "page": page,
        "limit": limit,
        "items": items,
    }


@app.get("/pages/{page_id}/posts", response_model=List[schemas.Post])
async def get_page_posts(
    page_id: str,
    limit: int = Query(default=10, ge=1, le=50),
    db: AsyncSession = Depends(get_db),
):
    stmt_page = select(Page).where(Page.linkedin_page_id == page_id)
    res_page = await db.execute(stmt_page)
    page = res_page.scalar_one_or_none()
    if not page:
        raise HTTPException(status_code=404, detail="Page not found")

    stmt = (
        select(Post)
        .where(Post.page_id == page.id)
        .order_by(Post.posted_at.desc().nullslast())
        .limit(limit)
    )
    res = await db.execute(stmt)
    posts = res.scalars().all()
    return [schemas.Post.model_validate(p) for p in posts]


@app.get("/pages/{page_id}/followers", response_model=List[schemas.FollowerUser])
async def get_page_followers(
    page_id: str,
    limit: int = Query(default=20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    stmt_page = select(Page).where(Page.linkedin_page_id == page_id)
    res_page = await db.execute(stmt_page)
    page = res_page.scalar_one_or_none()
    if not page:
        raise HTTPException(status_code=404, detail="Page not found")

    stmt = (
        select(SocialMediaUser)
        .join(PageFollower, PageFollower.user_id == SocialMediaUser.id)
        .where(PageFollower.page_id == page.id)
        .limit(limit)
    )
    res = await db.execute(stmt)
    users = res.scalars().all()
    return [schemas.FollowerUser.model_validate(u) for u in users]
