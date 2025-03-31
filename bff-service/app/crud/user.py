import requests
from app.config import settings
from app.schemas import UserPublic
from fastapi import HTTPException


async def get_users() -> list[UserPublic]:
    """
    Fetches a list of users from the user service.
    """
    url = f"{settings.user_url}/users"
    try:
        response = requests.get(url, headers=settings.header)
        if response.status_code == 200:
            data = response.json()
            return [UserPublic(**user) for user in data]
        else:
            raise HTTPException(
                status_code=response.status_code,
                detail="Failed to retrieve users",
            )
    except requests.exceptions.RequestException as e:
        raise HTTPException(
            status_code=500,
            detail=f"Request to user service failed: {str(e)}",
        )
