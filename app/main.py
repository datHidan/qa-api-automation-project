from fastapi import FastAPI
from fastapi.responses import JSONResponse

from app.schemas import (
    LoginRequest,
    LoginResponse,
    UserCreateRequest,
    UserResponse,
    UserListResponse,
)
from app.store import InMemoryStore

app = FastAPI(title="QA Mock API", version="1.0.0")
store = InMemoryStore()

# jednoduchá "auth" logika pro trénink
VALID_EMAIL = "eve.holt@reqres.in"
VALID_PASSWORD = "cityslicka"
FAKE_TOKEN = "qa_mock_token_123"

from fastapi import Header

def _is_authorized(authorization: str | None) -> bool:
    return authorization == f"Bearer {FAKE_TOKEN}"

@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/api/login", response_model=LoginResponse)
def login(payload: LoginRequest):
    if payload.email == VALID_EMAIL and payload.password == VALID_PASSWORD:
        return LoginResponse(token=FAKE_TOKEN)

    # stejné chování jako veřejné tréninkové API: 400 + error
    return JSONResponse(status_code=400, content={"error": "Invalid login"})


@app.get("/api/users", response_model=UserListResponse)
def list_users(authorization: str | None = Header(default=None)):
    if not _is_authorized(authorization):
        return JSONResponse(status_code=401, content={"error": "Unauthorized"})
    users = [UserResponse(id=u.id, name=u.name, job=u.job) for u in store.list_users()]
    return UserListResponse(data=users)


@app.get("/api/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int, authorization: str | None = Header(default=None)):
    if not _is_authorized(authorization):
        return JSONResponse(status_code=401, content={"error": "Unauthorized"})
    u = store.get_user(user_id)
    if not u:
        return JSONResponse(status_code=404, content={"error": "User not found"})
    return UserResponse(id=u.id, name=u.name, job=u.job)

@app.post("/api/users", response_model=UserResponse, status_code=201)
def create_user(payload: UserCreateRequest, authorization: str | None = Header(default=None)):
    if not _is_authorized(authorization):
        return JSONResponse(status_code=401, content={"error": "Unauthorized"})
    u = store.create_user(payload.name, payload.job)
    return UserResponse(id=u.id, name=u.name, job=u.job)