
import os
import argparse
import datetime
import shutil


DATETIME_FORMAT = '%Y%m%dT%H%M%SZ'


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=  'Extract data')
    parser.add_argument('--date_string', default = datetime.datetime.now().strftime(DATETIME_FORMAT), help = 'Date in format YYYYMMMDDTHHMMSSZ')
    parser.add_argument('--country_code', type = str, default = 'IT', help = 'Country code to search')
    parser.add_argument('--job', type = str, default = 'Data_Engineer', help = 'Job to search (use _ instead of space)')

    args = parser.parse_args()
    # print(args)

    date_string = args.date_string
    country = args.country_code
    job = args.job

    try:
        date_datetime = datetime.datetime.strptime(date, DATETIME_FORMAT)

        print('Creating folders if needed')
        if os.path.isdir('data') == False:
            os.mkdir('data')

        if os.path.isdir('data/extracted') == False:
            os.mkdir('data/extracted')

        if os.path.isdir('data/extracted/' + date_string) == True:
            shutil.rmtree('data/extracted/' + date_string)

        os.mkdir('data/extracted/' + date_string)



    except ValueError:
        print('Error: incorrect date string format. It should be {}'.format(DATETIME_FORMAT))