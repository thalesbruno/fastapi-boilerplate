# FastAPI boilerplate (with PostgreSQL)
A boilerplate RESTFul application code using FastAPI and PostgreSQL

## Structure
The backend is a RESTful API application built in FastAPI and a PostgreSQL database.

## Usage

### With docker-compose
To run the application you need to have `Docker` and `docker-compose` installed. So, just execute from the root directory:

```bash
docker-compose up
```

#### Create the test_app database
The tests will fail at the first time we run `docker-compose up`, because the creation of `test_app` database is not present in the images build process. There's an [issue](https://github.com/thalesbruno/fastapi-boilerplate/issues/6) for fix this already.

At the moment, we need to execute the command below to create it
```docker
docker exec fastapi-boilerplate_db_1 psql -U app -c "create database test_app with owner app;"
```
To drop:
```docker
docker exec fastapi-boilerplate_db_1 psql -U app -c "drop database test_app;"
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
