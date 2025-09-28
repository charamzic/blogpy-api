import os
import markdown
import yaml
from bs4 import BeautifulSoup
from typing import List, Dict, Any

from app.config import POSTS_DIR

def generate_excerpt(html_content: str, max_chars: int = 150) -> str:
    """Creates a safe text excerpt from HTML content."""
    soup = BeautifulSoup(html_content, "html.parser")
    text = soup.get_text()
    if len(text) > max_chars:
        return text[:max_chars].rstrip() + "…"
    return text

def get_all_tags(articles: List[Dict[str, Any]]) -> List[str]:
    """Returns a sorted list of all unique tags from the provided articles."""
    tags = set()
    for a in articles:
        tags.update(a.get("tags", []))
    return sorted(tags)

def load_articles(lang: str = "en") -> List[Dict[str, Any]]:
    """
    Loads all articles for a given language from the posts directory.
    Converts markdown content to HTML and extracts metadata.
    """
    articles = []
    # Filter files by language extension
    files = [f for f in os.listdir(POSTS_DIR) if f.endswith(f".{lang}.md")]
    
    for f in files:
        path = os.path.join(POSTS_DIR, f)
        with open(path, "r", encoding="utf-8") as file:
            content = file.read()
            
            # Split front-matter and content
            meta = {}
            md_content = content
            if content.startswith("---"):
                parts = content.split("---", 2)
                # Use safe_load to prevent arbitrary code execution
                meta = yaml.safe_load(parts[1]) or {}
                md_content = parts[2].strip()
            
            # Convert Markdown to HTML
            html_content = markdown.markdown(md_content)
            excerpt = generate_excerpt(html_content, max_chars=150)
            # Use file name without extension as slug/ID
            slug = f.split(f".{lang}.md")[0]
            
            articles.append({
                "id": slug,
                "title": meta.get("title", slug),
                "tags": meta.get("tags", []),
                "content": html_content,
                "excerpt": excerpt
            })
            
    return articles
