#!/bin/bash

echo "Running Migrations..."
python manage.py migrate

# Command 2
echo "Collecting Static Files..."
python manage.py collectstatic --noinput

# Command 3
echo "running cron jobs..."
python manage.py runcrons


# Command 3
echo "Starting Server..."
gunicorn -w 4 -k uvicorn.workers.UvicornWorker your_project.asgi:application