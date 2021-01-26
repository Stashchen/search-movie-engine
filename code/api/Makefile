migrate: 
	python src/manage.py migrate
makemigrations:
	python src/manage.py makemigrations
loaddata:
	python src/manage.py loaddata $(file_name)	
initialize:
	python src/manage.py makemigrations api movie_site
	python src/manage.py migrate
	python src/manage.py loaddata initial_data.json
	python src/manage.py etl
