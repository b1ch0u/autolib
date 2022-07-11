from pydantic import BaseModel


class CarBase(BaseModel):
    x: int
    y: int


class CarCreate(CarBase):
    pass


class Car(CarBase):
    id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    car: Car | None

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str
