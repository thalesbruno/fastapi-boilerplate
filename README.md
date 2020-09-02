# FastAPI boilerplate (with PostgreSQL)
![example workflow name](https://github.com/thalesbruno/fastapi-boilerplate/workflows/FastAPI%20Boilerplate%20Application/badge.svg)

A boilerplate RESTFul application code using FastAPI and PostgreSQL

## Structure
The backend is a RESTful API application built in FastAPI and a PostgreSQL database.

## Usage

### With docker-compose
To run the application you need to have `Docker` and `docker-compose` installed. So, just execute from the root directory:

```bash
docker-compose up
```

So, run the first migration:

```bash
docker exec fastapi-boilerplate_app_1 alembic upgrade head
```


### Tests

To re-run the tests, first of all, recreate the tests database:

Remove the data files before recreate the container
```
rm -fr db_data_test/*
```
Recreate the db_test service

```docker
docker-compose stop db_test
docker-compose rm db_test
docker-compose up -d db_test
```
Finally, restart the tests service
```
docker-compose restart tests
```

<!--
### With python virtual environment
If you want to run the application from your terminal, you may create a python virtual environment, install the dependencies and run it using uvicorn:

```bash
python3 -m venv .venv
source ./venv/bin/activate
(.venv) pip install -r requirements/dev.txt
(.venv) cd backend
(.venv) uvicorn main:app --reload
```
-->
