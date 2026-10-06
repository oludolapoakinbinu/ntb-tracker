from fastapi.testclient import TestClient

from app import __version__
from app.main import create_app


def test_health_returns_version_and_environment() -> None:
    client = TestClient(create_app())

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "version": __version__,
        "environment": "local",
    }


def test_openapi_names_the_service() -> None:
    client = TestClient(create_app())

    schema = client.get("/openapi.json").json()

    assert schema["info"]["title"] == "NTB Toolkit"
    assert schema["info"]["version"] == __version__
    assert "/health" in schema["paths"]
