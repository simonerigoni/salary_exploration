"""Run a salary exploration: scrape the salaries, then convert them to euro.

Usage: uv run salary-exploration [--date_string 20220530T103056Z]
"""

import argparse
import datetime

import pandas as pd

from salary_exploration import extract
from salary_exploration.config import (
    COUNTRIES_FILENAME,
    COUNTRY_JOB_SALARY_FILENAME,
    COUNTRY_JOB_SALARY_TRANSFORMED_FILENAME,
    DATA_FOLDER,
    DATETIME_FORMAT,
    DEFAULT_COUNTRIES_SEARCH,
    DEFAULT_JOBS_SEARCH,
    JOBS_FILENAME,
    SEARCH_FOLDER,
)
from salary_exploration.transform import transform_salary


def get_all_explorations() -> list[str]:
    """Return the date strings of all explorations, oldest first."""
    if not DATA_FOLDER.is_dir():
        return []
    # Folder names are timestamps, so sorting by name sorts by date.
    return sorted(path.name for path in DATA_FOLDER.iterdir() if path.is_dir())


def get_last_exploration() -> str | None:
    """Return the date string of the newest exploration, or None if there is none."""
    explorations = get_all_explorations()
    return explorations[-1] if explorations else None


def get_country_job_salary_transformed(date_string: str) -> pd.DataFrame:
    """Read the euro salaries of one exploration."""
    path = DATA_FOLDER / date_string / COUNTRY_JOB_SALARY_TRANSFORMED_FILENAME
    return pd.read_csv(path, encoding="utf-8")


def extract_salaries(date_string: str) -> None:
    """Scrape the salary of every searched job in every searched country.

    The search files are then moved into the exploration folder, so every exploration
    keeps a record of what was searched.
    """
    folder = DATA_FOLDER / date_string
    output_path = folder / COUNTRY_JOB_SALARY_FILENAME
    if output_path.is_file():
        print(f"{output_path} already exists, skipping the extraction")
        return

    folder.mkdir(parents=True, exist_ok=True)
    countries = _read_search(COUNTRIES_FILENAME, "Country", DEFAULT_COUNTRIES_SEARCH)
    jobs = _read_search(JOBS_FILENAME, "Job", DEFAULT_JOBS_SEARCH)

    rows = [
        {"Country": country, "Job": job, "Salary": extract.get_salary(country, job)}
        for country in countries
        for job in jobs
    ]
    pd.DataFrame(rows, columns=["Country", "Job", "Salary"]).to_csv(
        output_path, index=False, encoding="utf-8"
    )

    for filename in [COUNTRIES_FILENAME, JOBS_FILENAME]:
        (SEARCH_FOLDER / filename).replace(folder / filename)


def _read_search(filename: str, column: str, defaults: list[str]) -> list[str]:
    """Read one search list from the search folder. Write the defaults there if it is missing."""
    path = SEARCH_FOLDER / filename
    if not path.is_file():
        SEARCH_FOLDER.mkdir(exist_ok=True)
        pd.DataFrame({column: defaults}).to_csv(path, index=False, encoding="utf-8")
    return pd.read_csv(path, encoding="utf-8")[column].tolist()


def run_exploration(date_string: str) -> None:
    """Extract the salaries, then convert them to euro."""
    folder = DATA_FOLDER / date_string
    extract_salaries(date_string)
    transform_salary(
        folder / COUNTRY_JOB_SALARY_FILENAME, folder / COUNTRY_JOB_SALARY_TRANSFORMED_FILENAME
    )


def main(argv: list[str] | None = None) -> None:
    """Command line entry point."""
    parser = argparse.ArgumentParser(description="Salary exploration")
    parser.add_argument(
        "--date_string",
        default=datetime.datetime.now(datetime.UTC).strftime(DATETIME_FORMAT),
        help="Exploration date in format YYYYMMDDTHHMMSSZ. "
        "Pass an existing one to only redo its transform.",
    )
    args = parser.parse_args(argv)

    # The date string becomes a folder name, so check it before creating anything.
    try:
        datetime.datetime.strptime(args.date_string, DATETIME_FORMAT)
    except ValueError:
        parser.error(f"incorrect date string format. It should be {DATETIME_FORMAT}")

    run_exploration(args.date_string)


if __name__ == "__main__":
    main()
