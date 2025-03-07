from pydantic import NaiveDatetime, BaseModel


class UserCreate(BaseModel):
    username: str
    email: str
    password: str


class RequestDetails(BaseModel):
    email: str
    password: str


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str


class ChangePassword(BaseModel):
    email: str
    old_password: str
    new_password: str


class TokenCreate(BaseModel):
    user_id: str
    access_token: str
    refresh_token: str
    status: bool
    created_date: NaiveDatetime
