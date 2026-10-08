from fastapi.testclient import TestClient

from app.main import create_app
from app.tbill import quote


def test_quote_91_day_bill() -> None:
    assert quote(91, 10) == {
        "tenor": 91,
        "discount_rate": 10,
        "true_yield": 10.2557,
        "price": 97.5068,
    }


def test_quote_endpoint() -> None:
    client = TestClient(create_app())

    response = client.get("/tbills", params={"tenor": 91, "rate": 10})

    assert response.status_code == 200
    assert response.json() == quote(91, 10)


def test_quote_rejects_bad_tenor() -> None:
    client = TestClient(create_app())

    response = client.get("/tbills", params={"tenor": 0, "rate": 10})

    assert response.status_code == 422
