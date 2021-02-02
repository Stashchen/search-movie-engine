migrate: makemigrations
	python manage.py migrate

makemigrations:
	python manage.py makemigrations

loaddata:
	python manage.py loaddata $(file_name)

initialize:
	python manage.py makemigrations api
	python manage.py migrate
	python manage.py loaddata initial_data.json
	python manage.py etl

test:
	python manage.py test
	
coverage:
	@coverage run manage.py test api
	@coverage report -m
