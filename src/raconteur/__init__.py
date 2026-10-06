import json
from datetime import datetime 
import matplotlib.pyplot as plt

def main() -> None:
    CHOSEN_COUNTRY = input("country: ")
    CHOSEN_YEAR = int(input("year: ") or 0)

    with open("data.json", "r", encoding="utf-8") as file:
        eva_data = json.load(file)

    records = []

    for eva in eva_data:
        date_text = eva.get("date")
        duration_text = eva.get("duration")
        country = eva.get("country")

        if not all((date_text, duration_text, country)):
            continue

        date = datetime.fromisoformat(date_text)
        hours, minutes = map(int, duration_text.split(":"))
        duration_hours = hours + minutes / 60

        records.append((date, duration_hours, country))

    if CHOSEN_COUNTRY:
        records = list(filter(lambda record: record[2] == CHOSEN_COUNTRY, records))
    if CHOSEN_YEAR:
        records = list(filter(lambda record: record[0].year == CHOSEN_YEAR, records))
    records.sort(key=lambda record: record[0])

    for i, rec in enumerate(records):
        def classify(hours):
            if hours < 4: return "short"
            if hours < 7: return "standard"
            else: return "long"
        records[i] = (*rec, classify(rec[1]))

    short = len(list(filter(lambda r: r[3] == "short", records)))
    standard = len(list(filter(lambda r: r[3] == "standard", records)))
    long = len(list(filter(lambda r: r[3] == "long", records)))
    total = sum((short, standard, long))
    
    print(f"{total} trips were performed.")
    print(f"{short} short trips, {short/total*100:.2f}% of trips.")
    print(f"{standard} standard trips, {standard/total*100:.2f}% of trips.")
    print(f"{long} long trips, {long/total*100:.2f}% of trips.")

    dates = []
    cumulative_hours = []
    total_hours = 0

    for date, duration_hours, *_ in records:
        total_hours += duration_hours
        dates.append(date)
        cumulative_hours.append(total_hours)

    if CHOSEN_COUNTRY:
        print(f"For {CHOSEN_COUNTRY}")
    if CHOSEN_YEAR:
        print(f"In {CHOSEN_YEAR}")
    print(f"Total hours spent on trips: {total_hours}")
    print(f"Total eva trips: {len(records)}")

    plt.plot(dates, cumulative_hours)
    plt.xlabel("Year")
    plt.ylabel("Cumulative EVA duration (hours)")
    plt.tight_layout()
    plt.savefig("cumulative_duration.png")
    plt.show()

if __name__ == "__main__":
    main()
