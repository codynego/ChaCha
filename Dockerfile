FROM django:1.8-python2


ENV DJANGO_SETTINGS_MODULE=mysite.settings
ENV DJANGO_SECRET_KEY=secret
ENV DJANGO_ALLOWED_HOSTS=[]
ENV MYSQL_ROOT_PASSWORD=root
ENV MYSQL_DATABASE=chacha
ENV MYSQL_USER=nego
ENV MYSQL_PASSWORD=2499768

RUN apt-get update && apt-get install -y \
    mysql-server \
    mysql-client \
    libmysqlclient-dev \
    vim \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir /code
WORKDIR /code

COPY requirements.txt /code/
RUN pip install -r requirements.txt

COPY . /code/


CMD ["python", "manage.py", "runserver"]