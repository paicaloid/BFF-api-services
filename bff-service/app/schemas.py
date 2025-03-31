from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class UserPublic(BaseModel):
    id: int
    name: str
    username: str
    email: str


class PostPublic(BaseModel):
    id: int
    userId: int
    title: str
    body: str


class UserPostsPublic(UserPublic):
    posts: list["PostPublic"]


class PostCreate(BaseModel):
    userId: int
    title: str
    body: str
