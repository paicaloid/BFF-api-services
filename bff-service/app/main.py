import requests
from app.config import settings
from app.deps import get_current_user
from app.schemas import Token, UserPublic
from fastapi import Depends, FastAPI
from fastapi.exceptions import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer

security = HTTPBearer()

app = FastAPI(
    title="BFF-Service",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/access-token", response_model=Token)
async def get_access_token() -> Token:
    url = f"http://{settings.LOGIN_SERVICE_URL}:{settings.LOGIN_SERVICE_PORT}/access-token"

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


@app.get("/protected", dependencies=[Depends(get_current_user)])
async def protected_route():
    return {"message": "This is a protected route."}


@app.get(
    "/users",
    response_model=list[UserPublic],
)
async def get_users(skip: int = 0, limit: int = 3):
    url = f"http://{settings.USER_SERVICE_URL}:{settings.USER_SERVICE_PORT}/users"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return [UserPublic(**user) for user in data[skip : skip + limit]]
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


@app.get("/posts")
async def get_posts_by_username(username: str):
    url = f"http://{settings.POST_SERVICE_URL}:{settings.POST_SERVICE_PORT}/posts"
    params = {"username": username}
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            return data
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
