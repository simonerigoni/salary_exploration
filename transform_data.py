# Transform data
#
# python transform_data.py data/20220529T121639Z/country_job_salary.csv

import os
import argparse
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd


SLEEP_TIME = 5


def convert_local_currency_to_euro(local_currency):
    '''
    Convert local currency to euro

    Parameters:
        input_file: File with salary to normalize

    Returns:
        None
    '''
    print('Convert local currency to euro')

    euro_amount = None

    if '€' in local_currency:
        euro_amount = float(local_currency.replace('€', ''))
    else:
        url = 'https://www.google.com/'

        time.sleep(SLEEP_TIME)
        print('Connecting to {}'.format(url))
        browser = webdriver.Firefox()
        browser.get(url)
        print(browser.title)

        if 'Google' in browser.title:
            time.sleep(SLEEP_TIME)
            print('Accept cookies')
            accept_cookies_button =  browser.find_element(by = By.ID, value = 'L2AGLb')
            accept_cookies_button.click()

            time.sleep(SLEEP_TIME)
            print('Search for conversion')
            search_box = browser.find_element(by = By.NAME, value = 'q')
            search_box.send_keys('{} to euro'.format(local_currency))
            search_box.submit()

            browser.switch_to.default_content()

            time.sleep(SLEEP_TIME)
            element =  browser.find_element(by = By.XPATH, value = '/html/body/div[7]/div/div[10]/div/div[2]/div[2]/div/div/div[1]/div/div/div/div/div/div/div[3]/div[1]/div[1]/div[2]/span[1]')
            euro_string = element.text
            euro_amount = float(euro_string.replace(' ', '').replace(',', '.'))

            print('Close the browser')
            time.sleep(SLEEP_TIME)
            #browser.quit()
        else:
            print('Error: another page was expected')

    return euro_amount


def normalize_salary(input_file):
    '''
    Create a CSV file with normalized salary

    Parameters:
        input_file: File with salary to normalize

    Returns:
        None
    '''
    print('Create a CSV file with normalized salary')
    if os.path.isfile(input_file) is False:
        print('Error: file {} not found')
    else:
        filename, extension = input_file.split('.')

        if extension == 'csv':
            output_filename = filename + '_normalized.csv'
            
            if os.path.isfile(output_filename) is False:
                 
                df = pd.read_csv(input_file)
                with open(output_filename, 'w') as output_file:
                    output_file.write('Country,Job,Local Currency Salary,Euro Salary\n')
                
                    for index, row in df.iterrows():
                        if row['Salary'] == 'None':
                            pass
                        else:
                            euro_salary = convert_local_currency_to_euro(row['Salary'])
                            output_file.write('{},{},{},{}\n'.format(row['Country'], row['Job'], row['Salary'], euro_salary))
            else:
                pass
        else:
            print('Error: {} file extension not supported. {} expected'.format(extension, 'csv'))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=  'Transform data')
    parser.add_argument('--input_file', default =  'data/20220529T121639Z/country_job_salary.csv', help = 'Date in format YYYYMMMDDTHHMMSSZ')

    args = parser.parse_args()
    # print(args)

    input_file = args.input_file

    # print(convert_local_currency_to_euro('€30159'))
    # print(convert_local_currency_to_euro('96304 Fr.'))

    normalize_salary(input_file)
else:
    pass