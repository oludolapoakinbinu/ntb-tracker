import httpx2
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import HTMLResponse

from app.auctions import fetch_auctions
from app.chart import chart_page

router = APIRouter(tags=["chart"])


@router.get("/chart", response_class=HTMLResponse)
def stop_rate_chart(
    limit: int = Query(default=80, gt=0, le=100),
) -> HTMLResponse:
    try:
        rows = fetch_auctions()
    except httpx2.HTTPError as exc:
        raise HTTPException(status_code=502, detail="auction feed unavailable") from exc
    return HTMLResponse(chart_page(rows, limit))
