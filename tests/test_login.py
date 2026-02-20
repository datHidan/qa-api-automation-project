def test_login_success(api, credentials):
    r = api.post("/api/login", json=credentials["valid"])
    assert r.status_code == 200
    data = r.json()
    assert data["token"] == "qa_mock_token_123"


def test_login_invalid(api, credentials):
    r = api.post("/api/login", json=credentials["invalid"])
    assert r.status_code == 400
    data = r.json()
    assert data["error"] == "Invalid login"