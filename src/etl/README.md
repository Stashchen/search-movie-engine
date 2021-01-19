# ETL scripts
Extract Transform Load script for data from PostgreSQL to ElasticSearch

# Usage
Open your psql and run at the begining `gen_database.sql` script and then execute `insert.sql` script. Afther that you will allow acces to your database and data
Create file with name `.env` with next structure:

```bash
DB_NAME = "yandex_db"
USER_DB = "postgres"
PASSWORD_DB = "postgres"
HOST_DB = "localhost"
PORT_DB = "5432"
```

And at the last step run `ETL_script.py`.

