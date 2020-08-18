# FastAPI + React.js + PostgreSQL
A boilerplate application code using FastAPI, ReactJS and PostgreSQL

## Structure
The backend is a RESTful API application built in FastAPI and a PostgreSQL database. The frontend will be a React.js web application.

## Usage

### With docker-compose
To run the application you need to have `Docker` and `docker-compose` installed. So, just execute from the root directory:

```bash
docker-compose up -d
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
