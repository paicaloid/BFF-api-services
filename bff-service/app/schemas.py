from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class UserBase(BaseModel):
    name: str
    username: str
    email: str


class UserCreate(UserBase):
    pass


class UserUpdate(UserBase):
    pass


class UserPublic(UserBase):
    id: int


class PostPublic(BaseModel):
    id: int
    userId: int
    title: str
    body: str


class PostCreate(BaseModel):
    userId: int
    title: str
    body: str


class UserPostsPublic(UserPublic):
    posts: list["PostPublic"]
