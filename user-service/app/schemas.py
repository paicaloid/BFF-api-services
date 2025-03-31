from pydantic import BaseModel


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

    class Config:
        orm_mode = True
