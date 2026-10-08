def quote(tenor: int, rate: float) -> dict[str, float | int]:
    discount = rate / 100
    accrual = discount * tenor / 365
    price = 100 * (1 - accrual)
    true_yield = discount / (1 - accrual) * 100
    return {
        "tenor": tenor,
        "discount_rate": round(rate, 4),
        "true_yield": round(true_yield, 4),
        "price": round(price, 4),
    }
