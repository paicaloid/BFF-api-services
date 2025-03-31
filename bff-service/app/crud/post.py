import requests
from app.config import settings
from app.crud.user import get_users
from app.schemas import PostCreate, PostPublic, PostUpdate, UserPostsPublic
from fastapi import HTTPException


async def get_posts() -> list[PostPublic]:
    """
    Fetches a list of posts from the post service.
    """
    url = f"{settings.post_url}/posts"
    try:
        response = requests.get(url, headers=settings.header)
        if response.status_code == 200:
            data = response.json()
            return [PostPublic(**post) for post in data]
        else:
            raise HTTPException(
                status_code=response.status_code,
                detail=response.text,
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
    headers.update(settings.header)
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


async def update_post(post_id: int, post_in: PostUpdate) -> None:
    """
    Updates an existing post in the post service.
    """
    url = f"{settings.post_url}/posts/{post_id}"
    headers = {
        "Content-Type": "application/json",
    }
    headers.update(settings.header)
    data = post_in.model_dump()
    try:
        response = requests.put(url, json=data, headers=headers)
        if response.status_code == 200:
            return
        else:
            raise HTTPException(
                status_code=response.status_code,
                detail="Failed to update post",
            )
    except requests.exceptions.RequestException as e:
        raise HTTPException(
            status_code=500,
            detail=f"Request to post service failed: {str(e)}",
        )


async def delete_post(post_id: int) -> None:
    """
    Deletes a post in the post service.
    """
    url = f"{settings.post_url}/posts/{post_id}"
    headers = {
        "Content-Type": "application/json",
    }
    headers.update(settings.header)
    try:
        response = requests.delete(url, headers=headers)
        if response.status_code == 200:
            return
        else:
            raise HTTPException(
                status_code=response.status_code,
                detail="Failed to delete post",
            )
    except requests.exceptions.RequestException as e:
        raise HTTPException(
            status_code=500,
            detail=f"Request to post service failed: {str(e)}",
        )
