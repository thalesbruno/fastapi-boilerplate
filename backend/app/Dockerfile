FROM python:3.8
COPY . /app
WORKDIR /app
RUN pip install -r requirements/dev.txt
EXPOSE 8000
ENTRYPOINT ["uvicorn", "main:app", "--host", "0.0.0.0", "--reload"]