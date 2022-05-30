# Scrape data from https://www.payscale.com/research/IT/Job=Data_Engineer/Salary
#
# python extract_data.py --country='United States' --job='Data Engineer'

import os
import argparse
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import pickle


SLEEP_TIME = 5


def _get_country_code(country):
    '''
    Get the country for a specific code

    Parameters:
        country: Country to search

    Returns:
        country_code: Code of the searched country
    '''

    print('Get country code')
    country_code_countries = {}

    if os.path.isdir('data') is True:
        if os.path.isfile('data/country_code_countries.pkl') is True:
            with open('data/country_code_countries.pkl', 'rb') as input_file:
                country_code_countries = pickle.load(input_file)
        else:
            country_code_countries = _get_country_code_countries()
            with open('data/country_code_countries.pkl', 'wb') as output_file:
                pickle.dump(country_code_countries, output_file)

        if country in country_code_countries.values():
            for key, value in country_code_countries.items():
                if country == value:
                    return key
                else:
                    pass
        else:
            print('Error: {} not found'.format(country))
    else:
        print('Error: data folder not found')

    return None


def _get_country_code_countries():
    '''
    Scrape country codes and countries from web page

    Parameters:
        None

    Returns:
        country_code_countries: dict with country codes and countries
    '''

    print('Get country code countries')
    country_code_countries = {}
    url = 'https://www.payscale.com/research/Country'

    time.sleep(SLEEP_TIME)
    print('Connecting to {}'.format(url))
    browser = webdriver.Firefox()
    browser.get(url)
    #print(browser.title)

    if 'PayScale' in browser.title:
        print('Extract country code')
        time.sleep(SLEEP_TIME)
        element = browser.find_element(by=By.XPATH, value = '/html/body/div[1]/div/div[2]/div/div[3]/div')
        inner_html = element.get_attribute('innerHTML')

        inner_html = inner_html.replace('<div class="location__col location__col--full"><a href="', '')
        href_locations = list(inner_html.split('</a></div>'))

        for href_location in href_locations:
            if len(href_location) > 0:
                href_location = href_location.split('/Salary')[0]
                href_location = href_location.replace('/research/', '')
                country_code, country = href_location.split('/Country=')
                country_code_countries[country_code] = country
            else:
                pass

        #print(country_code_countries)

        time.sleep(SLEEP_TIME)
        print('Close the browser')
        browser.quit()
    else:
        print('Error: another page was expected')

    return country_code_countries


def get_salary(country, job):
    '''
    Scrape salaty from web page

    Parameters:
        country: Country to search
        job: job name to search

    Returns:
        salary: salary
    '''
    
    print('Get salary')
    salary = None
    base_url = 'https://www.payscale.com/research/_COUNTRY_CODE_/Job=_JOB_NAME_/Salary'

    country = country.replace(' ', '_')
    job = job.replace(' ', '_')

    print('Creating folders if needed')
    if os.path.isdir('data') is False:
        os.mkdir('data')
    else:
        pass

    country_code = _get_country_code(country)

    if country_code is None:
        print('Error: country code not found for {}'.format(country))
    else:
        url = base_url.replace('_COUNTRY_CODE_', country_code).replace('_JOB_NAME_', job)

        time.sleep(SLEEP_TIME)
        print('Connecting to {}'.format(url))
        browser = webdriver.Firefox()
        browser.get(url)
        #print(browser.title)

        if 'PayScale' in browser.title:
            print('Extract salary')
            time.sleep(SLEEP_TIME)
            element = browser.find_element(by = By.CLASS_NAME, value = 'paycharts__value')
            salary = element.text
            salary = salary.replace(',', '')

            #print(salary)

        else:
            print('Error: another page was expected')

        print('Close the browser')
        time.sleep(SLEEP_TIME)
        browser.quit()

    return salary


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=  'Extract data')
    parser.add_argument('--country', type = str, default = 'Italy', help = 'Country to search')
    parser.add_argument('--job', type = str, default = 'Data Engineer', help = 'Job to search')

    args = parser.parse_args()
    # print(args)

    country = args.country
    job = args.job

    print(get_salary(country, job))
else:
    pass