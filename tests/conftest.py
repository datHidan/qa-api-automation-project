import os
import subprocess
import sys
import time

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
def api_server(api_base_url: str):
    """
    Starts FastAPI server for the whole test session (unless API_BASE_URL points elsewhere).
    Set START_API_SERVER=0 to disable local startup (useful if you run server manually).
    """
    start = os.getenv("START_API_SERVER", "1") != "0"
    if not start:
        yield
        return

    # Start uvicorn as subprocess
    cmd = [
        sys.executable, "-m", "uvicorn",
        "app.main:app",
        "--host", "127.0.0.1",
        "--port", "8000",
        "--log-level", "warning",
    ]

    # On Windows, avoid opening a new console window
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