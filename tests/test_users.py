from jsonschema import validate

user_schema = {
    "type": "object",
    "properties": {
        "id": {"type": "number"},
        "name": {"type": "string"},
        "job": {"type": "string"},
    },
    "required": ["id", "name", "job"],
}

user_list_schema = {
    "type": "object",
    "properties": {
        "data": {
            "type": "array",
            "items": user_schema,
        }
    },
    "required": ["data"],
}


def test_users_requires_auth(api):
    r = api.get("/api/users")
    assert r.status_code == 401
    assert r.json()["error"] == "Unauthorized"


def test_list_users(auth_api):
    r = auth_api.get("/api/users")
    assert r.status_code == 200
    data = r.json()

    validate(instance=data, schema=user_list_schema)
    assert len(data["data"]) >= 2


def test_get_user_found(auth_api):
    r = auth_api.get("/api/users/1")
    assert r.status_code == 200
    data = r.json()

    validate(instance=data, schema=user_schema)
    assert data["id"] == 1


def test_get_user_not_found(auth_api):
    r = auth_api.get("/api/users/9999")
    assert r.status_code == 404
    assert r.json()["error"] == "User not found"


def test_create_user(auth_api):
    payload = {"name": "Jiri", "job": "QA Engineer"}
    r = auth_api.post("/api/users", json=payload)

    assert r.status_code == 201
    data = r.json()

    validate(instance=data, schema=user_schema)
    assert data["name"] == "Jiri"
    assert data["job"] == "QA Engineer"