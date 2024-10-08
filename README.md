# Weather App

A Dockerized FastAPI-based weather application that allows users to add, retrieve, and update weather measurements, including temperature, humidity, wind speed, wind direction, and rainfall.

## Features

- **Create Measurements**: Add new weather data including temperature, humidity, wind speed, wind direction, and rainfall.
- **Retrieve Measurements**: Get all measurements or filter by specific station IDs and date ranges.
- **Update Measurements**: Modify existing measurements.
- **Authentication**: Endpoints are protected using JWT-based authentication.

## Requirements

- Docker
- Docker Compose

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/Alefas5/weather_app.git
cd weather_app
```

### 2. Build and Run the Docker Containers Use Docker Compose to build and run the application:

- docker-compose up --build

### 3. Run the test_app

- python -m pytest test_app.py

### 4. API Endpoints

- POST /token: Obtain JWT token by providing a username and password.
- POST /measurements/: Create a new weather measurement (requires a valid JWT token).
- GET /measurements/: Retrieve all measurements or filter by station IDs and date ranges (requires a valid JWT token).
- PUT /measurements/{station_id}/{timestamp}/: Update an existing measurement (requires a valid JWT token).

### 5. Access the API Documentation

- **Swagger UI**: http://127.0.0.1:8000/docs - Interactive API documentation.
- **ReDoc**: http://127.0.0.1:8000/redoc - Alternative API documentation with a different style.
- **OpenAPI JSON**: http://127.0.0.1:8000/openapi.json - Raw OpenAPI schema in JSON format.
