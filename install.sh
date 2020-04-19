mkdir -p logs
docker-compose build
docker-compose run django /app/manage.py makemigrations
docker-compose run django /app/manage.py migrate
docker-compose run django /app/importcsv.py
docker-compose run django /app/manage.py createsuperuser