# Scrape salary data
#
# python salary_exploration.py 20220529T121639Z


import os
import argparse
import datetime
import pandas as pd

import extract_data
import transform_data


DATETIME_FORMAT = '%Y%m%dT%H%M%SZ'
DEAFULT_COUNTRY_SEARCH = ['Italy', 'Czech Republic', 'Germany', 'Spain', 'United States', 'Switzerland', 'Pluto']
DEAFULT_JOB_SEARCH = ['Data Engineer', 'Data Scientist', 'Embedded Software Engineer', 'Pippo']


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=  'Salary Exploration')
    parser.add_argument('--date_string', default = datetime.datetime.now().strftime(DATETIME_FORMAT), help = 'Date in format YYYYMMMDDTHHMMSSZ')

    args = parser.parse_args()
    # print(args)

    date_string = args.date_string

    try:
        date_datetime = datetime.datetime.strptime(date_string, DATETIME_FORMAT)

        country_code_countries = {}

        print('Creating folders if needed')
        if os.path.isdir('data') is False:
            os.mkdir('data')
        else:
            pass

        if os.path.isdir('search') is False:
            os.mkdir('search')
        else:
            pass

        if os.path.isdir('data/' + date_string) is False:
            os.mkdir('data/' + date_string)
        else:
            pass

        if os.path.isfile('data/' + date_string + '/country_job_salary.csv') is False:
            print('Read countries to search')

            if os.path.isfile('search/countries.csv') is False:
                df = pd.DataFrame(DEAFULT_COUNTRY_SEARCH, columns = ['Country'])
                df.to_csv('search/countries.csv', index=False)
                
            else:
                pass

            df_search_countries = pd.read_csv('search/countries.csv')
            list_search_countries = df_search_countries['Country'].values.tolist()

            print('Read jobs to search')

            if os.path.isfile('search/jobs.csv') is False:
                df = pd.DataFrame(DEAFULT_JOB_SEARCH, columns = ['Job'])
                df.to_csv('search/jobs.csv', index=False)
                
            else:
                pass

            df_search_jobs = pd.read_csv('search/jobs.csv')
            list_search_jobs = df_search_jobs['Job'].values.tolist()

            print('Write salary informations in {}'.format('data/' + date_string + '/country_job_salary.csv'))

            with open('data/' + date_string + '/country_job_salary.csv', 'w') as output_file:
                output_file.write('Country,Job,Salary\n')

                for country in list_search_countries:
                    for job in list_search_jobs:
                        output_file.write('{},{},{}\n'.format(country, job, extract_data.get_salary(country, job)))

            print('Move file {} in {}'.format('search/countries.csv', 'data/' + date_string + '/countries.csv'))
            os.rename('search/countries.csv', 'data/' + date_string + '/countries.csv')
        
            print('Move file {} in {}'.format('search/jobs.csv', 'data/' + date_string + '/jobs.csv'))
            os.rename('search/jobs.csv', 'data/' + date_string + '/jobs.csv')
        else:
            transform_data.normalize_salary('data/' + date_string + '/country_job_salary.csv')
           

    except ValueError:
        print('Error: incorrect date string format. It should be {}'.format(DATETIME_FORMAT))
else:
    pass