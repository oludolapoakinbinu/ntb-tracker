from fastapi import APIRouter, Query

from app.schemas.tbill import TbillQuote
from app.tbill import quote

router = APIRouter(tags=["tbills"])


@router.get("/tbills", response_model=TbillQuote)
def tbill_quote(
    tenor: int = Query(gt=0, le=365),
    rate: float = Query(ge=0, lt=100),
) -> TbillQuote:
    return TbillQuote(**quote(tenor, rate))
