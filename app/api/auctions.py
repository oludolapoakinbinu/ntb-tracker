import httpx2
from fastapi import APIRouter, HTTPException, Query

from app.auctions import fetch_auctions, latest_auctions
from app.schemas.auction import Auction, LatestAuction

router = APIRouter(tags=["auctions"])


@router.get("/auctions/latest", response_model=list[LatestAuction])
def list_latest_auctions() -> list[LatestAuction]:
    try:
        rows = fetch_auctions()
    except httpx2.HTTPError as exc:
        raise HTTPException(status_code=502, detail="auction feed unavailable") from exc
    return [LatestAuction(**row) for row in latest_auctions(rows)]


@router.get("/auctions", response_model=list[Auction])
def list_auctions(
    tenor: int | None = Query(default=None, gt=0, le=365),
    limit: int = Query(default=30, gt=0, le=100),
) -> list[Auction]:
    try:
        rows = fetch_auctions()
    except httpx2.HTTPError as exc:
        raise HTTPException(status_code=502, detail="auction feed unavailable") from exc
    if tenor is not None:
        rows = [row for row in rows if row["tenor"] == tenor]
    return [Auction(**row) for row in rows[:limit]]
