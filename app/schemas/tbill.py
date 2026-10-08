from pydantic import BaseModel


class TbillQuote(BaseModel):
    tenor: int
    discount_rate: float
    true_yield: float
    price: float
