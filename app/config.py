from dotenv import load_dotenv
import os
from typing import List

load_dotenv()

API_KEY = os.environ.get("ALLOWED_API_KEY")
ENCRYPTION_KEY = os.environ.get("ENCRYPTION_KEY")

if not API_KEY:
    print("WARNING: ALLOWED_API_KEY not set. API endpoints are UNPROTECTED in this environment.")

if not ENCRYPTION_KEY:
    print("FATAL WARNING: ENCRYPTION_KEY not set. Cannot decrypt articles!")


POSTS_DIR = "posts"
DEFAULT_LANG = "cs"
PER_PAGE = 5

ALLOWED_ORIGINS: List[str] = [
    "https://azmarach.work",
]
