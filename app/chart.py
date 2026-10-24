TENORS = (91, 182, 364)


def _series(rows: list[dict], tenor: int, limit: int) -> list[dict]:
    matched = [row for row in rows if row["tenor"] == tenor][:limit]
    matched.reverse()
    return matched


def _points(series: list[dict]) -> str:
    if len(series) < 2:
        return ""
    rates = [row["stop_rate"] for row in series]
    low = min(rates)
    high = max(rates)
    span = high - low or 1
    last = len(series) - 1
    coords = []
    for index, row in enumerate(series):
        x = 36 + (index / last) * 590
        y = 16 + (1 - (row["stop_rate"] - low) / span) * 128
        coords.append(f"{x:.1f},{y:.1f}")
    return " ".join(coords)


def chart_page(rows: list[dict], limit: int = 80) -> str:
    parts = [
        "<!doctype html><html><head><meta charset='utf-8'>",
        "<title>NTB stop rates</title>",
        "<style>",
        "body{font-family:sans-serif;margin:32px;background:#fff;color:#111}",
        "svg{width:100%;max-width:720px;height:180px}",
        "</style></head><body>",
        "<h1>NTB stop rates</h1>",
    ]
    for tenor in TENORS:
        series = _series(rows, tenor, limit)
        latest = f" {series[-1]['stop_rate']}%" if series else ""
        parts.append(f"<h2>{tenor}-day{latest}</h2>")
        parts.append(
            "<svg viewBox='0 0 640 160'>"
            "<polyline fill='none' stroke='#111' stroke-width='2' "
            f"points='{_points(series)}'/>"
            "</svg>"
        )
    parts.append("</body></html>")
    return "".join(parts)
