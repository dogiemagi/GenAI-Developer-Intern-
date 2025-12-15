from pydantic import BaseModel
from typing import List


class CommentOut(BaseModel):
    text: str

    class Config:
        orm_mode = True


class PostOut(BaseModel):
    content: str
    comments: List[CommentOut]

    class Config:
        orm_mode = True


class EmployeeOut(BaseModel):
    name: str
    role: str

    class Config:
        orm_mode = True


class PageOut(BaseModel):
    page_id: str
    name: str
    description: str
    industry: str
    followers: int
    headcount: int
    posts: List[PostOut]
    employees: List[EmployeeOut]

    class Config:
        orm_mode = True
