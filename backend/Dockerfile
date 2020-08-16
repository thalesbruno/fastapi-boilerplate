FROM python:3.8
COPY . /usr/src/app
WORKDIR /usr/src/app
RUN ["pip", "install", "-r", "requirements.txt"]
EXPOSE 8000
ENTRYPOINT [ "uvicorn", "main:app", "--host", "0.0.0.0", "--reload" ]