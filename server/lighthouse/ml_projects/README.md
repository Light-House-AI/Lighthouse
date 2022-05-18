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
