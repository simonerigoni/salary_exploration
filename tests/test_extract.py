import pickle

import pytest

from salary_exploration import extract
from salary_exploration.config import COUNTRY_CODE_COUNTRIES_FILENAME


@pytest.fixture
def data_folder(tmp_path, monkeypatch):
    """Run the test from an empty project folder that has a data folder."""
    monkeypatch.chdir(tmp_path)
    (tmp_path / "data").mkdir()
    return tmp_path / "data"


def _write_country_codes(data_folder, country_code_countries):
    path = data_folder / COUNTRY_CODE_COUNTRIES_FILENAME
    path.write_bytes(pickle.dumps(country_code_countries))


def test_get_country_code_reads_the_cached_codes(data_folder, capsys):
    _write_country_codes(data_folder, {"IT": "Italy", "US": "United_States"})

    assert extract.get_country_code("Italy") == "IT"
    assert extract.get_country_code("United_States") == "US"
    assert extract.get_country_code("Pluto") is None
    assert "Pluto not found" in capsys.readouterr().out


def test_get_country_code_scrapes_and_caches_when_no_cache(data_folder, monkeypatch):
    monkeypatch.setattr(extract, "_scrape_country_code_countries", lambda: {"DE": "Germany"})

    assert extract.get_country_code("Germany") == "DE"
    cache = data_folder / COUNTRY_CODE_COUNTRIES_FILENAME
    assert pickle.loads(cache.read_bytes()) == {"DE": "Germany"}


def test_get_country_code_missing_data_folder(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    assert extract.get_country_code("Italy") is None
    assert "folder not found" in capsys.readouterr().out


def test_parse_country_code_countries():
    inner_html = (
        '<div class="location__col location__col--full">'
        '<a href="/research/IT/Country=Italy/Salary">Italy</a></div>'
        '<div class="location__col location__col--full">'
        '<a href="/research/US/Country=United_States/Salary">United States</a></div>'
    )
    assert extract.parse_country_code_countries(inner_html) == {
        "IT": "Italy",
        "US": "United_States",
    }


def test_get_salary_returns_none_for_an_unknown_country(data_folder):
    _write_country_codes(data_folder, {"IT": "Italy"})
    # No browser is opened: the country code lookup fails first.
    assert extract.get_salary("Pluto", "Data Engineer") is None
