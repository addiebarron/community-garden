python manage.py makemigrations
python manage.py migrate
python manage.py runworkers

if [ $APP_ENV = "dev" ]; then
  python manage.py runserver 0.0.0.0:8000
else
  echo "Do something more production-y"
fi
