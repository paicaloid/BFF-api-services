from app import crud
from app.deps import get_current_user
from app.schemas import UserCreate, UserPublic, UserUpdate
from fastapi import APIRouter, Depends, status

router = APIRouter(dependencies=[Depends(get_current_user)])


@router.get(
    "",
    response_model=list[UserPublic],
)
async def get_users(
    skip: int = 0,
    limit: int = 3,
) -> list[UserPublic]:
    res = await crud.get_users()
    return res[skip : skip + limit]


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
)
async def create_user(
    user_in: UserCreate,
) -> None:
    """
    Create a new user.
    """
    await crud.create_user(user_in)


@router.put(
    "/{user_id}",
    status_code=status.HTTP_200_OK,
)
async def update_user(
    user_id: int,
    user_in: UserUpdate,
) -> None:
    """
    Update an existing user.
    """
    await crud.update_user(user_in=user_in, user_id=user_id)


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_user(
    user_id: int,
) -> None:
    """
    Delete a user.
    """
    await crud.delete_user(user_id=user_id)
