import requests
from app.config import settings
from app.schemas import UserCreate, UserPublic, UserUpdate
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


async def create_user(user_in: UserCreate) -> None:
    """
    Creates a new user in the user service.
    """
    url = f"{settings.user_url}/users"
    try:
        response = requests.post(
            url, json=user_in.model_dump(), headers=settings.header
        )
        if response.status_code == 201:
            return
        else:
            raise HTTPException(
                status_code=response.status_code,
                detail=response.text,
            )
    except requests.exceptions.RequestException as e:
        raise HTTPException(
            status_code=500,
            detail=f"Request to user service failed: {str(e)}",
        )


async def update_user(user_in: UserUpdate, user_id: int) -> None:
    """
    Updates an existing user in the user service.
    """
    url = f"{settings.user_url}/users/{user_id}"
    try:
        response = requests.put(url, json=user_in.model_dump(), headers=settings.header)
        if response.status_code == 200:
            return
        else:
            raise HTTPException(
                status_code=response.status_code,
                detail=response.text,
            )
    except requests.exceptions.RequestException as e:
        raise HTTPException(
            status_code=500,
            detail=f"Request to user service failed: {str(e)}",
        )


async def delete_user(user_id: int) -> None:
    """
    Deletes a user from the user service.
    """
    url = f"{settings.user_url}/users/{user_id}"
    try:
        response = requests.delete(url, headers=settings.header)
        if response.status_code == 204:
            return
        else:
            raise HTTPException(
                status_code=response.status_code,
                detail=response.text,
            )
    except requests.exceptions.RequestException as e:
        raise HTTPException(
            status_code=500,
            detail=f"Request to user service failed: {str(e)}",
        )
