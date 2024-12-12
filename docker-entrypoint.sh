#!/bin/bash


python -m src.core.utils.form_templates
gunicorn src.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000
