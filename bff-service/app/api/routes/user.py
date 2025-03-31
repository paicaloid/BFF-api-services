from app import crud
from app.deps import get_current_user
from app.schemas import UserPublic
from fastapi import APIRouter, Depends

router = APIRouter(dependencies=[Depends(get_current_user)])


@router.get(
    "/",
    response_model=list[UserPublic],
)
async def get_users(
    skip: int = 0,
    limit: int = 3,
) -> list[UserPublic]:
    res = await crud.get_users()
    return res[skip : skip + limit]
