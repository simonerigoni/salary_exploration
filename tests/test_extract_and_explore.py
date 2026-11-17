import pickle

import pandas as pd

import configuration
import extract_data
import salary_exploration


def test_get_country_code_from_pickle(tmp_path, monkeypatch, capsys):
    data = tmp_path / "data"
    data.mkdir()
    mapping = {"IT": "Italy", "DE": "Germany"}
    (data / configuration.COUNTRY_CODE_COUNTRIES_FILENAME).write_bytes(pickle.dumps(mapping))
    monkeypatch.setattr(configuration, "DATA_FOLDER", str(data))
    assert extract_data._get_country_code("Italy") == "IT"
    assert extract_data._get_country_code("Germany") == "DE"
    assert extract_data._get_country_code("Pluto") is None
    assert "Pluto not found" in capsys.readouterr().out


def test_get_country_code_missing_data_folder(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(configuration, "DATA_FOLDER", str(tmp_path / "missing"))
    assert extract_data._get_country_code("Italy") is None
    assert "folder not found" in capsys.readouterr().out


def test_get_last_and_all_explorations(tmp_path, monkeypatch):
    data = tmp_path / "data"
    older = data / "20200101T000000Z"
    newer = data / "20200102T000000Z"
    older.mkdir(parents=True)
    newer.mkdir(parents=True)
    (older / "marker").write_text("old")
    (newer / "marker").write_text("new")
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(configuration, "DATA_FOLDER", "data")
    assert salary_exploration.get_last_salary_exploration() == "20200102T000000Z"
    assert set(salary_exploration.get_all_salary_exploration()) == {
        "20200101T000000Z",
        "20200102T000000Z",
    }


def test_get_country_job_salary_transformed(tmp_path, monkeypatch):
    data = tmp_path / "data"
    date_string = "20200101T000000Z"
    folder = data / date_string
    folder.mkdir(parents=True)
    output = folder / configuration.COUNTRY_JOB_SALARY_TRANSFORMED_FILENAME
    pd.DataFrame(
        {
            "Country": ["Italy"],
            "Job": ["Data Engineer"],
            "Local Currency Salary": ["€1000"],
            "Euro Salary": [1000.0],
        }
    ).to_csv(output, index=False)
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(configuration, "DATA_FOLDER", "data")
    df = salary_exploration.get_country_job_salary_transformed(date_string)
    assert list(df["Country"]) == ["Italy"]
    assert df.loc[0, "Euro Salary"] == 1000.0


def test_configuration_constants():
    assert configuration.DATA_FOLDER == "data"
    assert configuration.COUNTRY_JOB_SALARY_TRANSFORMED_FILENAME.endswith("_transformed.csv")
    assert configuration.COUNTRY_CODE_COUNTRIES_FILENAME.endswith(".pk")
