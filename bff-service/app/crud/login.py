import requests
from app.config import settings
from app.schemas import Token
from fastapi import HTTPException


async def get_access_token() -> Token:
    """
    Fetches an access token from the login service.
    """
    url = f"{settings.login_url}/access-token"
    try:
        response = requests.get(url, headers=settings.header)
        if response.status_code == 200:
            data = response.json()
            return Token(
                access_token=data["access_token"],
                token_type=data["token_type"],
            )
        else:
            raise HTTPException(
                status_code=response.status_code,
                detail="Failed to retrieve access token",
            )
    except requests.exceptions.RequestException as e:
        raise HTTPException(
            status_code=500,
            detail=f"Request to login service failed: {str(e)}",
        )
