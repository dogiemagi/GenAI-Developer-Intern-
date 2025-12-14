# app/models.py
from sqlalchemy import (
    Column,
    String,
    Integer,
    Text,
    DateTime,
    ForeignKey,
    BigInteger,
    func,
)
from sqlalchemy.orm import relationship
from .database import Base


class Page(Base):
    __tablename__ = "pages"

    id = Column(Integer, primary_key=True, index=True)
    linkedin_page_id = Column(String(255), unique=True, index=True, nullable=False)
    linkedin_platform_id = Column(String(255), nullable=True)
    name = Column(String(255), nullable=False)
    url = Column(String(512), nullable=False)
    profile_image_url = Column(String(512), nullable=True)
    description = Column(Text, nullable=True)
    website = Column(String(512), nullable=True)
    industry = Column(String(255), nullable=True)
    follower_count = Column(Integer, nullable=True)
    headcount = Column(Integer, nullable=True)
    specialities = Column(Text, nullable=True)  # comma separated for simplicity
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    posts = relationship("Post", back_populates="page", cascade="all, delete-orphan")
    employments = relationship(
        "Employment", back_populates="page", cascade="all, delete-orphan"
    )
    followers = relationship(
        "PageFollower", back_populates="page", cascade="all, delete-orphan"
    )


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    page_id = Column(Integer, ForeignKey("pages.id", ondelete="CASCADE"), nullable=False)
    linkedin_post_id = Column(String(255), index=True, nullable=False)
    content_text = Column(Text, nullable=True)
    media_url = Column(String(512), nullable=True)
    like_count = Column(Integer, nullable=True)
    comment_count = Column(Integer, nullable=True)
    share_count = Column(Integer, nullable=True)
    posted_at = Column(DateTime(timezone=True), nullable=True)

    page = relationship("Page", back_populates="posts")
    comments = relationship(
        "Comment", back_populates="post", cascade="all, delete-orphan"
    )


class SocialMediaUser(Base):
    __tablename__ = "social_media_users"

    id = Column(Integer, primary_key=True, index=True)
    linkedin_user_id = Column(String(255), unique=True, index=True, nullable=False)
    name = Column(String(255), nullable=False)
    headline = Column(String(512), nullable=True)
    profile_url = Column(String(512), nullable=True)
    profile_image_url = Column(String(512), nullable=True)

    employments = relationship(
        "Employment", back_populates="user", cascade="all, delete-orphan"
    )
    comments = relationship(
        "Comment", back_populates="user", cascade="all, delete-orphan"
    )
    followed_pages = relationship(
        "PageFollower", back_populates="user", cascade="all, delete-orphan"
    )


class Employment(Base):
    __tablename__ = "employments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(
        Integer, ForeignKey("social_media_users.id", ondelete="CASCADE"), nullable=False
    )
    page_id = Column(Integer, ForeignKey("pages.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(255), nullable=True)
    location = Column(String(255), nullable=True)

    user = relationship("SocialMediaUser", back_populates="employments")
    page = relationship("Page", back_populates="employments")


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(
        Integer, ForeignKey("social_media_users.id", ondelete="CASCADE"), nullable=False
    )
    content_text = Column(Text, nullable=True)
    like_count = Column(Integer, nullable=True)

    post = relationship("Post", back_populates="comments")
    user = relationship("SocialMediaUser", back_populates="comments")


class PageFollower(Base):
    __tablename__ = "page_followers"

    id = Column(Integer, primary_key=True, index=True)
    page_id = Column(Integer, ForeignKey("pages.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(
        Integer, ForeignKey("social_media_users.id", ondelete="CASCADE"), nullable=False
    )

    page = relationship("Page", back_populates="followers")
    user = relationship("SocialMediaUser", back_populates="followed_pages")
