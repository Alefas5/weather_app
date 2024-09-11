from fastapi.testclient import TestClient
from datetime import datetime
from urllib.parse import quote
from main import app

# Create a test client for the FastAPI app
client = TestClient(app)

# Helper function to get the authorization token
def get_auth_token():
    response = client.post(
        "/token",
        data={"username": "alefas", "password": "12345"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert response.status_code == 200  # Ensure token generation is successful
    return response.json()["access_token"]  # Return the access token

# Test case to create a new measurement
def test_create_measurement():
    token = get_auth_token()  # Get the authorization token
    response = client.post(
        "/measurements/",
        json={
            "datetime": "2024-09-07T12:00:00",
            "station_id": "ST001",
            "temperature": 25.5,
            "humidity": 60.0,
            "wind_speed": 5.0,
            "wind_direction": 180.0,
            "rainfall": 2.5
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200  # Ensure creation is successful
    assert response.json()["station_id"] == "ST001"  # Verify the station ID

# Test case to retrieve all measurements
def test_get_measurements():
    token = get_auth_token()  # Get the authorization token
    response = client.get("/measurements/", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200  # Ensure retrieval is successful
    assert isinstance(response.json(), list)  # Verify the response is a list

# Test case to update an existing measurement
def test_update_measurement():
    token = get_auth_token()  # Get the authorization token
    
    # First, create a measurement to update later
    create_response = client.post(
        "/measurements/",
        json={
            "datetime": "2024-09-08T21:17:37",  # Ensure the format matches the database
            "station_id": "ST001",
            "temperature": 25.5,
            "humidity": 60.0,
            "wind_speed": 5.0,
            "wind_direction": 180.0,
            "rainfall": 2.5
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    assert create_response.status_code == 200  # Ensure creation is successful
    created_measurement = create_response.json()

    # URL-encode the datetime to make it safe for use in the URL
    encoded_datetime = quote(created_measurement['datetime'])

    # Update the measurement that was just created
    update_response = client.put(
        f"/measurements/{created_measurement['station_id']}/{encoded_datetime}",
        json={
            "temperature": 26.5,  # Update temperature and humidity
            "humidity": 55.0
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    assert update_response.status_code == 200  # Ensure update is successful
    updated_measurement = update_response.json()

    # Verify that the values were updated correctly
    assert updated_measurement["temperature"] == 26.5
    assert updated_measurement["humidity"] == 55.0

# Test case to retrieve measurements with filters
def test_get_measurements_with_filters():
    token = get_auth_token()  # Get the authorization token

    # Create multiple measurements
    create_response_1 = client.post(
        "/measurements/",
        json={
            "datetime": "2024-09-07T12:00:00",
            "station_id": "ST001",
            "temperature": 25.5,
            "humidity": 60.0,
            "wind_speed": 5.0,
            "wind_direction": 180.0,
            "rainfall": 2.5
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    assert create_response_1.status_code == 200

    create_response_2 = client.post(
        "/measurements/",
        json={
            "datetime": "2024-09-07T14:00:00",
            "station_id": "ST002",
            "temperature": 22.0,
            "humidity": 55.0,
            "wind_speed": 3.0,
            "wind_direction": 90.0,
            "rainfall": 1.0
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    assert create_response_2.status_code == 200

    create_response_3 = client.post(
        "/measurements/",
        json={
            "datetime": "2024-09-08T10:00:00",
            "station_id": "ST001",
            "temperature": 20.0,
            "humidity": 50.0,
            "wind_speed": 4.0,
            "wind_direction": 270.0,
            "rainfall": 0.0
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    assert create_response_3.status_code == 200

    # Test filtering by station_id and a specific date
    response = client.get("/measurements/?station_ids=ST001&start_date=2024-09-08", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    measurements = response.json()
    assert isinstance(measurements, list)
    assert all(m["station_id"] == "ST001" for m in measurements)


    # Convert datetime strings to datetime objects and compare the date part only
    assert all(datetime.fromisoformat(m["datetime"].split("+")[0]).date() == datetime(2024, 9, 8).date() for m in measurements)


# Test case to handle invalid temperature input
def test_create_measurement_invalid_temperature():
    token = get_auth_token()  # Get the authorization token
    response = client.post(
        "/measurements/",
        json={
            "datetime": "2024-09-07T12:00:00",
            "station_id": "ST001",
            "temperature": 150.0,  # Invalid temperature
            "humidity": 60.0,
            "wind_speed": 5.0,
            "wind_direction": 180.0,
            "rainfall": 2.5
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 422  # Ensure validation error (Unprocessable Entity)

# Test case to handle invalid wind direction input
def test_create_measurement_invalid_wind_direction():
    token = get_auth_token()  # Get the authorization token
    response = client.post(
        "/measurements/",
        json={
            "datetime": "2024-09-07T12:00:00",
            "station_id": "ST001",
            "temperature": 25.5,
            "humidity": 60.0,
            "wind_speed": 5.0,
            "wind_direction": 400.0,  # Invalid wind direction
            "rainfall": 2.5
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 422  # Ensure validation error (Unprocessable Entity)
