# Currency Conversion API

## Overview

This project is a FastAPI application designed to provide an API for currency conversion. It allows users to obtain current currency rates, update these rates from an external source, and perform currency conversion between any two given currencies.

## Features

- Fetch current exchange rates from an external API and store them in a PostgreSQL database.
- Display the date and time of the last update of the exchange rates.
- Convert amounts from one currency to another based on the latest rates.

## Technologies

- **FastAPI**: For creating the RESTful API.
- **SQLAlchemy**: For ORM support.
- **Alembic**: For database migrations.
- **Docker and Docker-Compose**: For containerization and orchestration.

## Getting Started

### Prerequisites

- Docker
- Docker Compose

### Installation

1. **Clone the Repository**

   ```sh
   git clone https://github.com/ArtemHorik/CurrencyAPI.git
   cd CurrencyAPI
   ```
2. **Environment Setup**

   Before building and running the application, create a `.env` file in the root directory of the project with the following content:

   ```plaintext
   # Docker PostgreSQL Database
   DATABASE_URL="postgresql+asyncpg://postgres:postgres@db/api_db"

   # API Key for External Exchange Rates API
   API_KEY="YOUR EXCHANGERATES API KEY"
   ```

   Replace `"YOUR EXCHANGERATES API KEY"` with your actual API key from the https://exchangeratesapi.io/.

3. **Build and Run with Docker Compose**

   ```sh
   docker-compose up --build -d
   ```

This command builds the application and starts PostgreSQL database.

Now you can access the api from your localhost on port 8000 as specified in docker-compose.yml.

### Using the API

Once the application is running, you can interact with the API using the following endpoints:

- **Update Exchange Rates**: `POST /update-rates`
  
  Fetches the latest exchange rates from the external API and updates the database.
  
  **Example Response**:
  ```json
  {
    "message": "Exchange rates updated successfully."
  }
  ```


- **Get Currencies List**: `POST /currencies`
  
  Returns a list of all the currencies from the database. (Base currency in EUR)
  
  **Example Response**
  ```json
  [
    {
        "rate": 3.970735,
        "code": "AED",
        "name": "United Arab Emirates Dirham"
    },
    {
        "rate": 1.081075,
        "code": "USD",
        "name": "United States Dollar"
    },
    {
        "rate": 1,
        "code": "EUR",
        "name": "Euro"
    }, ...
  ]
  ```

- **Last Update Time**: `GET /last-update-time`
  
  Returns the date and time of the last successful update of exchange rates. (UTC)
  
  **Example Response**:
  ```json
  {
    "last_update_time": "20-Feb-2024 20:33"
  }
  ```


- **Convert Currency**: `GET /convert?source=USD&target=EUR&amount=100`
  
  Converts an amount from the source currency to the target currency. Replace `USD`, `EUR`, and `100` with your desired source currency, target currency, and amount.
  
  **Example Response**:
  ```json
  {
    "converted_amount": 85.34
  }
  ```


### Documentation

- **Swagger UI**: Access the auto-generated Swagger documentation at `http://localhost:8000/docs`.
- **ReDoc**: Access the ReDoc documentation at `http://localhost:8000/redoc`.


## Database Migration Documentation

### Overview

This project uses Alembic for database migration management to handle changes to the database schema. Migrations ensure that the database schema is correctly aligned with the current state of the application models.

### Automatic Migration on Startup

When the project is started using `docker-compose up`, it automatically applies any pending migrations to the database. This ensures that the database schema is always up to date with the application's requirements.

### Running Migrations Manually

Although migrations are applied automatically at startup, you may find yourself needing to manage migrations manually (e.g., creating new migrations or applying specific migrations). Here's how to do it:

1. **Creating a New Migration**

   If you've made changes of SQLAlchemy models that require a change in the database schema, you can generate a new migration script with:

   ```sh
   docker-compose exec app alembic revision --autogenerate -m "Description of changes"
   ```

2. **Applying Migrations**

   To apply the latest migrations manually, use:

   ```sh
   docker-compose exec app alembic upgrade head
   ```

3. **Rolling Back Migrations**

   If you need to revert the most recent migration, you can do so with:

   ```sh
   docker-compose exec app alembic downgrade -1
   ```
