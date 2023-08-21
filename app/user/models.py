from pydantic import BaseModel


class UserBase(BaseModel):
    name: str


class UserIn(UserBase):
    password: str


class UserOut(UserBase):
    id: int
    model_config = {"from_attributes": True}


class UserUpdate(UserBase):
    pass
