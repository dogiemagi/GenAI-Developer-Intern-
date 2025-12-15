from fastapi import FastAPI
from app.database import Base, engine
from app.routers.pages import router as pages_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="LinkedIn Insights Microservice")

app.include_router(pages_router)
