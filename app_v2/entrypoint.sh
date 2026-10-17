#!/bin/bash

cd backend/

export PYTHONPATH=$(pwd)

alembic upgrade head

uvicorn app.main:app --reload --host=0.0.0.0 --port=8000
