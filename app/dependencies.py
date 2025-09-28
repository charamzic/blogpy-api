from fastapi import HTTPException, Header, Depends
from app.config import API_KEY
from typing import Optional

async def verify_api_key(x_api_key: Optional[str] = Header(None, alias="X-API-Key")):
    """
    Dependency to verify the presence and correctness of the X-API-Key header.
    
    If API_KEY is set in config (production/dotenv), it must match the header value.
    If API_KEY is None (local unprotected), access is granted.
    """
    
    # If no key is configured, allow access (e.g., in a specific testing environment)
    if API_KEY is None:
        return True
        
    if x_api_key is None or x_api_key != API_KEY:
        raise HTTPException(
            status_code=401, 
            detail="Unauthorized: Invalid or missing API Key"
        )
    return True

# Dependency applied to all secure routers
secure_endpoint = Depends(verify_api_key)
