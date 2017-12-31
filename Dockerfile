FROM tiangolo/uwsgi-nginx-flask:python3.6

RUN pip install flask-bootstrap
RUN pip install flask-socketio
RUN pip install requests
RUN pip install pandas
RUN pip install flask_wtf
RUN pip install flask-admin
RUN pip install babel
RUN pip install flask-babel
RUN pip install Flask-Session


COPY ./app /app
