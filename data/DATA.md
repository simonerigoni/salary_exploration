# Salary exploration

## Data

This folder contains the data used by the project. It is public salary data scraped from [payscale.com](https://www.payscale.com/) and contains no personal information.

Using the url `https://www.payscale.com/research/IT/Job=Data_Engineer/Salary` we can see that it is possible to automatically search the website by providing a country code and a job name. After searching for each country and each job, the salary is converted from local currency to a common one (Euro).

All CSV files are UTF-8 encoded.

### Files

- `country_code_countries.pk`: pickled Python dict that maps Payscale country codes to country names as Payscale writes them, with underscores instead of spaces (for example `{"IT": "Italy", "US": "United_States"}`). It is a cache: if it is missing, it is scraped again from the Payscale country list.
- `YYYYMMDDTHHMMSSZ/`: one folder per exploration, named after its UTC start time. Each folder contains:
  - `countries.csv`: the countries searched (column `Country`).
  - `jobs.csv`: the jobs searched (column `Job`).
  - `country_job_salary.csv`: the salary found for each country and job, in local currency (columns `Country`, `Job`, `Salary`). The salary is empty or `None` when Payscale has no result.
  - `country_job_salary_transformed.csv`: the same salaries converted to Euro, without the rows that have no salary (columns `Country`, `Job`, `Local Currency Salary`, `Euro Salary`).

### Explorations

| Folder | Countries | Jobs | Notes |
| --- | --- | --- | --- |
| `20220529T102956Z` | Italy, Germany, Spain, United States, Switzerland, Pluto | Data Engineer, Data Scientist, Embedded Software Engineer, Pippo | Pluto and Pippo are deliberate unknown values to test missing results |
| `20220530T195841Z` | Italy, Germany, Spain, France, Portugal, Greece | Data Engineer, Data Scientist, Data Analyst | |
| `20250519T153216Z` | Italy, Germany | Data Engineer, Data Scientist | Same salaries as `20250519T161156Z` |
| `20250519T161156Z` | Italy, Germany | Data Engineer, Data Scientist | |
| `20260310T115628Z` | Italy, Germany | Data Engineer, Data Scientist | |
