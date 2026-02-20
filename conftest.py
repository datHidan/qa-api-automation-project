import pytest
from src.api_client import ApiClient

BASE_URL = "http://127.0.0.1:8000"

@pytest.fixture(scope="session")
def api():
    return ApiClient(BASE_URL)