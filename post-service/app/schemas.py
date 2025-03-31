from pydantic import BaseModel


class PostBase(BaseModel):
    title: str
    body: str
    userId: int


class PostCreate(PostBase):
    pass


class PostUpdate(PostBase):
    pass


class PostPublic(PostBase):
    id: int

    class Config:
        orm_mode = True
