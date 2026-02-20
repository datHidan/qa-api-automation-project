import requests

class ApiClient:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self._token: str | None = None

    def set_bearer_token(self, token: str | None):
        self._token = token
        if token:
            self.session.headers.update({"Authorization": f"Bearer {token}"})
        else:
            self.session.headers.pop("Authorization", None)

    def post(self, path: str, json: dict | None = None):
        return self.session.post(f"{self.base_url}{path}", json=json, timeout=10)

    def get(self, path: str, params: dict | None = None):
        return self.session.get(f"{self.base_url}{path}", params=params, timeout=10)