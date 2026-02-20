from pydantic import BaseModel, EmailStr, Field


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1)


class LoginResponse(BaseModel):
    token: str


class ErrorResponse(BaseModel):
    error: str


class UserCreateRequest(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    job: str = Field(min_length=1, max_length=100)


class UserResponse(BaseModel):
    id: int
    name: str
    job: str


class UserListResponse(BaseModel):
    data: list[UserResponse]