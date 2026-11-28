"""Scrape salaries from payscale.com."""

import pickle
import re
import time

from selenium.webdriver.common.by import By

from salary_exploration.browser import open_browser
from salary_exploration.config import COUNTRY_CODE_COUNTRIES_FILENAME, DATA_FOLDER, SLEEP_TIME

PAYSCALE_COUNTRIES_URL = "https://www.payscale.com/research/Country"
PAYSCALE_SALARY_URL = "https://www.payscale.com/research/{country_code}/Job={job}/Salary"


def get_salary(country: str, job: str) -> str | None:
    """Return the salary Payscale shows for a job in a country, e.g. "€33158", or None."""
    # Payscale writes spaces as underscores, both in URLs and in country names.
    country = country.replace(" ", "_")
    job = job.replace(" ", "_")

    country_code = get_country_code(country)
    if country_code is None:
        print(f"Error: country code not found for {country}")
        return None

    browser = open_browser(PAYSCALE_SALARY_URL.format(country_code=country_code, job=job))
    try:
        if "PayScale" not in browser.title:
            print("Error: another page was expected")
            return None
        time.sleep(SLEEP_TIME)
        salary = browser.find_element(By.CLASS_NAME, "paycharts__value").text
        return salary.replace(",", "")
    finally:
        browser.quit()


def get_country_code(country: str) -> str | None:
    """Return the Payscale code of a country, e.g. "IT" for "Italy", or None if unknown."""
    if not DATA_FOLDER.is_dir():
        print(f"Error: {DATA_FOLDER} folder not found")
        return None

    for country_code, country_name in _load_country_code_countries().items():
        if country_name == country:
            return country_code

    print(f"Error: {country} not found")
    return None


def _load_country_code_countries() -> dict[str, str]:
    """Read the cached country codes. Scrape and cache them the first time."""
    cache_path = DATA_FOLDER / COUNTRY_CODE_COUNTRIES_FILENAME
    if not cache_path.is_file():
        cache_path.write_bytes(pickle.dumps(_scrape_country_code_countries()))
    # The cache is a file we wrote ourselves, so unpickling it is safe.
    return pickle.loads(cache_path.read_bytes())


def _scrape_country_code_countries() -> dict[str, str]:
    """Scrape the country codes from the Payscale country list."""
    browser = open_browser(PAYSCALE_COUNTRIES_URL)
    try:
        if "PayScale" not in browser.title:
            print("Error: another page was expected")
            return {}
        time.sleep(SLEEP_TIME)
        country_list = browser.find_element(By.XPATH, "/html/body/div[1]/div/div[2]/div/div[3]/div")
        return parse_country_code_countries(country_list.get_attribute("innerHTML") or "")
    finally:
        browser.quit()


def parse_country_code_countries(inner_html: str) -> dict[str, str]:
    """Turn links like href="/research/IT/Country=Italy/Salary" into {"IT": "Italy"}."""
    links = re.findall(r'href="/research/([^/"]+)/Country=([^/"]+)/Salary', inner_html)
    return dict(links)
