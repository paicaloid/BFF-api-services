from app.api.routes import login, post, user
from fastapi import APIRouter

api_router = APIRouter()

api_router.include_router(login.router, prefix="/login", tags=["login"])
api_router.include_router(user.router, prefix="/users", tags=["users"])
api_router.include_router(post.router, prefix="/posts", tags=["posts"])
