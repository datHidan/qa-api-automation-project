import json
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Iterator

import pytest
import requests

from src.api_client import ApiClient


def _wait_for_health(url: str, timeout_s: int = 20) -> None:
    deadline = time.time() + timeout_s
    last_err = None

    while time.time() < deadline:
        try:
            r = requests.get(url, timeout=2)
            if r.status_code == 200:
                return
        except Exception as e:
            last_err = e

        time.sleep(0.5)

    raise RuntimeError(f"API not healthy after {timeout_s}s. Last error: {last_err}")


@pytest.fixture(scope="session")
def api_base_url() -> str:
    return os.getenv("API_BASE_URL", "http://127.0.0.1:8000")


@pytest.fixture(scope="session", autouse=True)
def api_server(api_base_url: str) -> Iterator[None]:
    """
    Automatically starts FastAPI server for the test session.
    Can be disabled with environment variable:
        START_API_SERVER=0
    """

    start = os.getenv("START_API_SERVER", "1") != "0"
    if not start:
        yield
        return

    cmd = [
        sys.executable,
        "-m",
        "uvicorn",
        "app.main:app",
        "--host",
        "127.0.0.1",
        "--port",
        "8000",
        "--log-level",
        "warning",
    ]

    creationflags = 0
    if sys.platform.startswith("win"):
        creationflags = subprocess.CREATE_NO_WINDOW  # type: ignore[attr-defined]

    proc = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        creationflags=creationflags,
    )

    try:
        _wait_for_health(f"{api_base_url}/health", timeout_s=25)
        yield
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()


@pytest.fixture(scope="session")
def api(api_base_url: str) -> ApiClient:
    return ApiClient(api_base_url)


@pytest.fixture(scope="session")
def credentials() -> dict:
    """
    Loads test credentials from data/credentials.json
    """
    path = Path(__file__).resolve().parent.parent / "data" / "credentials.json"
    return json.loads(path.read_text(encoding="utf-8"))


@pytest.fixture()
def auth_api(api: ApiClient, credentials: dict) -> Iterator[ApiClient]:
    """
    Logs in before each test and sets Bearer token.
    Clears token after test.
    """
    response = api.post("/api/login", json=credentials["valid"])
    assert response.status_code == 200, f"Login failed: {response.status_code} {response.text}"

    token = response.json()["token"]
    api.set_bearer_token(token)

    yield api

    api.set_bearer_token(None)