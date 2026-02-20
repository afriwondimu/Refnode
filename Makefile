.PHONY: help install run migrate makemigrations

help:
	@echo "Available commands:"
	@echo "  make install        - Install dependencies"
	@echo "  make run            - Run development server"
	@echo "  make migrate        - Apply migrations"
	@echo "  make makemigrations - Create new migration"

install:
	@echo "Installing dependencies..."
	pip install -r requirements.txt

run:
	@echo "Starting server..."
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

migrate:
	@echo "Applying migrations..."
	alembic upgrade head

makemigrations:
	@echo "Creating new migration..."
	alembic revision --autogenerate -m "$(message)"