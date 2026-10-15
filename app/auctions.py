from datetime import datetime

import httpx2

CBN_NTB_URL = "https://www.cbn.gov.ng/api/GetAllSecuritiesNTB"


def _number(value: object) -> float | None:
    text = str(value or "").strip().replace(",", "").replace("%", "")
    if not text:
        return None
    try:
        return round(float(text), 4)
    except ValueError:
        return None


def _tenor(value: object) -> int | None:
    digits = ""
    for char in str(value or ""):
        if char.isdigit():
            digits += char
        elif digits:
            break
    if not digits:
        return None
    return int(digits)


def _date(value: object) -> str | None:
    try:
        return datetime.strptime(str(value), "%B-%d-%Y").date().isoformat()
    except ValueError:
        return None


def auctions_from(rows: list[dict]) -> list[dict]:
    auctions = []
    for row in rows:
        auction_date = _date(row.get("auctionDate"))
        tenor = _tenor(row.get("tenor"))
        stop_rate = _number(row.get("rate"))
        offered = _number(row.get("amtOffered"))
        subscribed = _number(row.get("totalSubscription"))
        allotted = _number(row.get("totalSuccessful"))
        if None in (auction_date, tenor, stop_rate, offered, subscribed, allotted):
            continue
        auctions.append(
            {
                "auction_date": auction_date,
                "tenor": tenor,
                "stop_rate": stop_rate,
                "amount_offered": offered,
                "amount_subscribed": subscribed,
                "amount_allotted": allotted,
            }
        )
    auctions.sort(key=lambda item: item["auction_date"], reverse=True)
    return auctions


def fetch_auctions() -> list[dict]:
    response = httpx2.get(CBN_NTB_URL, timeout=30)
    response.raise_for_status()
    return auctions_from(response.json())
