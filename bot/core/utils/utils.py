from datetime import datetime


def parse_date(s: str) -> str | None:
    try:
        dt = datetime.fromisoformat(s.replace("Z", "+00:00"))

        today = datetime.today()

        if dt.date() == today.date():
            return dt.strftime('%H:%M')

        return dt.strftime("%d.%m.%y")
    except (ValueError, TypeError, AttributeError):
        return None
