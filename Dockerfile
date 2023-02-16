FROM python:3.11.2-alpine

WORKDIR /saveit

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

COPY old/requirements.txt /saveit

RUN pip install -r requirements.txt && \
    rm -rf /var/lib/apt/lists/*

COPY . /saveit

RUN python manage.py makemigrations && \
    python manage.py migrate && \
    pytest > log.txt && \
    python scripts.py >> log.txt

EXPOSE 8000

ENTRYPOINT cat log.txt && python manage.py runserver 0.0.0.0:8000