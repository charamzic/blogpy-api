from pydantic import BaseModel, Field
from typing import List, TypeVar, Generic

# Define a TypeVar for generic use in PaginatedResponse
T = TypeVar('T')

class ArticleBase(BaseModel):
    """Schema for an article in the list view."""
    id: str = Field(..., description="Unique slug for the article.")
    title: str = Field(..., description="The title of the article.")
    excerpt: str = Field(..., description="A short excerpt of the article content.")
    tags: List[str] = Field(..., description="List of tags associated with the article.")

class ArticleDetail(ArticleBase):
    """Schema for a single article detail, extending ArticleBase with full content."""
    content: str = Field(..., description="The full HTML content of the article body.")

class PaginatedResponse(BaseModel, Generic[T]):
    """Schema for a paginated API response."""
    total_items: int = Field(..., description="Total number of articles matching the filter.")
    total_pages: int = Field(..., description="Total number of pages available.")
    page: int = Field(..., description="The current page number (1-based).")
    per_page: int = Field(..., description="Number of items per page.")
    items: List[T] = Field(..., description="List of articles for the current page.")
