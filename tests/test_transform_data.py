import pandas as pd

import configuration
from salary_exploration import _create_folders
from transform_data import convert_local_currency_to_euro, transform_salary


def test_convert_local_currency_to_euro_parses_euro_amount():
    assert convert_local_currency_to_euro("€1234.50") == 1234.50
    assert convert_local_currency_to_euro("€0") == 0.0


def test_create_folders(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(configuration, "DATA_FOLDER", "data")
    monkeypatch.setattr(configuration, "SEARCH_FOLDER", "search")
    _create_folders("20200101T000000Z")
    assert (tmp_path / "data").is_dir()
    assert (tmp_path / "search").is_dir()
    assert (tmp_path / "data" / "20200101T000000Z").is_dir()


def test_transform_salary_missing_file_is_a_no_op(tmp_path, capsys):
    missing = tmp_path / "missing.csv"
    output = tmp_path / "out.csv"
    transform_salary(str(missing), str(output))
    assert not output.exists()
    assert "not found" in capsys.readouterr().out


def test_transform_salary_converts_euro_rows(tmp_path):
    input_path = tmp_path / "country_job_salary.csv"
    output_path = tmp_path / "country_job_salary_transformed.csv"
    # Euro-only fixture so convert_local_currency_to_euro does not open a browser.
    pd.DataFrame({"Country": ["Italy"], "Job": ["Data Engineer"], "Salary": ["€1000.00"]}).to_csv(
        input_path, index=False
    )

    transform_salary(str(input_path), str(output_path))
    result = pd.read_csv(output_path)
    assert list(result.columns) == ["Country", "Job", "Local Currency Salary", "Euro Salary"]
    assert len(result) == 1
    assert result.loc[0, "Country"] == "Italy"
    assert result.loc[0, "Euro Salary"] == 1000.0
