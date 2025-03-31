from app import crud
from app.deps import get_current_user
from app.schemas import PostCreate, PostPublic, PostUpdate, UserPostsPublic
from fastapi import APIRouter, Depends, status

router = APIRouter(dependencies=[Depends(get_current_user)])


@router.get("/by-user", response_model=UserPostsPublic)
async def get_posts_by_username(username: str) -> UserPostsPublic:
    res = await crud.get_posts_by_username(username=username)
    return res


@router.get("", response_model=list[PostPublic])
async def get_posts(
    skip: int = 0,
    limit: int = 3,
) -> list[PostPublic]:
    res = await crud.get_posts()
    return res[skip : skip + limit]


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_post(post_in: PostCreate):
    await crud.create_post(post_in=post_in)


@router.put("/{post_id}", status_code=status.HTTP_200_OK)
async def update_post(post_id: int, post_in: PostUpdate):
    await crud.update_post(post_id=post_id, post_in=post_in)


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(post_id: int):
    await crud.delete_post(post_id=post_id)
