
set-env:
    export DB_NAME=app-db
    export DB_USER=postgres
    export DB_PASSWORD=secret
    export DB_HOST=localhost
    export DB_PORT=5432


create-migrations:
	python manage.py makemigrations weather

migrate:
	python manage.py migrate

run:
	python manage.py runserver
src:
	source venv/bin/activate

startapp:
	python manage.py startapp task