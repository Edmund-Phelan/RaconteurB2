import sys

from . import analysis, data, display


def main() -> None:
    if sys.argv[1:] == ["compare"]:
        compare()
        return

    country = input("country: ")
    year = int(input("year: ") or 0)

    records = data.load_records("data.json")
    records = analysis.filter_records(records, country, year, year)

    display.print_summary(analysis.count_by_class(records), analysis.total_hours(records), country, year)
    display.plot_cumulative(*analysis.cumulative_hours(records))


def compare() -> None:
    country_a = input("Country A: ")
    country_b = input("Country B: ")
    try:
        start_year = int(input("Start year: "))
        end_year = int(input("End year: "))
    except ValueError:
        print("Years must be whole numbers, e.g. 1990.")
        return

    try:
        result = analysis.compare_countries(data.load_records("data.json"), country_a, country_b, start_year, end_year)
    except ValueError as error:
        print(error)
        return
    display.print_comparison(result)


if __name__ == "__main__":
    main()
