# Pricing API
## Overview
This project provides a REST API for retrieving AWS RDS pricing data from [AWS RDS Pricing Documentation](https://sleakops-interview-tests.s3.us-east-1.amazonaws.com/rds_us_east_1_pricing.json), filtering by various attributes, handling different contract types, and automating data ingestion from an external JSON source into a PostgreSQL database. The API allows adding, deleting, and modifying contract types for a specific product using the SKU as an identifier as well.

The System Architecture Documentation can be found in the `docs` folder.
## Installation and Setup
### Prerequisites
* Docker and Docker Compose installed.
### Steps to Run
1. Create and activate a conda environment
```
conda create --name sk_challenge python=3.12.2 -y
conda activate sk_challenge
```
2. Clone the repository:
```
git clone https://github.com/GabrielCrisnejo/sleakops_challenge.git
cd sleakops_challenge
```
3. Start the services with Docker Compose
```
docker-compose up --build
```
What happens when running `docker-compose up --build`?

3.1 Database Container (`db`):
* Starts a PostgreSQL 17.4 container.
* Creates the database using credentials from `.env`.
* Runs a health check using `pg_isready` to ensure the database is ready before other services start.
* Persists data using a Docker volume.

3.2 Migrations Container (`migrations`):
* Waits until the database is healthy.
* Runs Alembic migrations to ensure the database schema is up to date.
* Exits upon successful migration.

3.3 API Container (`api`):
* Waits for the migrations to complete.
* Starts the FastAPI application.
* Exposes the API on port `8000.`
* Reads and writes data to the PostgreSQL database.

3.4 Scheduler Container (`scheduler)`:
* Waits for the database and migrations to complete.
* Runs a CRON job that periodically triggers data fetching and loading. Default at 3am every day.

## Endpoints
- `GET /pricing_data`: Retrieves processed pricing data.

For an example of how to query pricing data, check the `example` folder:
```
python example/api_filters_check.py
```
- `POST /skus/{sku}/terms/`: Creates a pricing term for a specific SKU.
- `PUT /skus/{sku}/terms/{term_type}`: Updates an existing pricing term.
- `DELETE /skus/{sku}/terms/{term_type}`: Deletes a pricing term.

Request Body:
```
{
  "termType": "Reserved",
  "leaseContractLength": "2yr",
  "purchaseOption": "Partial Upfront"
}
```
See the `tests` folder for details.
## Running Tests
The project includes a robust testing setup using `pytest`, `TestClient` from FastAPI, and `testcontainers` for database isolation.

### Testing Approach
* `TestClient`: Used to simulate API calls and validate responses without needing to run the server separately.
* `Testcontainers`: Runs a temporary PostgreSQL container to provide an isolated test environment, ensuring consistency between tests and the production database.
* `Fixtures`: `pytest` fixtures initialize the database, insert test data, and provide a test client instance.

To run the test suite, use
```
pytest -v
```