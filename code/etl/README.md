# ETL script
Extract Transform Load script for data from PostgreSQL to ElasticSearch

# Usage
Open your PostgreSQL instance `sudo su - postgres` and run at the begining `gen_database.sql` script `psql -f path/to/gen_database.sql` and then execute `insert.sql` script with command `psql -f path/to/insert.sql`. Afther that you will allow acces to your database and data.
Create file with name `.env` with next structure:

```bash
DB_NAME = "yandex_db"
USER_DB = "postgres"
PASSWORD_DB = "postgres"
HOST_DB = "localhost"
PORT_DB = "5432"
```

In the `ETL_script.py` change `BASE_URL` to your URL where your ElasticSearch server run.

```py
...
BASE_URL = 'http://127.0.0.1:9200'
...
```

And at the last step run `ETL_script.py`.

