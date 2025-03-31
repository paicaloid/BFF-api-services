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


class PostBase(BaseModel):
    userId: int
    title: str
    body: str


class PostCreate(PostBase):
    pass


class PostUpdate(PostBase):
    pass


class PostPublic(PostBase):
    id: int


class UserPostsPublic(UserPublic):
    posts: list["PostPublic"]
