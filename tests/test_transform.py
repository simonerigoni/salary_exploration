import pandas as pd

from salary_exploration.transform import convert_local_currency_to_euro, transform_salary


def _write_salaries(path, salaries):
    """Write a small country_job_salary.csv with one row per salary."""
    pd.DataFrame(
        {
            "Country": ["Italy", "Germany", "Spain"][: len(salaries)],
            "Job": ["Data Engineer", "Data Scientist", "Analyst"][: len(salaries)],
            "Salary": salaries,
        }
    ).to_csv(path, index=False, encoding="utf-8")


def test_convert_local_currency_to_euro_parses_euro_amount():
    assert convert_local_currency_to_euro("€1234.50") == 1234.50
    assert convert_local_currency_to_euro("€0") == 0.0


def test_convert_local_currency_to_euro_handles_missing_values():
    assert convert_local_currency_to_euro(None) is None
    assert convert_local_currency_to_euro(float("nan")) is None
    assert convert_local_currency_to_euro("None") is None
    assert convert_local_currency_to_euro("  None  ") is None
    assert convert_local_currency_to_euro("nan") is None
    assert convert_local_currency_to_euro("NaN") is None
    assert convert_local_currency_to_euro("") is None


def test_transform_salary_missing_file_is_a_no_op(tmp_path, capsys):
    missing = tmp_path / "archive.final.csv"
    output = tmp_path / "out.csv"
    transform_salary(missing, output)
    assert not output.exists()
    out = capsys.readouterr().out
    assert str(missing) in out
    assert "not found" in out


def test_transform_salary_rejects_non_csv_even_with_multiple_dots(tmp_path, capsys):
    input_path = tmp_path / "salary.data.txt"
    input_path.write_text("not csv")
    output_path = tmp_path / "out.csv"
    transform_salary(input_path, output_path)
    assert not output_path.exists()
    out = capsys.readouterr().out
    assert "txt" in out
    assert "not supported" in out


def test_transform_salary_skips_when_output_already_exists(tmp_path):
    input_path = tmp_path / "in.csv"
    output_path = tmp_path / "out.csv"
    _write_salaries(input_path, ["€1"])
    output_path.write_text("already here")
    transform_salary(input_path, output_path)
    assert output_path.read_text() == "already here"


def test_transform_salary_converts_euro_rows(tmp_path):
    input_path = tmp_path / "country_job_salary.csv"
    output_path = tmp_path / "country_job_salary_transformed.csv"
    # Euro-only fixture so convert_local_currency_to_euro does not open a browser.
    _write_salaries(input_path, ["€1000.00"])

    transform_salary(input_path, output_path)

    result = pd.read_csv(output_path, encoding="utf-8")
    assert list(result.columns) == ["Country", "Job", "Local Currency Salary", "Euro Salary"]
    assert result.to_dict(orient="records") == [
        {
            "Country": "Italy",
            "Job": "Data Engineer",
            "Local Currency Salary": "€1000.00",
            "Euro Salary": 1000.0,
        }
    ]


def test_transform_salary_skips_missing_salary_rows(tmp_path):
    input_path = tmp_path / "in.csv"
    output_path = tmp_path / "out.csv"
    _write_salaries(input_path, ["€1000.00", "None", "€2500.00"])

    transform_salary(input_path, output_path)

    result = pd.read_csv(output_path, encoding="utf-8")
    assert list(result["Country"]) == ["Italy", "Spain"]
    assert list(result["Euro Salary"]) == [1000.0, 2500.0]


def test_transform_salary_accepts_string_paths(tmp_path):
    input_path = tmp_path / "in.csv"
    output_path = tmp_path / "out.csv"
    _write_salaries(input_path, ["€1"])
    transform_salary(str(input_path), str(output_path))
    assert output_path.is_file()
