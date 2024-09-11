from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from app.schemas import Measurement, MeasurementUpdate
from app.dependencies import get_db
from app import crud
from fastapi.security import OAuth2PasswordRequestForm
from app.auth import create_access_token, verify_token  # Import functions for token creation and verification

# Create a FastAPI router for handling API endpoints
router = APIRouter()

# Public login endpoint
@router.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # Check user credentials
    if form_data.username == "alefas" and form_data.password == "12345":
        user_dict = {"username": form_data.username}
        access_token = create_access_token(data=user_dict)  # Generate an access token
        return {"access_token": access_token, "token_type": "bearer"}
    else:
        raise HTTPException(status_code=400, detail="Invalid username or password")

# Protected endpoint for inserting new measurements
@router.post("/measurements/")
def create_measurement(
    measurement: Measurement,
    db: Session = Depends(get_db), 
    payload: dict = Depends(verify_token)  # Verify the token before allowing access
):
    # Call CRUD function to create a measurement
    return crud.create_measurement(db, measurement)

# Protected endpoint for retrieving measurements with optional filters
@router.get("/measurements/")
def get_measurements(
    station_ids: List[str] = Query(None),  # Accept a list of station IDs as a query parameter
    start_date: str = None,  # Optional start date filter
    end_date: str = None,  # Optional end date filter
    db: Session = Depends(get_db),
    payload: dict = Depends(verify_token)  # Verify the token before allowing access
):
    # Call CRUD function to retrieve measurements based on filters
    return crud.get_measurements(db, station_ids, start_date, end_date)

# Protected endpoint for updating an existing measurement
@router.put("/measurements/{station_id}/{timestamp}/")
def update_measurement(
    station_id: str,  # Path parameter for station ID
    timestamp: str,  # Path parameter for timestamp
    measurement: MeasurementUpdate,  # Use the schema for partial updates
    db: Session = Depends(get_db),
    payload: dict = Depends(verify_token)  # Verify the token before allowing access
):
    # Perform the update using the CRUD function
    updated_measurement = crud.update_measurement(db, station_id, timestamp, measurement)
    if updated_measurement:
        return updated_measurement  # Return the updated measurement if found
    else:
        raise HTTPException(status_code=404, detail="Measurement not found")  # Raise an error if no measurement is found
