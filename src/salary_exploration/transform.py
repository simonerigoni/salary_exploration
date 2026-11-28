"""Convert the scraped salaries from local currency to euro."""

import math
import time
from pathlib import Path

import pandas as pd
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from salary_exploration.browser import open_browser
from salary_exploration.config import SLEEP_TIME

# Google shows the converted amount in one of these two places, depending on the page layout.
CONVERTED_AMOUNT_XPATHS = [
    "/html/body/div[7]/div/div[10]/div/div[2]/div[2]/div/div/div[1]/div/div/div/div/div/div/div[3]/div[1]/div[1]/div[2]/span[1]",
    "/html/body/div[7]/div/div[11]/div/div[2]/div[2]/div/div/div[1]/div/div/div/div/div/div/div[3]/div[1]/div[1]/div[2]/span[1]",
]


def is_missing_amount(value: object) -> bool:
    """Return True for a missing salary: None, NaN, or text such as "None" or "nan"."""
    if value is None:
        return True
    if isinstance(value, float) and math.isnan(value):
        return True
    return isinstance(value, str) and value.strip() in {"", "None", "nan", "NaN"}


def convert_local_currency_to_euro(local_currency: object) -> float | None:
    """Convert an amount such as "€30159" or "96304 Fr." to euro. Return None if missing."""
    if is_missing_amount(local_currency):
        return None

    amount = str(local_currency)
    if "€" in amount:
        return float(amount.replace("€", ""))
    return _convert_with_google(amount)


def _convert_with_google(amount: str) -> float | None:
    """Ask Google for the conversion. Return None if the result cannot be read."""
    print(f"Convert {amount} to euro")
    browser = open_browser("https://www.google.com/")
    try:
        if "Google" not in browser.title:
            print("Error: another page was expected")
            return None

        time.sleep(SLEEP_TIME)
        browser.find_element(By.ID, "L2AGLb").click()  # Accept cookies
        time.sleep(SLEEP_TIME)
        browser.find_element(By.XPATH, "/html/body/div[1]/div[4]/div/div/a").click()  # English

        time.sleep(SLEEP_TIME)
        search_box = browser.find_element(By.NAME, "q")
        search_box.send_keys(f"{amount} to EUR")
        search_box.submit()

        time.sleep(SLEEP_TIME)
        euro_text = _read_converted_amount(browser)
    finally:
        browser.quit()

    if euro_text == "":
        return None
    return float(euro_text.replace(" ", "").replace(",", ""))


def _read_converted_amount(browser: WebDriver) -> str:
    """Return the converted amount shown by Google, or "" if it is not on the page."""
    for xpath in CONVERTED_AMOUNT_XPATHS:
        try:
            return browser.find_element(By.XPATH, xpath).text
        except NoSuchElementException:
            continue
    return ""


def transform_salary(input_filename: str | Path, output_filename: str | Path) -> None:
    """Write a CSV with every salary converted to euro. Rows without a salary are skipped."""
    input_path = Path(input_filename)
    output_path = Path(output_filename)

    if not input_path.is_file():
        print(f"Error: file {input_path} not found")
        return
    if input_path.suffix.lower() != ".csv":
        print(f"Error: {input_path.suffix.lstrip('.')} file extension not supported. csv expected")
        return
    if output_path.is_file():
        print(f"{output_path} already exists, skipping the transform")
        return

    print(f"Transform {input_path} into {output_path}")
    salaries = pd.read_csv(input_path, encoding="utf-8")
    rows = [
        {
            "Country": row["Country"],
            "Job": row["Job"],
            "Local Currency Salary": row["Salary"],
            "Euro Salary": convert_local_currency_to_euro(row["Salary"]),
        }
        for row in salaries.to_dict(orient="records")
        if not is_missing_amount(row["Salary"])
    ]
    columns = ["Country", "Job", "Local Currency Salary", "Euro Salary"]
    pd.DataFrame(rows, columns=columns).to_csv(output_path, index=False, encoding="utf-8")
