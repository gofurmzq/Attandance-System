FROM python:3.7.13-buster

WORKDIR /project

RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install psycopg2
RUN pip install --upgrade pip

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

CMD ["gunicorn", "-w 4", "-b", "0.0.0.0:5000", "app:app"]