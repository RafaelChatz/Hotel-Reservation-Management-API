# Hotel-Reservation-Management-API

A RESTful API for managing hotels, customers, and reservations. 

## Table of Contents
- Features
- Architecture
- Design Decisions
- Tech Stack
- Getting Started
- Testing
- API Documentation
- API Endpoints
- Business Rules
- SQL Queries
- Postman
- Assumptions

## Features

Key features include:

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
- Interactive Swagger/OpenAPI documentation
- Postman collection testing every endpoint
- Unit tests for service layer

## Architecture

The application follows a layered architecture:

Routes
    ↓
Services
    ↓
Repositories
    ↓
PostgreSQL

- Routes handle HTTP requests and responses.
- Services contain business rules and validations.
- Repositories encapsulate database access.

## Design Decisions

- Layered architecture (Routes → Services → Repositories)
- Soft deletion for hotels
- Logical cancellation for reservations
- SQLAlchemy ORM
- Marshmallow validation
- PostgreSQL as primary database

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

### Install and run locally

Clone the project

```bash
git clone https://github.com/RafaelChatz/Hotel-Reservation-Management-API.git
```

Go to the project directory

```bash
  cd Hotel-Reservation-Management-API
```

Create the environment file: Create a `.env` file based on `.env.example`.

Start the containers

```bash
  docker compose up --build -d
```

Run database migrations

```bash
  docker compose exec backend flask --app run.py db upgrade
```

Populate Database

```bash
  docker exec -i postgres_hotel_db psql -U postgres -d hotel_db < database\seed.sql
```

Access home page: http://localhost:5000/


## Testing

Run all unit tests:
```bash
docker compose exec backend python -m pytest
```

## API Documentation

Swagger UI is available after starting the application:

http://localhost:5000/apidocs

## API Endpoints

### Hotels
- GET           /hotels
- GET           /hotels/<id>
- POST          /hotels
- PUT           /hotels/<id>
- DELETE        /hotels/<id>

### Customers
- GET           /customers
- GET           /customers/<id>
- POST          /customers

### Reservations
- GET           /reservations
- GET           /reservations/<id>
- POST          /reservations
- DELETE        /reservations/<id>


- GET           /reservations/search
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

## Postman

The project includes a postman collection that test every endpoint

Location:

postman/

## Assumptions

The following assumptions were made where the requirements did not provide explicit details:

- Database IDs use `BIGINT` with auto-generated values through database identity columns.
- Hotel names are stored as strings with a maximum length of 150 characters.
- Flask-Migrate (Alembic) was chosen because it is the standard migration tool for Flask applications using SQLAlchemy
- Prices will allow 0 values for free reservations(promotions, complimentary stays etc.)
- Newly created reservations have a default status of `ACTIVE`.
- Customer email addresses have a maximum length of 254 characters, following RFC 5321.
- Soft deleted hotels are not shown, but deleted reservations (`CANCELLED`) are shown.
- The date_removed value in hotels cannot be changed with PUT and POST request.
- Cancelled reservations remain available for reporting and historical purposes.