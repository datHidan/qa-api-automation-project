def test_login_success(api):
    payload = {"email": "eve.holt@reqres.in", "password": "cityslicka"}
    r = api.post("/api/login", json=payload)

    assert r.status_code == 200
    data = r.json()
    assert data["token"] == "qa_mock_token_123"


def test_login_invalid(api):
    payload = {"email": "eve.holt@reqres.in", "password": "wrong"}
    r = api.post("/api/login", json=payload)

    assert r.status_code == 400
    data = r.json()
    assert data["error"] == "Invalid login"