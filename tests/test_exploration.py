import pandas as pd
import pytest

from salary_exploration import exploration


@pytest.fixture
def project_folder(tmp_path, monkeypatch):
    """Run the test from an empty project folder."""
    monkeypatch.chdir(tmp_path)
    return tmp_path


def _fake_get_salary(country, job):
    return {"Italy": "€1000", "Germany": "€2000"}.get(country)


def test_get_all_and_last_explorations(project_folder):
    for date_string in ["20200102T000000Z", "20200101T000000Z"]:
        (project_folder / "data" / date_string).mkdir(parents=True)
    (project_folder / "data" / "country_code_countries.pk").write_bytes(b"")

    assert exploration.get_all_explorations() == ["20200101T000000Z", "20200102T000000Z"]
    assert exploration.get_last_exploration() == "20200102T000000Z"


def test_no_explorations_without_data_folder(project_folder):
    assert exploration.get_all_explorations() == []
    assert exploration.get_last_exploration() is None


def test_get_country_job_salary_transformed(project_folder):
    folder = project_folder / "data" / "20200101T000000Z"
    folder.mkdir(parents=True)
    (folder / "country_job_salary_transformed.csv").write_text(
        "Country,Job,Local Currency Salary,Euro Salary\nItaly,Data Engineer,€1000,1000.0\n",
        encoding="utf-8",
    )

    df = exploration.get_country_job_salary_transformed("20200101T000000Z")

    assert list(df["Country"]) == ["Italy"]
    assert df.loc[0, "Euro Salary"] == 1000.0


def test_extract_salaries_uses_default_search_and_archives_it(project_folder, monkeypatch):
    monkeypatch.setattr(exploration.extract, "get_salary", _fake_get_salary)

    exploration.extract_salaries("20200101T000000Z")

    folder = project_folder / "data" / "20200101T000000Z"
    salaries = pd.read_csv(folder / "country_job_salary.csv", encoding="utf-8")
    assert list(salaries.columns) == ["Country", "Job", "Salary"]
    assert len(salaries) == 4
    assert (folder / "countries.csv").is_file()
    assert (folder / "jobs.csv").is_file()
    assert not (project_folder / "search" / "countries.csv").exists()


def test_extract_salaries_reads_the_search_folder(project_folder, monkeypatch):
    monkeypatch.setattr(exploration.extract, "get_salary", _fake_get_salary)
    (project_folder / "search").mkdir()
    (project_folder / "search" / "countries.csv").write_text("Country\nGermany\n")
    (project_folder / "search" / "jobs.csv").write_text("Job\nData Engineer\n")

    exploration.extract_salaries("20200101T000000Z")

    folder = project_folder / "data" / "20200101T000000Z"
    salaries = pd.read_csv(folder / "country_job_salary.csv", encoding="utf-8")
    assert salaries.to_dict(orient="records") == [
        {"Country": "Germany", "Job": "Data Engineer", "Salary": "€2000"}
    ]


def test_extract_salaries_keeps_an_existing_extraction(project_folder, monkeypatch):
    folder = project_folder / "data" / "20200101T000000Z"
    folder.mkdir(parents=True)
    (folder / "country_job_salary.csv").write_text("already here")
    monkeypatch.setattr(exploration.extract, "get_salary", pytest.fail)

    exploration.extract_salaries("20200101T000000Z")

    assert (folder / "country_job_salary.csv").read_text() == "already here"


def test_main_runs_extraction_and_transform(project_folder, monkeypatch):
    monkeypatch.setattr(exploration.extract, "get_salary", _fake_get_salary)

    exploration.main(["--date_string", "20200101T000000Z"])

    folder = project_folder / "data" / "20200101T000000Z"
    transformed = pd.read_csv(folder / "country_job_salary_transformed.csv", encoding="utf-8")
    assert list(transformed["Euro Salary"]) == [1000.0, 1000.0, 2000.0, 2000.0]


def test_main_rejects_a_bad_date_string(project_folder):
    with pytest.raises(SystemExit):
        exploration.main(["--date_string", "yesterday"])
    assert not (project_folder / "data").exists()
