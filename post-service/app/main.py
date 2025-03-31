from app import models
from app.config import settings
from app.db import get_db
from app.schemas import PostCreate, PostPublic, PostUpdate
from fastapi import Depends, FastAPI, HTTPException, Security, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import APIKeyHeader
from sqlalchemy.orm import Session

# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     models.Base.metadata.create_all(bind=engine)
#     init_post()
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


@app.get("/posts", response_model=list[PostPublic])
async def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts


@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_post(
    post_in: PostCreate,
    db: Session = Depends(get_db),
) -> None:
    post = models.Post(**post_in.model_dump())
    db.add(post)
    db.commit()
    db.refresh(post)


@app.put("/posts/{post_id}", status_code=status.HTTP_200_OK)
async def update_post(
    post_id: int,
    post_in: PostUpdate,
    db: Session = Depends(get_db),
) -> None:
    post = db.query(models.Post).filter(models.Post.id == post_id)
    if not post.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found",
        )

    post.update(post_in.model_dump())
    db.commit()


@app.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    post_id: int,
    db: Session = Depends(get_db),
) -> None:
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found",
        )

    db.delete(post)
    db.commit()
