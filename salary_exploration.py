# Scrape salary data
#
# python salary_exploration.py --date_string='20220530T103056Z'


import os
import argparse
import datetime
import pandas as pd


import extract_data
import transform_data

DATA_FOLDER = 'data'
SEARCH_FOLDER = 'search'
COUNTRY_JOB_SALARY_FILENAME = 'country_job_salary.csv'
COUNTRY_JOB_SALARY_TRANSFORMED_FILENAME = COUNTRY_JOB_SALARY_FILENAME.replace('.csv', '_transformed.csv')
COUNTRIES_FILENAME = 'countries.csv'
JOBS_FILENAME = 'jobs.csv'
DATETIME_FORMAT = '%Y%m%dT%H%M%SZ'
DEAFULT_COUNTRY_SEARCH = ['Italy', 'Germany', 'Spain', 'United States', 'Switzerland', 'Pluto']
DEAFULT_JOB_SEARCH = ['Data Engineer', 'Data Scientist', 'Embedded Software Engineer', 'Pippo']


def _create_folders(date_string):
    ''' 
    Creating folders if needed

    Parameters:
        date_string: Date in format YYYYMMMDDTHHMMSSZ

    Returns:
        None
    '''

    print('Creating folders if needed')
    if os.path.isdir(DATA_FOLDER) is False:
        os.mkdir(DATA_FOLDER)
    else:
        pass

    if os.path.isdir(SEARCH_FOLDER) is False:
        os.mkdir(SEARCH_FOLDER)
    else:
        pass

    if os.path.isdir(DATA_FOLDER + '/' + date_string) is False:
        os.mkdir(DATA_FOLDER + '/' + date_string)
    else:
        pass


def get_last_salary_exploration():
    ''' 
    Get country job salary transformed data. Based on https://stackoverflow.com/questions/2014554/find-the-newest-folder-in-a-directory-in-python
    
    Parameters:
        None
    Returns:
        date_string: last exploration date_string in format YYYYMMMDDTHHMMSSZ
    '''

    print('Get last salary exploration')
    latest_dir = ''
    all_dir = []

    for dir in os.listdir(DATA_FOLDER):
        if os.path.isdir(DATA_FOLDER + '/' + dir):
            all_dir.append(DATA_FOLDER + '/' + dir)
        else:
            pass

    if len(all_dir) == 0:
        pass
    else:
        latest_dir = max(all_dir, key = os.path.getmtime)
        latest_dir = latest_dir.split('/')[1]

    return latest_dir


def get_all_salary_exploration():
    ''' 
    Get date string of all salary exploration
    
    Parameters:
        None

    Returns:
        date_strings: all exploration date_string
    '''

    print('Get all salary exploration')
    all_dir = []

    for dir in os.listdir(DATA_FOLDER):
        if os.path.isdir(DATA_FOLDER + '/' + dir):
            all_dir.append(dir)
        else:
            pass

    return all_dir

    
def get_country_job_salary_transformed(date_string):
    ''' 
    Get country job salary transformed data
    
    Parameters:
        date_string: exploration date_string in format YYYYMMMDDTHHMMSSZ

    Returns:
        df: country job salary transformed data
    '''

    print('Get country job salary transformed')

    if date_string is None:
        date_string = get_last_salary_exploration()
    else:
        pass

    if os.path.isfile(DATA_FOLDER + '/' + date_string +  '/' + COUNTRY_JOB_SALARY_TRANSFORMED_FILENAME) is False:

        _do_salary_exploration()

        date_string = get_last_salary_exploration()

        transform_data.transform_salary(DATA_FOLDER + '/' + date_string +  '/' + COUNTRY_JOB_SALARY_FILENAME, DATA_FOLDER + '/' + date_string +  '/' + COUNTRY_JOB_SALARY_TRANSFORMED_FILENAME)
    else:
        pass

    df = pd.read_csv(DATA_FOLDER + '/' + date_string +  '/' + COUNTRY_JOB_SALARY_TRANSFORMED_FILENAME)

    return df


def _do_salary_exploration(date_string = datetime.datetime.now().strftime(DATETIME_FORMAT)):
    ''' 
    Do salary exploration
    
    Parameters:
        None
    Returns:
        None
    '''

    print('Do salary exploration')
    _create_folders(date_string)

    if os.path.isfile(DATA_FOLDER + '/' + date_string +  '/' + COUNTRY_JOB_SALARY_FILENAME) is False:
        print('Read countries to search')

        if os.path.isfile(SEARCH_FOLDER + '/' + COUNTRIES_FILENAME) is False:
            df = pd.DataFrame(DEAFULT_COUNTRY_SEARCH, columns = ['Country'])
            df.to_csv(SEARCH_FOLDER + '/' + COUNTRIES_FILENAME, index=False)
            
        else:
            pass

        df_search_countries = pd.read_csv(SEARCH_FOLDER + '/' + COUNTRIES_FILENAME)
        list_search_countries = df_search_countries['Country'].values.tolist()

        print('Read jobs to search')

        if os.path.isfile(SEARCH_FOLDER + '/' + JOBS_FILENAME) is False:
            df = pd.DataFrame(DEAFULT_JOB_SEARCH, columns = ['Job'])
            df.to_csv(SEARCH_FOLDER + '/' + JOBS_FILENAME, index=False)
            
        else:
            pass

        df_search_jobs = pd.read_csv(SEARCH_FOLDER + '/' + JOBS_FILENAME)
        list_search_jobs = df_search_jobs['Job'].values.tolist()

        print('Write salary informations in {}'.format(DATA_FOLDER + '/' + date_string +  '/' + COUNTRY_JOB_SALARY_FILENAME))

        with open(DATA_FOLDER + '/' + date_string +  '/' + COUNTRY_JOB_SALARY_FILENAME, 'w') as output_file:
            output_file.write('Country,Job,Salary\n')

            for country in list_search_countries:
                for job in list_search_jobs:
                    output_file.write('{},{},{}\n'.format(country, job, extract_data.get_salary(country, job)))

        print('Move file {} in {}'.format(SEARCH_FOLDER + '/' + COUNTRIES_FILENAME, DATA_FOLDER + '/' + date_string + '/' + COUNTRIES_FILENAME))
        os.rename(SEARCH_FOLDER + '/' + COUNTRIES_FILENAME, DATA_FOLDER + '/' + date_string + '/' + COUNTRIES_FILENAME)
    
        print('Move file {} in {}'.format(SEARCH_FOLDER + '/' + JOBS_FILENAME, DATA_FOLDER + '/' + date_string + '/' + JOBS_FILENAME))
        os.rename(SEARCH_FOLDER + '/' + JOBS_FILENAME, DATA_FOLDER + '/' + date_string + '/' + JOBS_FILENAME)
    else:
        pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=  'Salary Exploration')
    parser.add_argument('--date_string', default = datetime.datetime.now().strftime(DATETIME_FORMAT), help = 'Date in format YYYYMMMDDTHHMMSSZ')

    args = parser.parse_args()
    # print(args)

    date_string = args.date_string

    try:
        date_datetime = datetime.datetime.strptime(date_string, DATETIME_FORMAT)

        _do_salary_exploration(date_string)

        transform_data.transform_salary(DATA_FOLDER + '/' + date_string +  '/' + COUNTRY_JOB_SALARY_FILENAME, DATA_FOLDER + '/' + date_string +  '/' + COUNTRY_JOB_SALARY_TRANSFORMED_FILENAME)

    except ValueError:
        print('Error: incorrect date string format. It should be {}'.format(DATETIME_FORMAT))

    # print(get_last_salary_exploration())
else:
    pass