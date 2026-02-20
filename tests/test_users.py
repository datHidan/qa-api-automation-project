from jsonschema import validate

user_schema = {
    "type": "object",
    "properties": {
        "id": {"type": "number"},
        "name": {"type": "string"},
        "job": {"type": "string"},
    },
    "required": ["id", "name", "job"]
}

def test_user_schema_validation(api):
    r = api.get("/api/users/1")
    assert r.status_code == 200
    validate(instance=r.json(), schema=user_schema)