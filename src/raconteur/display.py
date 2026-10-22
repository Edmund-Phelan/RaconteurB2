import matplotlib.pyplot as plt


def print_summary(counts, total_hours, country, year):
    total = sum(counts.values())
    print(f"{total} trips were performed.")
    for name, count in counts.items():
        print(f"{count} {name} trips, {count/total*100:.2f}% of trips.")

    if country:
        print(f"For {country}")
    if year:
        print(f"In {year}")
    print(f"Total hours spent on trips: {total_hours}")
    print(f"Total eva trips: {total}")


def plot_cumulative(dates, hours):
    plt.plot(dates, hours)
    plt.xlabel("Year")
    plt.ylabel("Cumulative EVA duration (hours)")
    plt.tight_layout()
    plt.savefig("cumulative_duration.png")
    plt.show()


def print_comparison(result):
    print(f"EVA comparison, {result['start_year']} to {result['end_year']} (inclusive)")
    for s in result["countries"]:
        average = f"{s['average']:.2f} hours" if s["average"] is not None else "unavailable"
        print(f"{s['country']}: {s['count']} EVAs, {s['total']:.2f} total hours, average {average}")
    if result["leader"]:
        print(f"{result['leader']} had the greater total EVA duration.")
    else:
        print("Tie: both countries had the same total EVA duration.")
