from contextlib import asynccontextmanager

from app import models
from app.db import engine, get_db
from app.init_data import init_user
from app.models import User
from app.schemas import UserPublic
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session


@asynccontextmanager
async def lifespan(app: FastAPI):
    models.Base.metadata.create_all(bind=engine)
    init_user()
    yield
    # models.Base.metadata.drop_all(bind=engine)


app = FastAPI(
    title="User-Service",
    lifespan=lifespan,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)


@app.get("/users", response_model=list[UserPublic])
async def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users
