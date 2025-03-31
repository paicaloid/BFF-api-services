from app import crud
from app.deps import get_current_user
from app.schemas import PostCreate, UserPostsPublic
from fastapi import APIRouter, Depends, status

router = APIRouter(dependencies=[Depends(get_current_user)])


@router.get("/", response_model=UserPostsPublic)
async def get_posts_by_username(username: str) -> UserPostsPublic:
    res = await crud.get_posts_by_username(username=username)
    return res


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_post(post_in: PostCreate):
    await crud.create_post(post_in=post_in)
