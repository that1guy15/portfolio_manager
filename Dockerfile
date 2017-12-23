FROM tiangolo/uwsgi-nginx-flask:python3.6

RUN pip install flask-bootstrap

COPY ./app /app

