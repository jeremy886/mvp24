#!/bin/bash

# Check for the correct number of arguments
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <environment>"
    echo "Where <environment> is 'development' or 'production'."
    exit 1
fi

# Set the DJANGO_SETTINGS_MODULE based on the argument
if [ "$1" == "development" ]; then
    export DJANGO_SETTINGS_MODULE='mvp24.settings.development'
elif [ "$1" == "production" ]; then
    export DJANGO_SETTINGS_MODULE='mvp24.settings.production'
else
    echo "Invalid environment: $1"
    echo "Please choose 'development' or 'production'."
    exit 1
fi

# Generate a new secret key
# echo "export SECRET_KEY='$(openssl rand -hex 40)'" > .DJANGO_SECRET_KEY
source .DJANGO_SECRET_KEY

# Print the settings being used
echo "Starting Django server with settings: $DJANGO_SETTINGS_MODULE"
echo "Using SECRET_KEY: $SECRET_KEY"

# Collect static files in production
if [ "$1" == "production" ]; then
    echo "Collecting static files..."
    python manage.py collectstatic --noinput
fi

# Start the server
# For development:
if [ "$1" == "development" ]; then
    python manage.py runserver
# For production, assuming you use gunicorn:
elif [ "$1" == "production" ]; then
    gunicorn -c config/gunicorn/prod.py
fi