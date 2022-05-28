# Scrape data from https://www.payscale.com/research/IT/Job=Data_Engineer/Salary
#
# python extract_data.py

import argparse
import time
import selenium
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# from selenium.webdriver.support.select import Select
# # from selenium.webdriver.support.ui import WebDriverWait
# # from selenium.webdriver.common.by import By
# # from selenium.webdriver.support import expected_conditions as EC
# from bs4 import BeautifulSoup
# import pandas as pd


BASE_URL = 'https://www.payscale.com/research/_COUNTRY_CODE_/Job=_JOB_NAME_/Salary'
SLEEP_TIME = 5


def get_salary(country_code, job):
    '''
    Scrape salaty from web page

    Parameters:
        country_code: Country code to search
        job: job name to search with _ instead od spaces

    Returns:
        salary: salary
    '''

    url = BASE_URL.replace('_COUNTRY_CODE_', country_code).replace('_JOB_NAME_', job)

    time.sleep(SLEEP_TIME)
    print('Connecting to {}'.format(url))
    browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    browser.get(url)
    # #print(browser.title)
    # assert 'Agor' in browser.title

    # print('Selecting data for last 60 days')
    # time.sleep(SLEEP_TIME * 2)
    # select_period = browser.find_element_by_class_name('custom-select')
    # select_period = Select(select_period)
    # select_period.select_by_visible_text('Ultimi 60 giorni')

    # print('Extract data from totali table')
    # time.sleep(SLEEP_TIME * 2)
    # soup = BeautifulSoup(browser.page_source, 'lxml') # Selenium hands the page source to Beautiful Soup
    # voci = [element.text for element in soup.find_all('div', attrs = {'class':'col-md-5 col-sm-4 col-3'})]
    # #print(voci)
    # totali = [element.text for element in soup.find_all('div', attrs = {'class':'col-md-4 col-sm-4 col-4 dettaglio_consumi total-consumi'})]
    # #print(totali)
    # totals = pd.DataFrame({'Voci' : voci, 'Totali' : totali})
    # #print(totals)
    # totals.to_pickle('data/extracted/' + dt_string + '/totali.pickle')
    # #shutil.move('totals.pickle', 'data/extracted/' + dt_string + '/totals.pickle')
    # print('Save data from totali table in {}'.format('data/extracted/' + dt_string + '/totali.pickle'))

    # print('Extract data from soglie table')

    # # Open soglie table
    # time.sleep(SLEEP_TIME)
    # button_soglie = browser.find_element_by_id('link-soglie')
    # button_soglie.click()
    # #WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.ID, 'link-soglie'))).click()

    # # Extract data from soglie table
    # time.sleep(SLEEP_TIME)
    # data = []
    # table = soup.find('table')
    # table_body = table.find('tbody')
    # rows = table_body.find_all('tr')

    # for i in range(len(rows)):
    #     if i == 0:
    #         cols = rows[i].find_all('th')
    #     else:
    #         cols = rows[i].find_all('td')
    #     cols = [ele.text.strip() for ele in cols]
    #     data.append([ele for ele in cols if ele]) # Get rid of empty values

    # #print(data)
    # soglie = pd.DataFrame(data)
    # soglie.columns = soglie.iloc[0]
    # soglie = soglie.drop(soglie.index[0])
    # #print(soglie)
    # soglie.to_pickle('data/extracted/' + dt_string + '/soglie.pickle')
    # #shutil.move('soglie.pickle', 'data/extracted/' + dt_string + '/soglie.pickle')
    # print('Save data from soglie table in {}'.format('data/extracted/' + dt_string + '/soglie.pickle'))

    # time.sleep(SLEEP_TIME)
    # button_close = browser.find_elements_by_class_name('close')[1] # For soglie is the second one
    # button_close.click()

    # # Extract data for each voce

    # time.sleep(SLEEP_TIME)
    # a_tags = browser.find_elements_by_tag_name('a')
    # button_dettagli = []
    # for a_tag in a_tags:
    #     if 'DETTAGLI' in a_tag.text:
    #         button_dettagli.append(a_tag)
    # # button_dettagli = browser.find_elements_by_xpath("//section[@class='dettagli_traffico']//container//row//div[@class='col-md-10 col-sm-12']//row//div[@class='col-md-3 col-sm-4 col-5 text-right//a']")

    # #print(len(button_dettagli))

    # for j in range(len(button_dettagli)):
    #     print('Extract data from {} table'.format(voci[j]))

    #     #input("Enter to continue")

    #     time.sleep(SLEEP_TIME)
    #     button_dettagli[j].click()
    #     time.sleep(SLEEP_TIME)

    #     texts = []
    #     soup = BeautifulSoup(browser.page_source, 'lxml') # Selenium hands the page source to Beautiful Soup

    #     texts = [element.text for element in soup.find_all('div', attrs = {'class': 'modal-body'})]
    #     #print(texts)

    #     if 'Nessun consumo da visualizzare' in texts[0]:
    #         print('No data')
    #     else:
    #         table = soup.find('table')
    #         table_body = table.find('tbody')
    #         rows = table_body.find_all('tr')
    #         data = []

    #         for i in range(len(rows)):
    #             if i == 0:
    #                 cols = rows[i].find_all('th')
    #             else:
    #                 cols = rows[i].find_all('td')
    #             cols = [ele.text.strip() for ele in cols]
    #             data.append([ele for ele in cols if ele]) # Get rid of empty values

    #         #print(data)
    #         dettaglio = pd.DataFrame(data)
    #         dettaglio.columns = dettaglio.iloc[0]
    #         dettaglio = dettaglio.drop(dettaglio.index[0])
    #         #print(dettaglio)
    #         dettaglio.to_pickle('data/extracted/' + dt_string + '/dettaglio_' + voci[j].replace(' ', '_').lower() + '.pickle')
    #         print('Save data from {} table in {}'.format(voci[j], 'data/extracted/' + dt_string + '/dettaglio_' + voci[j].replace(' ', '_').lower() + '.pickle'))

    #     time.sleep(SLEEP_TIME)
    #     button_close = browser.find_elements_by_class_name('close')[0] # For dettaglio is the first one
    #     button_close.click()

    print('Close the browser')
    time.sleep(SLEEP_TIME)
    browser.quit()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=  'Extract data')
    parser.add_argument('--country_code', type = str, default = 'IT', help = 'Country code to search')
    parser.add_argument('--job', type = str, default = 'Data_Engineer', help = 'Job to search (use _ instead of space)')

    args = parser.parse_args()
    # print(args)

    country_code = args.country_code
    job = args.job

    print(get_salary(country_code, job))
else:
    pass