import json
from datetime import datetime
from typing import NamedTuple


class Record(NamedTuple):
    date: datetime
    hours: float
    country: str


def load_records(path: str) -> list[Record]:
    with open(path, "r", encoding="utf-8") as file:
        eva_data = json.load(file)

    records = []
    for eva in eva_data:
        date_text = eva.get("date")
        duration_text = eva.get("duration")
        country = eva.get("country")

        if not all((date_text, duration_text, country)):
            continue

        hours, minutes = map(int, duration_text.split(":"))
        records.append(Record(datetime.fromisoformat(date_text), hours + minutes / 60, country))
    return records
