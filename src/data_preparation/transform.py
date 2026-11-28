# Transform data
#
# python -m src.data_preparation.transfor data/20220529T121639Z/country_job_salary.csv

import os
import argparse
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd


from src.config import SLEEP_TIME


def convert_local_currency_to_euro(local_currency: str) -> float:
    """
    Convert local currency to euro

    Args:
        input_file: File with salary to transform

    Returns:
        None
    """

    print("Convert local currency {} to euro".format(local_currency))
    euro_amount = None

    if local_currency is None or local_currency == 'nan':
        pass
    else:
        if "€" in local_currency:
            euro_amount = float(local_currency.replace("€", ""))
        else:
            url = "https://www.google.com/"

            time.sleep(SLEEP_TIME)
            print("Connecting to {}".format(url))
            browser = webdriver.Firefox()
            browser.get(url)
            print(browser.title)

            if "Google" in browser.title:
                time.sleep(SLEEP_TIME)
                print("Accept cookies")
                accept_cookies_button = browser.find_element(by=By.ID, value="L2AGLb")
                accept_cookies_button.click()

                time.sleep(SLEEP_TIME)
                print("Select English")
                element = browser.find_element(
                    by=By.XPATH, value="/html/body/div[1]/div[4]/div/div/a"
                )
                element.click()

                time.sleep(SLEEP_TIME)
                print("Search for conversion")
                search_box = browser.find_element(by=By.NAME, value="q")
                search_box.send_keys("{} to EUR".format(local_currency))
                search_box.submit()

                time.sleep(SLEEP_TIME)
                print("Read converted value")

                euro_string = ""

                try:
                    element = browser.find_element(
                        by=By.XPATH,
                        value="/html/body/div[7]/div/div[10]/div/div[2]/div[2]/div/div/div[1]/div/div/div/div/div/div/div[3]/div[1]/div[1]/div[2]/span[1]",
                    )
                    euro_string = element.text
                except Exception as e:
                    print(e)

                if euro_string == "":
                    try:
                        element = browser.find_element(
                            by=By.XPATH,
                            value="/html/body/div[7]/div/div[11]/div/div[2]/div[2]/div/div/div[1]/div/div/div/div/div/div/div[3]/div[1]/div[1]/div[2]/span[1]",
                        )
                        euro_string = element.text
                    except Exception as e:
                        print(e)
                else:
                    pass

                if euro_string == "":
                    euro_string = "0"
                else:
                    pass

                euro_amount = float(euro_string.replace(" ", "").replace(",", ""))

                time.sleep(SLEEP_TIME)
                print("Close the browser")
                browser.quit()
            else:
                print("Error: another page was expected")

    return euro_amount


def transform_salary(input_filename: str, output_filename: str) -> None:
    """
    Create a CSV file with transformed salary

    Args:
        input_filename: File with salary to transform

    Returns:
        None
    """

    print("Create a CSV file with transformed salary")
    if os.path.isfile(input_filename) is False:
        print("Error: file {} not found")
    else:
        filename, extension = input_filename.split(".")

        if extension == "csv":
            if os.path.isfile(output_filename) is False:
                df = pd.read_csv(input_filename, encoding='windows-1252')
                with open(output_filename, "w") as output_file:
                    output_file.write("Country,Job,Euro Salary\n")

                    for index, row in df.iterrows():
                        if row["Salary"] == "None":
                            pass
                        else:
                            euro_salary = convert_local_currency_to_euro(row["Salary"])
                            output_file.write(
                                "{},{},{},{}\n".format(
                                    row["Country"],
                                    row["Job"],
                                    euro_salary,
                                )
                            )
            else:
                pass
        else:
            print(
                "Error: {} file extension not supported. {} expected".format(
                    extension, "csv"
                )
            )


if __name__ == "__main__":
    print("Transform data")
    parser = argparse.ArgumentParser(description="Transform data")
    parser.add_argument(
        "--input_file",
        help="Input filepath in format data/YYYYMMMDDTHHMMSSZ/country_job_salary.csv",
    )

    args = parser.parse_args()
    # print(args)

    input_file = args.input_file

    # print(convert_local_currency_to_euro('€30159'))
    # print(convert_local_currency_to_euro('96304 Fr.'))

    transform_salary(input_file, input_file.replace(".csv", "_transformed.csv"))
else:
    pass
