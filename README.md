# Hotel-Reservation-Management-API

A RESTful API for managing hotels, customers, and reservations. 
The application supports reservation creation,hotel creation, hotel update, hotel soft deletion, logical cancellation and searching

## Table of Contents
- Features
- Tech Stack
- Getting Started
- API Endpoints
- Business Rules
- SQL Queries
- Assumptions

## Features

Currently implemented:

- Hotel CRUD operations
- Customer CRUD operations
- Reservation CRUD operations
- Reservation search endpoint
- Reservation reports
- Soft delete for hotels
- Logical cancellation for reservations
- Global exception handling
- Request validation using Marshmallow
- PostgreSQL database integration
- Database migrations using Flask-Migrate (Alembic)
- Dockerized development environment
- Database seed script
- Standalone SQL query solutions

## Tech Stack

### Backend

- Python 3.12
- Flask
- Flask-SQLAlchemy
- Flask-Migrate
- Alembic
- Marshmallow

### Database

- PostgreSQL 16
- SQLAlchemy ORM

### Infrastructure

- Docker
- Docker Compose

## Getting Started

### Prerequisites

- Docker
- Docker Compose

### Installation

1. Create the environment file: Create a `.env` file based on `.env.example`.
2. Start the containers: docker compose up --build -d
3. Run database migrations: docker compose exec backend flask --app run.py db upgrade
4. Populate Database:
        Windows PowerShell : Get-Content database\seed.sql | docker exec -i postgres_hotel_db psql -U postgres -d hotel_db
        Linux / macOS: docker exec -i postgres_hotel_db psql -U postgres -d hotel_db < database\seed.sql
5. Access the API: http://localhost:5000

6. Test by running: docker compose exec backend python -m pytest

## API Endpoints

### Hotels
- GET /hotels
- GET /hotels/<id>
- POST /hotels
- PUT /hotels/<id>
- DELETE /hotels/<id>

### Customers
- GET /customers
- GET /customers/<id>
- POST /customers

### Reservations
- GET /reservations
- GET /reservations/<id>
- POST /reservations
- DELETE /reservations/<id>

### Search
GET /reservations/search

#### Parameters
- hotelName -– Filters reservations by hotel name (partial, case-insensitive match).
- customerName -- Filters reservations by the customer's full name (partial, case-insensitive match).
- city -- Filters reservations by hotel city (partial, case-insensitive match). 
- status -- Filters reservations by reservation status (ACTIVE or CANCELLED).
- checkIn -– Returns reservations with a check-in date on or after the specified date.
- checkOut -- Returns reservations with a check-out date on or before the specified date.

## Business rules

- Hotel stars must be between 1 and 5.
- Customer email addresses must be unique.
- Reservation price cannot be negative.
- Check-out date must be after check-in.
- Customers cannot have overlapping active reservations.
- Hotels are soft deleted.
- Deleting a reservation performs a logical cancellation by changing its status to `CANCELLED`.
- Soft deleted hotels are excluded from API responses.
- Reservations belonging to deleted hotels are automatically cancelled.


## SQL Queries

The project includes standalone SQL solutions requested by the assignment.

Location:

database/sql_queries/

## Assumptions

The following assumptions were made where the requirements did not provide explicit details:

- Database IDs use `BIGINT` with auto-generated values through database identity columns.
- Hotel names are stored as strings with a maximum length of 150 characters.
- Flask-Migrate (Alembic) was chosen because it is the standard migration tool for Flask applications using SQLAlchemy
- Prices will allow 0 values for free reservations(promotions, complimentary stays etc.)
- Newly created reservations have a default status of `ACTIVE`.
- Customer email addresses have a maximum length of 254 characters, following RFC 5321.
- Soft deleted hotels are not shown, but deleted reservations (`CANCELLED`) are shown.
- The data_removed value in hotels cannot be changed with PUT and POST request.
- Cancelled reservations remain available for reporting and historical purposes.