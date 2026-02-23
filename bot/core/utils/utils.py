from datetime import datetime


def date_to_ddmmyy(s: str) -> str | None:
    try:
        dt = datetime.fromisoformat(s.replace("Z", "+00:00"))
        return dt.strftime("%d.%m.%y")
    except (ValueError, TypeError, AttributeError):
        return None
