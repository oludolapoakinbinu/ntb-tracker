from fastapi.testclient import TestClient

from app.chart import chart_page
from app.main import create_app

ROWS = [
    {"tenor": 91, "stop_rate": 15.5, "auction_date": "2026-10-07"},
    {"tenor": 91, "stop_rate": 15.2, "auction_date": "2026-09-30"},
    {"tenor": 182, "stop_rate": 16.1, "auction_date": "2026-10-07"},
    {"tenor": 364, "stop_rate": 15.85, "auction_date": "2026-10-07"},
]


def test_chart_page_shows_latest_stop_rate() -> None:
    html = chart_page(ROWS)

    assert "91-day 15.5%" in html
    assert "182-day 16.1%" in html
    assert "<polyline" in html


def test_chart_endpoint(monkeypatch) -> None:
    monkeypatch.setattr("app.api.chart.fetch_auctions", lambda: ROWS)
    client = TestClient(create_app())

    response = client.get("/chart")

    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "91-day 15.5%" in response.text
