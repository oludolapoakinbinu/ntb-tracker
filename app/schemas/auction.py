from pydantic import BaseModel


class Auction(BaseModel):
    auction_date: str
    tenor: int
    stop_rate: float
    amount_offered: float
    amount_subscribed: float
    amount_allotted: float
