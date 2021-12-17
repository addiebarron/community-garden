# Migrate models
python manage.py migrate

# Load initial data from JSON in /fixtures
python manage.py loaddata data.json

# Run workers in the background
python manage.py runworkers &

if [ $APP_ENV = "dev" ]; then
  python manage.py runserver 0.0.0.0:8000
else
  echo "Do something more production-y"
fi
