from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import ALLOWED_ORIGINS

from app.routers import articles


app = FastAPI(
    title="Blog Content API",
    description="Service for retrieving blog articles with filtering, pagination, and i18n.",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)

app.include_router(articles.router)

