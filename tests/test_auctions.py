from fastapi.testclient import TestClient

from app.auctions import auctions_from
from app.main import create_app

ROW = {
    "auctionDate": "October-07-2026",
    "tenor": "91DAY",
    "rate": "15.5000",
    "amtOffered": "100000.0000",
    "totalSubscription": "39423.5700",
    "totalSuccessful": "38548.9530",
}


def test_auctions_from_cbn_row() -> None:
    parsed = auctions_from([ROW, {"auctionDate": "", "tenor": "91"}])

    assert parsed == [
        {
            "auction_date": "2026-10-07",
            "tenor": 91,
            "stop_rate": 15.5,
            "amount_offered": 100000.0,
            "amount_subscribed": 39423.57,
            "amount_allotted": 38548.953,
        }
    ]


def test_auctions_endpoint(monkeypatch) -> None:
    monkeypatch.setattr("app.api.auctions.fetch_auctions", lambda: auctions_from([ROW]))
    client = TestClient(create_app())

    response = client.get("/auctions", params={"tenor": 364})

    assert response.status_code == 200
    assert response.json() == []


def test_auctions_endpoint_returns_matching_tenor(monkeypatch) -> None:
    monkeypatch.setattr("app.api.auctions.fetch_auctions", lambda: auctions_from([ROW]))
    client = TestClient(create_app())

    response = client.get("/auctions", params={"tenor": 91, "limit": 5})

    assert response.status_code == 200
    assert response.json() == auctions_from([ROW])
