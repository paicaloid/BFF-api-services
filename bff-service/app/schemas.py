from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class UserPublic(BaseModel):
    id: int
    name: str
    username: str
    email: str
