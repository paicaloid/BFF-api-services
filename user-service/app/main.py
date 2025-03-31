import sqlalchemy
from app.config import settings
from app.db import get_db

# from app.init_data import init_user
from app.models import User
from app.schemas import UserCreate, UserPublic, UserUpdate
from fastapi import Depends, FastAPI, HTTPException, Security, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import APIKeyHeader
from sqlalchemy.orm import Session

# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     # models.Base.metadata.create_all(bind=engine)
#     # init_user()
#     yield
#     # models.Base.metadata.drop_all(bind=engine)

api_key_header = APIKeyHeader(
    name="X-Internal-API-Key",
)


def verify_api_key(api_key: str = Security(api_key_header)):
    if api_key != settings.INTERNAL_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key",
        )


app = FastAPI(
    title="User-Service",
    # lifespan=lifespan,
    dependencies=[Depends(verify_api_key)],
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/users", response_model=list[UserPublic])
async def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users


@app.post("/users", status_code=status.HTTP_201_CREATED)
async def create_user(
    user_in: UserCreate,
    db: Session = Depends(get_db),
) -> None:
    try:
        db_user = User(**user_in.model_dump())
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    except sqlalchemy.exc.IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username/Email already exists",
        )


@app.put("/users/{user_id}", status_code=status.HTTP_200_OK)
async def update_user(
    user_id: int,
    user_in: UserUpdate,
    db: Session = Depends(get_db),
) -> None:
    db_user = db.query(User).filter(User.id == user_id)
    if not db_user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    db_user.update(user_in.model_dump())
    db.commit()


@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
) -> None:
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    db.delete(db_user)
    db.commit()
