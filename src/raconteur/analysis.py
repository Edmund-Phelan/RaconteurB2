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


def compare_countries(records, country_a, country_b, start_year, end_year):
    """Count, total and average hours per country over an inclusive year range, plus the leader (None for a tie).

    Raises ValueError for a reversed year range or a country not in the records.
    """
    if start_year > end_year:
        raise ValueError(f"Start year {start_year} is after end year {end_year}.")
    known = {r.country for r in records}
    for country in (country_a, country_b):
        if country not in known:
            raise ValueError(f"Unknown country '{country}'. Known countries: {', '.join(sorted(known))}.")

    stats = []
    for country in (country_a, country_b):
        selected = filter_records(records, country, start_year, end_year)
        total = total_hours(selected)
        average = total / len(selected) if selected else None
        stats.append({"country": country, "count": len(selected), "total": total, "average": average})

    a, b = stats
    leader = a["country"] if a["total"] > b["total"] else b["country"] if b["total"] > a["total"] else None
    return {"start_year": start_year, "end_year": end_year, "countries": stats, "leader": leader}
