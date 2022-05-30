# Configuration
#
# python configuration.py

EXTERNAL_STYLESHEETS = [
    'https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css',
    {
        'href': 'https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css',
        'rel': 'stylesheet',
        'integrity': 'sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u',
        'crossorigin': 'anonymous'
    },
    'https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap-theme.min.css',
    {
        'href': 'https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap-theme.min.css',
        'rel': 'stylesheet',
        'integrity': 'sha384-rHyoN1iRsVXV4nD0JutlnGaslCJuC7uwjduW9SVrLvRYooPp2bWYgmgJQIXwl/Sp',
        'crossorigin': 'anonymous'
    }
]

DATA_FOLDER = 'data'
SEARCH_FOLDER = 'search'
COUNTRY_JOB_SALARY_FILENAME = 'country_job_salary.csv'
COUNTRY_JOB_SALARY_TRANSFORMED_FILENAME = COUNTRY_JOB_SALARY_FILENAME.replace('.csv', '_transformed.csv')
COUNTRIES_FILENAME = 'countries.csv'
JOBS_FILENAME = 'jobs.csv'
DATETIME_FORMAT = '%Y%m%dT%H%M%SZ'
DEAFULT_COUNTRY_SEARCH = ['Italy', 'Germany', 'Spain', 'United States', 'Switzerland', 'Pluto']
DEAFULT_JOB_SEARCH = ['Data Engineer', 'Data Scientist', 'Embedded Software Engineer', 'Pippo']
COUNTRY_CODE_COUNTRIES_FILENAME = 'country_code_countries.pk'
SLEEP_TIME = 5


if __name__ == '__main__':
    pass
else:
    pass