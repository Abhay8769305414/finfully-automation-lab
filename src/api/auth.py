import os
import logging
from fastapi import Security, HTTPException, status
from fastapi.security import APIKeyHeader
from src.config import Config

logger = logging.getLogger(__name__)

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

def verify_api_token(api_key_header: str = Security(api_key_header)):
    """Verify Bearer token or X-API-Key header against Config.API_AUTH_TOKEN."""
    expected_token = Config.API_AUTH_TOKEN
    if not expected_token:
        return True
    
    if api_key_header == expected_token:
        return True
        
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or missing API authentication token.",
    )
