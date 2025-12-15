from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base


class Page(Base):
    __tablename__ = "pages"

    id = Column(Integer, primary_key=True, index=True)
    page_id = Column(String(100), unique=True, index=True)
    name = Column(String(255))
    url = Column(String(255))
    description = Column(Text)
    industry = Column(String(100))
    followers = Column(Integer)
    headcount = Column(Integer)

    posts = relationship("Post", back_populates="page", cascade="all, delete")
    employees = relationship("Employee", back_populates="page", cascade="all, delete")


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text)
    page_id = Column(Integer, ForeignKey("pages.id"))

    page = relationship("Page", back_populates="posts")
    comments = relationship("Comment", back_populates="post", cascade="all, delete")


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text)
    post_id = Column(Integer, ForeignKey("posts.id"))

    post = relationship("Post", back_populates="comments")


class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    role = Column(String(255))
    page_id = Column(Integer, ForeignKey("pages.id"))

    page = relationship("Page", back_populates="employees")
