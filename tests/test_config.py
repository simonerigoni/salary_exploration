from salary_exploration import config


def test_filenames():
    assert config.COUNTRY_JOB_SALARY_FILENAME == "country_job_salary.csv"
    assert config.COUNTRY_JOB_SALARY_TRANSFORMED_FILENAME == "country_job_salary_transformed.csv"
    assert config.COUNTRY_CODE_COUNTRIES_FILENAME == "country_code_countries.pk"


def test_folders_are_relative_to_the_project_folder():
    assert str(config.DATA_FOLDER) == "data"
    assert str(config.SEARCH_FOLDER) == "search"


def test_default_searches_start_with_the_default_country_and_job():
    assert config.DEFAULT_COUNTRIES_SEARCH[0] == config.DEFAULT_COUNTRY_SEARCH
    assert config.DEFAULT_JOBS_SEARCH[0] == config.DEFAULT_JOB_SEARCH
