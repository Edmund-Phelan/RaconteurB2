# Raconteur, Group 2

See [ARCHITECTURE.md](ARCHITECTURE.md) for the design and decisions.

## Install

Requires Python 3.11+. Run every command from the repository root, because the program reads `data.json` from the current folder.

**With [uv](https://docs.astral.sh/uv/)** 

```sh
uv sync
```

**Without uv**

```sh
python -m venv .venv
source .venv/bin/activate        # fish: source .venv/bin/activate.fish
pip install -e .
```

## Run

If you installed without uv, drop the `uv run` prefix from the commands below.

**Summary and plot**

```sh
uv run raconteur
```

It asks for a country and a year. Leave either blank to include everything. The plot is saved to `cumulative_duration.png`.

**Country comparison**

```sh
uv run raconteur compare
```

It asks for Country A, Country B, a start year and an end year (both years included). It prints each country's EVA count, total hours and average hours, then names the country with the greater total, or reports a tie. The countries in the data are `USA` and `Russia`.

## Tests

```sh
uv run python -m unittest discover -s tests -v
```
