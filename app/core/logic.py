import math
from typing import List, Dict, Any

from app.core.data import load_articles
from app.models import PaginatedResponse, ArticleBase
from app.config import PER_PAGE

def get_paginated_articles_data(
    lang: str, 
    tags: List[str], 
    page: int, 
    per_page: int
) -> PaginatedResponse[ArticleBase]:
    """
    Combines article loading, filtering, and pagination logic.
    """
    
    all_articles = load_articles(lang)
    
    if tags:
        # Logic: article must contain AT LEAST ONE of the given tags
        filtered_articles = [a for a in all_articles if set(tags).intersection(a["tags"])]
    else:
        filtered_articles = all_articles

    # Pagination Calculation
    total_items = len(filtered_articles)
    
    # Ensure safe page/per_page values
    per_page = max(1, per_page)
    total_pages = math.ceil(total_items / per_page) if total_items > 0 else 1
    page = max(1, min(page, total_pages))
    
    start = (page - 1) * per_page
    end = start + per_page
    
    paginated_data = filtered_articles[start:end]
    
    # Pydantic validation for the response list
    article_list_for_page = [ArticleBase(**item) for item in paginated_data]

    # Build PaginatedResponse
    return PaginatedResponse[ArticleBase](
        total_items=total_items,
        total_pages=total_pages,
        page=page,
        per_page=per_page,
        items=article_list_for_page
    )
