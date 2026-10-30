from fastapi.testclient import TestClient

from app.auctions import auctions_from, latest_auctions
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


def test_latest_auctions_keeps_newest_of_each_tenor() -> None:
    older = {
        "auction_date": "2026-09-30",
        "tenor": 91,
        "stop_rate": 15.2,
        "amount_offered": 100000.0,
        "amount_subscribed": 20000.0,
        "amount_allotted": 20000.0,
    }
    bill = {
        "auction_date": "2026-10-07",
        "tenor": 182,
        "stop_rate": 15.8,
        "amount_offered": 200000.0,
        "amount_subscribed": 400000.0,
        "amount_allotted": 200000.0,
    }
    year = {
        "auction_date": "2026-10-07",
        "tenor": 364,
        "stop_rate": 15.85,
        "amount_offered": 700000.0,
        "amount_subscribed": 1400000.0,
        "amount_allotted": 700000.0,
    }
    parsed = auctions_from([ROW])
    latest = latest_auctions([*parsed, older, bill, year])

    assert [row["tenor"] for row in latest] == [91, 182, 364]
    assert latest[0]["stop_rate"] == 15.5
    assert latest[0]["cover"] == 0.3942
    assert latest[1]["cover"] == 2.0


def test_latest_endpoint(monkeypatch) -> None:
    parsed = auctions_from([ROW])
    monkeypatch.setattr("app.api.auctions.fetch_auctions", lambda: parsed)
    client = TestClient(create_app())

    response = client.get("/auctions/latest")

    assert response.status_code == 200
    assert response.json()[0]["cover"] == 0.3942
