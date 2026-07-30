# Hotel-Reservation-Management-API

Internal service for managing hotels, customers, reservations, cancellations, searches, and reservation reports.

## Running with Docker

Create a `.env` file based on `.env.example`.

Start the application:

docker compose up --build -d

Run migrations:

docker compose exec backend flask --app run.py db upgrade

The API will be available at:

http://localhost:5000

## Features

Currently implemented:

- Flask application setup
- PostgreSQL database integration
- Database migrations using Flask-Migrate and Alembic
- Dockerized development environment
- Separate containers for:
- Flask backend API
- PostgreSQL database
- Environment-based configuration using `.env` files
- Added Hotel table

## Current Tech Stack

### Backend

- Python 3.12
- Flask
- Flask-SQLAlchemy
- Flask-Migrate
- Alembic

### Database

- PostgreSQL 16
- SQLAlchemy ORM

### Infrastructure

- Docker
- Docker Compose

## Assumptions

The following assumptions were made where the requirements did not provide explicit details:

- Database IDs use `BIGINT` with auto-generated values through database identity columns.
- Hotel names are stored as strings with a maximum length of 150 characters.
- Flask-Migrate (Alembic) was chosen because it is the standard migration tool for Flask applications using SQLAlchemy
- Prices will allow 0 values for free reservations(promotions, complimentary stays etc.)
- Newly created reservations have a default status of `ACTIVE`.
- Customer email addresses have a maximum length of 254 characters, following RFC 5321.