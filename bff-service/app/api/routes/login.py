from app import crud
from app.schemas import Token
from fastapi import APIRouter

router = APIRouter()


@router.get("/access-token", response_model=Token)
async def get_access_token() -> Token:
    return await crud.get_access_token()
