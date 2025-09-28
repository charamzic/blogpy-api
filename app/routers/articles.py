from fastapi import APIRouter, Query, HTTPException
from typing import List, Optional

from app.core.data import load_articles, get_all_tags
from app.core.logic import get_paginated_articles_data
from app.models import PaginatedResponse, ArticleBase, ArticleDetail
from app.dependencies import secure_endpoint
from app.config import DEFAULT_LANG, PER_PAGE

# Initialize the API router
router = APIRouter(
    prefix="/api/v1",
    tags=["articles"],
    dependencies=[secure_endpoint] # Apply API Key protection to all routes in this router
)


@router.get(
    "/articles",
    response_model=PaginatedResponse[ArticleBase],
    summary="List all articles with filtering and pagination"
)
def list_articles(
    lang: str = Query(DEFAULT_LANG, description="Language of the articles ('cs', 'en', etc.)."),
    # tags will automatically be parsed as List[str] from query parameters (&tags=tag1&tags=tag2)
    tags: Optional[List[str]] = Query(None, description="Filter articles by a list of tags. Articles containing ANY of these tags will be returned."),
    page: int = Query(1, ge=1, description="Page number."),
    per_page: int = Query(PER_PAGE, ge=1, le=100, description="Number of articles per page.")
):
    """
    Returns a paginated list of articles in JSON format, filtered by language and tags.
    """
    return get_paginated_articles_data(lang, tags or [], page, per_page)


@router.get(
    "/articles/{slug}",
    response_model=ArticleDetail,
    summary="Get a single article by slug"
)
def get_article_detail(
    slug: str,
    lang: str = Query(DEFAULT_LANG, description="Language of the article.")
):
    """
    Returns the detail of a single article (including full HTML content) in JSON format.
    """
    all_articles = load_articles(lang)
    # Find the article detail by slug
    article_data = next((a for a in all_articles if a["id"] == slug), None)
    
    if not article_data:
        raise HTTPException(status_code=404, detail="Article not found")

    # Pydantic validation and return using ArticleDetail model
    return ArticleDetail(**article_data)


@router.get(
    "/tags",
    response_model=List[str],
    summary="Get all unique tags"
)
def get_tags(
    lang: str = Query(DEFAULT_LANG, description="Language for which to list tags.")
):
    """Returns a list of all unique tags for the given language."""
    articles = load_articles(lang)
    return get_all_tags(articles)
