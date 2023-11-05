FROM django:latest


ENV DJANGO_SECRET_KEY=secret
ENV DJANGO_ALLOWED_HOSTS=[]
ENV MYSQL_ROOT_PASSWORD=${MYSQL_ROOT_PASSWORD}
ENV MYSQL_DATABASE=${MYSQL_DATABASE}
ENV MYSQL_USER=${MYSQL_USER}
ENV MYSQL_PASSWORD=${MYSQL_PASSWORD}

RUN mkdir /code
WORKDIR /code

COPY requirements.txt /code/
RUN apt-get update && sudo apt-get upgrade
RUN apt-get install python3.9
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . /code/


RUN python manage.py migrate
RUN python manage.py collectstatic --noinput
RUN python manage.py runcrons



CMD ["python", "manage.py", "runserver"]
