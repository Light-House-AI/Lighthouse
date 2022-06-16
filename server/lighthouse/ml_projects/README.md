# ML Projects service

## Generating new migration scripts

Make sure you have the latest version of the schema:

```
alembic -c lighthouse/ml_projects/db/migrations/alembic.ini upgrade head
```

Run the following command to generate the migration scripts:

```
alembic -c lighthouse/ml_projects/db/migrations/alembic.ini revision --autogenerate -m <MIGRATION_MESSAGE>
```

## Seeding the database

The seeder module helps you seed the database with data.

```bash
cd server
python -m lighthouse.ml_projects.db.seeder

# you can force the seeder to run by passing the --force flag
# this will delete all data in the database and seed it again
# use this with caution
python -m lighthouse.ml_projects.db.seeder --force=True
```

## Running the server

```bash
cd server
start.sh # or start.bat for windows
```

## Checking the documentation

Go to http://localhost:8000/api/v1/docs, and you should see the documentation.
You can also check the _redoc_ documentation in the browser by going to http://localhost:8000/api/v1/redoc/

You can also import he postman collection for the API. You can find it in the `docs` folder.
