#!/bin/sh

# Run migrations
alembic -c lighthouse/ml_projects/db/migrations/alembic.ini upgrade head

# Run lighthouse server
python -m lighthouse