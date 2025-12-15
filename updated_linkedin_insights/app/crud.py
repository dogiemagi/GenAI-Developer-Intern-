from sqlalchemy.orm import Session
from .models import Page, Post, Comment, Employee


def get_page_by_page_id(db: Session, page_id: str):
    return db.query(Page).filter(Page.page_id == page_id).first()


def create_page(db: Session, data: dict):
    page = Page(
        page_id=data["page_id"],
        name=data["name"],
        url=data["url"],
        description=data["description"],
        industry=data["industry"],
        followers=data["followers"],
        headcount=data["headcount"]
    )

    db.add(page)
    db.commit()
    db.refresh(page)

    for post_data in data["posts"]:
        post = Post(content=post_data["content"], page=page)
        db.add(post)
        db.commit()

        for c in post_data["comments"]:
            comment = Comment(text=c["text"], post=post)
            db.add(comment)

    for emp in data["employees"]:
        employee = Employee(
            name=emp["name"],
            role=emp["role"],
            page=page
        )
        db.add(employee)

    db.commit()
    return page
