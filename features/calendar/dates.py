from datetime import date, datetime

DATE_FORMATS = ("%m/%d/%Y", "%Y-%m-%d")


def parse_date(text: str) -> date | None:
    value = text.strip()
    if not value:
        return None

    for date_format in DATE_FORMATS:
        try:
            return datetime.strptime(value, date_format).date()
        except ValueError:
            continue

    return None