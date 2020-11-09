# simple-flask-server
API to retrieve simple aggregates from a Postgres database.

# APIs
### /median/< attribute >
Calculate the median across all values in a given numerical table column

# Pre-requsites
Run the Docker container defined here - https://github.com/Danny-AG/simple-docker-postgres-with-data-ingest

# Usage
Launch flask server:
``` python
python app.py <database-host> <database-port> <databasee-name> <user> <password> <table-to-aggregate>
```

Example server query:
``` bash
curl localhost:5000/median/height
```
