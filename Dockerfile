FROM python:3.6.1

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

ADD ./requirements.txt /usr/src/app/requirements.txt
ADD . /usr/src/app

RUN pip install -r requirements.txt

CMD python manage.py runserver -h 0.0.0.0
