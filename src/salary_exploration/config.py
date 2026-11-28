"""Project constants: folders, filenames and the default search."""

from pathlib import Path

# Folders are relative to the project folder, where the commands are run from.
DATA_FOLDER = Path("data")
SEARCH_FOLDER = Path("search")

COUNTRY_JOB_SALARY_FILENAME = "country_job_salary.csv"
COUNTRY_JOB_SALARY_TRANSFORMED_FILENAME = "country_job_salary_transformed.csv"
COUNTRIES_FILENAME = "countries.csv"
JOBS_FILENAME = "jobs.csv"
# Cache of Payscale country codes and country names, e.g. {"IT": "Italy"}.
COUNTRY_CODE_COUNTRIES_FILENAME = "country_code_countries.pk"

# Each exploration is saved in a data subfolder named after its UTC start time.
DATETIME_FORMAT = "%Y%m%dT%H%M%SZ"

# Used when the search folder has no countries.csv or jobs.csv.
DEFAULT_COUNTRY_SEARCH = "Italy"
DEFAULT_COUNTRIES_SEARCH = [
    DEFAULT_COUNTRY_SEARCH,
    "Germany",
    # "Spain",
    # "United States",
    # "Switzerland",
]
DEFAULT_JOB_SEARCH = "Data Engineer"
DEFAULT_JOBS_SEARCH = [
    DEFAULT_JOB_SEARCH,
    "Data Scientist",
    # "Embedded Software Engineer",
]

# Seconds to wait between browser steps, so pages can load and we stay gentle with the sites.
SLEEP_TIME = 5
