#!/bin/bash

# Django database setup script

echo "Setting up Django database..."

# Run migrations
echo "Running migrations..."
python manage.py makemigrations
python manage.py migrate

# Create superuser (optional - comment out for automated setup)
# echo "Creating superuser..."
# python manage.py createsuperuser

echo "Database setup complete!"
echo "Run 'python manage.py runserver' to start the development server"
