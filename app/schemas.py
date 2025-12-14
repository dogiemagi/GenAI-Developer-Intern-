# app/schemas.py
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel


class PostBase(BaseModel):
    linkedin_post_id: str
    content_text: Optional[str] = None
    media_url: Optional[str] = None
    like_count: Optional[int] = None
    comment_count: Optional[int] = None
    share_count: Optional[int] = None
    posted_at: Optional[datetime] = None


class Post(PostBase):
    id: int

    class Config:
        from_attributes = True


class PageBase(BaseModel):
    linkedin_page_id: str
    linkedin_platform_id: Optional[str] = None
    name: str
    url: str
    profile_image_url: Optional[str] = None
    description: Optional[str] = None
    website: Optional[str] = None
    industry: Optional[str] = None
    follower_count: Optional[int] = None
    headcount: Optional[int] = None
    specialities: Optional[str] = None


class Page(PageBase):
    id: int
    posts: List[Post] = []

    class Config:
        from_attributes = True


class PageListItem(BaseModel):
    id: int
    linkedin_page_id: str
    name: str
    industry: Optional[str]
    follower_count: Optional[int]

    class Config:
        from_attributes = True


class PaginatedPages(BaseModel):
    total: int
    page: int
    limit: int
    items: List[PageListItem]


class FollowerUser(BaseModel):
    id: int
    linkedin_user_id: str
    name: str
    headline: Optional[str] = None

    class Config:
        from_attributes = True
