import os
import markdown
import yaml
from cryptography.fernet import Fernet
from app.config import POSTS_DIR, ENCRYPTION_KEY
from bs4 import BeautifulSoup
from typing import List, Dict, Any

from app.config import POSTS_DIR


try:
    FERNET_CRYPTO = Fernet(ENCRYPTION_KEY.encode('utf-8'))
except Exception as e:
    print(f"ERROR: Failed to initialize Fernet. Check ENCRYPTION_KEY: {e}")
    FERNET_CRYPTO = None


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

def load_articles(lang: str = "en") -> List[Dict]:
    """
    Loads all articles for a given language, decrypts them, 
    converts markdown content to HTML and extracts metadata.
    """
    
    if FERNET_CRYPTO is None:
        print("Decryption is disabled or failed to initialize.")
        return []

    articles = []
    files = [f for f in os.listdir(POSTS_DIR) if f.endswith(f".{lang}.md")]
    
    for f in files:
        path = os.path.join(POSTS_DIR, f)
        with open(path, "rb") as file:
            encrypted_data = file.read()
            
            try:
                decrypted_content_bytes = FERNET_CRYPTO.decrypt(encrypted_data)
                
                content = decrypted_content_bytes.decode("utf-8")
                
            except Exception as e:
                print(f"Skipping article {f}: Decryption failed. Error: {e}")
                continue
            
            meta = {}
            md_content = content
            if content.startswith("---"):
                parts = content.split("---", 2)
                meta = yaml.safe_load(parts[1]) or {}
                md_content = parts[2].strip()

            html_content = markdown.markdown(md_content)
            excerpt = generate_excerpt(html_content, max_chars=150)
            slug = f.split(f".{lang}.md")[0]
            
            articles.append({
                "id": slug,
                "title": meta.get("title", slug),
                "tags": meta.get("tags", []),
                "content": html_content,
                "excerpt": excerpt
            })
            
    return articles
