FROM python:3.8-slim

ENV DJANGO_SECRET_KEY=secret
ENV DJANGO_ALLOWED_HOSTS=[]
ENV MYSQL_ROOT_PASSWORD=${MYSQL_ROOT_PASSWORD}
ENV MYSQL_DATABASE=${MYSQL_DATABASE}
ENV MYSQL_USER=${MYSQL_USER}
ENV MYSQL_PASSWORD=${MYSQL_PASSWORD}

# Install the specific Python version required by your project
RUN apt-get update \
    && apt-get install -y python3.8 \
    && apt-get clean \
    && ln -s /usr/bin/python3.8 /usr/local/bin/python

RUN mkdir /code
WORKDIR /code

RUN pip install --upgrade pip
RUN pip install pipenv

COPY Pipfile Pipfile.lock /code/
# Specify the Python version before running pipenv install
RUN pipenv --python /usr/local/bin/python3.8 install --deploy --ignore-pipfile

COPY . /code/

RUN python manage.py migrate
RUN python manage.py collectstatic --noinput
RUN python manage.py runcrons

CMD ["python", "manage.py", "runserver"]
