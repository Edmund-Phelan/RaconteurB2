from . import analysis, data, display


def main() -> None:
    country = input("country: ")
    year = int(input("year: ") or 0)

    records = data.load_records("data.json")
    records = analysis.filter_records(records, country, year, year)

    display.print_summary(analysis.count_by_class(records), analysis.total_hours(records), country, year)
    display.plot_cumulative(*analysis.cumulative_hours(records))


if __name__ == "__main__":
    main()
