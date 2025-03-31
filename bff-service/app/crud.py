import requests
from app.config import settings
from app.schemas import PostCreate, PostPublic, Token, UserPostsPublic, UserPublic
from fastapi import HTTPException


async def get_access_token() -> Token:
    """
    Fetches an access token from the login service.
    """
    url = f"{settings.login_url}/access-token"
    try:
        response = requests.get(url)
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


async def get_users() -> list[UserPublic]:
    """
    Fetches a list of users from the user service.
    """
    url = f"{settings.user_url}/users"
    try:
        response = requests.get(url)
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


async def get_posts() -> list[PostPublic]:
    """
    Fetches a list of posts from the post service.
    """
    url = f"{settings.post_url}/posts"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return [PostPublic(**post) for post in data]
        else:
            raise HTTPException(
                status_code=response.status_code,
                detail="Failed to retrieve posts",
            )
    except requests.exceptions.RequestException as e:
        raise HTTPException(
            status_code=500,
            detail=f"Request to post service failed: {str(e)}",
        )


async def get_posts_by_username(username: str) -> UserPostsPublic:
    """
    Fetches posts by username from the post service.
    """
    users = await get_users()
    user = next((user for user in users if user.username == username), None)
    if not user:
        raise HTTPException(status_code=404, detail="Username not found")

    posts = await get_posts()
    user_posts = [
        PostPublic(**post.model_dump()) for post in posts if post.userId == user.id
    ]

    return UserPostsPublic(
        id=user.id,
        name=user.name,
        username=user.username,
        email=user.email,
        posts=user_posts,
    )


async def create_post(post_in: PostCreate) -> None:
    """
    Creates a new post in the post service.
    """
    users = await get_users()
    user = next((user for user in users if user.id == post_in.userId), None)
    if not user:
        raise HTTPException(status_code=404, detail="User ID not found")

    url = f"{settings.post_url}/posts"
    headers = {
        "Content-Type": "application/json",
    }
    data = post_in.model_dump()
    try:
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 201:
            return
        else:
            raise HTTPException(
                status_code=response.status_code,
                detail="Failed to create post",
            )
    except requests.exceptions.RequestException as e:
        raise HTTPException(
            status_code=500,
            detail=f"Request to post service failed: {str(e)}",
        )
