# sleakops_challenge
This project provides an API to fetch and manage AWS RDS pricing data for various database engines and instance types.

## Installation

1. Clone the repository
2. Build the Docker image: `docker-compose build`
3. Start the services: `docker-compose up`
4. The API will be available at `http://localhost:5000`.

## Endpoints

- `GET /api/pricing`: Fetch pricing data with optional filters (`databaseEngine`, `instanceType`, `vcpu`, `memory`).
- `POST /api/load-pricing`: Load pricing data from the JSON file into the database.

## Database

The database is a PostgreSQL instance. Use the Docker Compose setup to spin it up automatically.

## Tests

Unit tests can be written to verify the functionality of the API and database interactions.
