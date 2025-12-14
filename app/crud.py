# app/crud.py
from typing import Optional, Tuple, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, delete
from . import models
from .schemas import PageListItem


async def get_page_by_slug(db: AsyncSession, page_id: str) -> Optional[models.Page]:
    stmt = select(models.Page).where(models.Page.linkedin_page_id == page_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def create_or_update_page_from_scrape(
    db: AsyncSession,
    scraped: dict,
) -> models.Page:
    page_data = scraped["page"]
    posts_data = scraped.get("posts", [])
    followers_data = scraped.get("followers", [])

    # create or update Page
    page = await get_page_by_slug(db, page_data["linkedin_page_id"])
    if not page:
        page = models.Page(**page_data)
        db.add(page)
        await db.flush()
    else:
        for k, v in page_data.items():
            setattr(page, k, v)
        await db.flush()

    # delete existing posts for this page (no lazy relationship access)
    await db.execute(
        delete(models.Post).where(models.Post.page_id == page.id)
    )

    # insert posts
    for p in posts_data:
        post = models.Post(page_id=page.id, **p)
        db.add(post)

    # delete existing followers for this page
    await db.execute(
        delete(models.PageFollower).where(models.PageFollower.page_id == page.id)
    )

    # followers: create users and link
    for f in followers_data:
        stmt = select(models.SocialMediaUser).where(
            models.SocialMediaUser.linkedin_user_id == f["linkedin_user_id"]
        )
        res = await db.execute(stmt)
        user = res.scalar_one_or_none()
        if not user:
            user = models.SocialMediaUser(**f)
            db.add(user)
            await db.flush()
        pf = models.PageFollower(page_id=page.id, user_id=user.id)
        db.add(pf)

    await db.commit()
    await db.refresh(page)
    return page


async def search_pages(
    db: AsyncSession,
    name: Optional[str],
    industry: Optional[str],
    followers_min: Optional[int],
    followers_max: Optional[int],
    page: int,
    limit: int,
) -> Tuple[int, List[PageListItem]]:
    stmt = select(models.Page)
    if name:
        stmt = stmt.where(models.Page.name.ilike(f"%{name}%"))
    if industry:
        stmt = stmt.where(models.Page.industry == industry)
    if followers_min is not None:
        stmt = stmt.where(models.Page.follower_count >= followers_min)
    if followers_max is not None:
        stmt = stmt.where(models.Page.follower_count <= followers_max)

    count_stmt = select(func.count()).select_from(stmt.subquery())
    total = (await db.execute(count_stmt)).scalar_one()

    stmt = stmt.offset((page - 1) * limit).limit(limit)
    res = await db.execute(stmt)
    items = res.scalars().all()

    data = [PageListItem.model_validate(i) for i in items]
    return total, data
