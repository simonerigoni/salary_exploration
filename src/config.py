# Config
#
# python -m src.config


DATA_FOLDER = "data"
IMAGES_FOLDER = "images"
SEARCH_FOLDER = "search"
COUNTRY_JOB_SALARY_FILENAME = "country_job_salary.csv"
COUNTRY_JOB_SALARY_TRANSFORMED_FILENAME = COUNTRY_JOB_SALARY_FILENAME.replace(
    ".csv", "_transformed.csv"
)
COUNTRIES_FILENAME = "countries.csv"
JOBS_FILENAME = "jobs.csv"
DATETIME_FORMAT = "%Y%m%dT%H%M%SZ"
DEAFULT_COUNTRY_SEARCH = "Italy"
DEAFULT_COUNTRIES_SEARCH = [
    DEAFULT_COUNTRY_SEARCH,
    "Germany",
    #"Spain",
    #"United States",
    #"Switzerland",
]
DEAFULT_JOB_SEARCH = "Data Engineer"
DEAFULT_JOBS_SEARCH = [
    DEAFULT_JOB_SEARCH,
    "Data Scientist",
    #"Embedded Software Engineer",
]
COUNTRY_CODE_COUNTRIES_FILENAME = "country_code_countries.pk"
SLEEP_TIME = 5


if __name__ == "__main__":
    print("Config")
    print(f"{DATA_FOLDER = }")
    print(f"{SEARCH_FOLDER = }")
    print(f"{COUNTRY_JOB_SALARY_FILENAME = }")
    print(f"{COUNTRY_JOB_SALARY_TRANSFORMED_FILENAME = }")
    print(f"{COUNTRIES_FILENAME = }")
    print(f"{JOBS_FILENAME = }")
    print(f"{DATETIME_FORMAT = }")
    print(f"{DEAFULT_COUNTRY_SEARCH = }")
    print(f"{DEAFULT_COUNTRIES_SEARCH = }")
    print(f"{DEAFULT_JOB_SEARCH = }")
    print(f"{DEAFULT_JOB_SEARCH = }")
    print(f"{COUNTRY_CODE_COUNTRIES_FILENAME = }")
    print(f"{SLEEP_TIME = }")
else:
    pass
