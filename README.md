# Blog Content API (FastAPI)

This project serves as a secure, fast, and scalable content API for a blog. It is built using FastAPI and leverages Markdown files with YAML front-matter as the source of truth for all content.

## Features

* **Content Management:** Articles are loaded dynamically from the `/posts` directory.
* **Internationalization (i18n):** Supports multiple languages based on file extensions (e.g., `article.cs.md`, `article.en.md`).
* **Filtering & Pagination:** Supports filtering by tags and pagination of the article list.
* **Secure Access:** All API endpoints are protected by an `X-API-Key` header for backend-to-backend communication.
* **Automatic Documentation:** Interactive API documentation (Swagger UI) is available at `/docs`.

## Project Structure

The project follows a modular structure for maintainability:

| Directory/File | Description |
| :--- | :--- |
| `main.py` | The application entry point and main FastAPI instance registration. |
| `app/config.py` | Central configuration for API settings, CORS, and loading environment variables. |
| `app/models.py` | Pydantic schemas for defining JSON response structure. |
| `app/dependencies.py` | Dependency Injection functions (e.g., API key verification). |
| `app/core/data.py` | Core logic for reading, parsing, and converting Markdown files to HTML. |
| `app/core/logic.py` | Logic for filtering and paginating the retrieved article data. |
| `app/routers/articles.py` | All secure API endpoints (`/articles`, `/tags`). |
| `posts/` | Directory containing all blog posts as Markdown files. |

## Setup and Running

1.  **Clone the repository:**
    ```bash
    git clone <your-repo-url>
    cd blogpy
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure API Key:**
    Create a file named **`.env`** in the project root and set your secret key:
    ```dotenv
    ALLOWED_API_KEY=your_super_secret_key_here
    ENCRYPTION_KEY=your_encryption_key
    ```

4.  **Run the server:**
    ```bash
    uvicorn main:app --reload
    ```

The API will be accessible at `http://127.0.0.1:8000`.

## Testing the API

Access the interactive documentation to test the endpoints: `http://127.0.0.1:8000/docs`

Remember to set the `X-API-Key` header when testing the protected endpoints.

## Encryption workflow

All article files in the `/posts` directory are **encrypted** using the Fernet standard (`cryptography`) and are stored on GitHub as unreadable binary data. They can only be decrypted on the server using a secret key. You can read all articles on the main website at **https://azmarach.work/blog** when connected.

Initial encryption for all files in `posts/`
```bash
    python content_manager.py encrypt --all
```
Note: The encrypt --all command safely skips files that are already encrypted, preventing accidental double-encryption.

Decrypt if you want to edit the article
```bash
    python content_manager.py decrypt prvni-clanek.cs.md
```

Encrypt again after edit
```bash
    python content_manager.py encrypt prvni-clanek.cs.md
```
