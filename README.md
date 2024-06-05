# Contractor invoices

A utility to work out the expected invoice amount for a set of contractors

## Getting started

Create a file called `docker.env` in the root of the project (this is not required for now, but any environment values would live here is required).

You will need to start the Docker container via compose:

```bash
docker compose run cli bash
```

This will drop you into the shell inside the container will all dependencies installed.

## Adding the data files

You will need to provide 2 data files in the `data` directory called `rates.csv` and `holidays.csv`.

These will need to conform to the following spec:

### rates.csv

This file will need the following columns (data type in _italics_):

- Employee Id _string_
- First Name _string_
- Last Name _string_
- Salary Amount _integer_
- Salary Effective Date _date_

With one employee (contractor) record per file

### holidays.csv

This file needs 2 columns (data type in _italics_):

- Employee Id _string_
- Holiday Duration (Days) _string_

The _Employee Id_ column value should match that of the `rates.csv` file.

This file can contain multiple rows for each employee if they have taken more than one holiday in the period.

Not every employee that appears in `rates.csv` needs to be rep esented in `holidays.csv`

### days.csv

This file needs 2 columns (data type in _italics_):

- Employee Id _string_
- Mon _boolean_
- Tue _boolean_
- Wed _boolean_
- Thu _boolean_
- Fri _boolean_

The days must be either `TRUE` or `FALSE` so that DuckDB can parse it as a boolean.

Not every employee that appears in `rates.csv` needs to be rep esented in `days.csv`.
If an employee is omitted from here, it is assumed that they work Monday to Friday.

## Running the CLI command

Ensuring that you are inside the container (see above), do:

```bash
# Inside the container
python ci/cli.py 2023 8
```

This will run the report for (in this case) August 2023.

## Making change to dependencies

If you need to add, remove or update any dependencies, do so in `requirements.txt` and then re-build the docker image with:

```bash
docker compose build cli
```
