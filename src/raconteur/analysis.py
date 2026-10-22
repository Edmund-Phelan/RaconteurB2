from itertools import accumulate

CLASSES = ("short", "standard", "long")


def filter_records(records, country=None, start_year=None, end_year=None):
    """Records matching the country and inclusive year range, sorted by date. None/empty means no filter."""
    if country:
        records = [r for r in records if r.country == country]
    if start_year:
        records = [r for r in records if r.date.year >= start_year]
    if end_year:
        records = [r for r in records if r.date.year <= end_year]
    return sorted(records, key=lambda r: r.date)


def classify(hours):
    if hours < 4:
        return "short"
    if hours < 7:
        return "standard"
    return "long"


def count_by_class(records):
    return {c: sum(classify(r.hours) == c for r in records) for c in CLASSES}


def total_hours(records):
    return sum(r.hours for r in records)


def cumulative_hours(records):
    """(dates, running total of hours) in record order."""
    return [r.date for r in records], list(accumulate(r.hours for r in records))
