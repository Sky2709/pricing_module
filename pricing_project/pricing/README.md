# Pricing Module

Django-based configurable pricing module with differential pricing capabilities.

## Features
- Configurable pricing rules via Django Admin
- Day-based differential pricing
- Time and distance-based calculations
- Audit logging for configuration changes
- REST API for price calculations

## Setup

1. Create virtual environment:
python -m venv venv
source venv/bin/activate


2. Install Dependencies
pip install -r requirements.txt

3. Run Migrations
python manage.py migrate

4. Create superuser:
python manage.py createsuperuser

5. Run server:
python manage.py runserver

Usage
Admin: http://localhost:8000/admin

API: POST to http://localhost:8000/pricing/api/calculate-price/
with JSON body:

json
{
    "distance": 5.2,
    "total_ride_time": 75,
    "waiting_time": 10,
    "day_of_week": 2
}


Testing
python manage.py test pricing


