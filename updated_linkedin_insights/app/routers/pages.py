from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.schemas import PageOut
from app import crud, scraper
from app.models import Page
from app.utils import paginate

router = APIRouter(prefix="/pages", tags=["Pages"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/{page_id}", response_model=PageOut)
def get_page(page_id: str, db: Session = Depends(get_db)):
    page = crud.get_page_by_page_id(db, page_id)
    if not page:
        data = scraper.scrape_linkedin_page(page_id)
        page = crud.create_page(db, data)
    return page


@router.get("/", response_model=list[PageOut])
def filter_pages(
    industry: str | None = None,
    min_followers: int = 0,
    max_followers: int = 1_000_000,
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    q = db.query(Page).filter(
        Page.followers.between(min_followers, max_followers)
    )

    if industry:
        q = q.filter(Page.industry.ilike(f"%{industry}%"))

    offset, limit = paginate(page, limit)
    return q.offset(offset).limit(limit).all()
