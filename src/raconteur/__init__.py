import json
from datetime import datetime 
import matplotlib.pyplot as plt

def main() -> None:
    CHOSEN_COUNTRY = input("country: ")

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
    records.sort(key=lambda record: record[0])

    dates = []
    cumulative_hours = []
    total_hours = 0

    for date, duration_hours, _ in records:
        total_hours += duration_hours
        dates.append(date)
        cumulative_hours.append(total_hours)

    print(f"Total hours spend for {CHOSEN_COUNTRY}: {total_hours}")

    plt.plot(dates, cumulative_hours)
    plt.xlabel("Year")
    plt.ylabel("Cumulative EVA duration (hours)")
    plt.tight_layout()
    plt.savefig("cumulative_duration.png")
    plt.show()

if __name__ == "__main__":
    main()
