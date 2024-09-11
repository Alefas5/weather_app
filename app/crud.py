from sqlalchemy.orm import Session
from typing import List
from app import models, schemas
from datetime import datetime


# Create a new measurement in the database
def create_measurement(db: Session, measurement: schemas.Measurement):
    # Create a new MeasurementDB object using the provided measurement data
    db_measurement = models.MeasurementDB(**measurement.dict())
    db.add(db_measurement)  # Add the new measurement to the database session
    db.commit()  # Commit the changes to the database
    db.refresh(db_measurement)  # Refresh the object with data from the database
    return db_measurement  # Return the new measurement object

# Retrieve measurements from the database with optional filters
def get_measurements(db: Session, station_ids: List[str] = None, start_date: str = None, end_date: str = None):
    # Start a query on the MeasurementDB table
    query = db.query(models.MeasurementDB)
    
    # Add filters for station IDs if provided
    if station_ids:
        query = query.filter(models.MeasurementDB.station_id.in_(station_ids))
    
    # Add date filters if provided
    if start_date:
        query = query.filter(models.MeasurementDB.datetime >= datetime.fromisoformat(start_date))
    if end_date:
        query = query.filter(models.MeasurementDB.datetime <= datetime.fromisoformat(end_date))
    
    return query.all()  # Return all matching measurements

# Update a specific measurement in the database
def update_measurement(db: Session, station_id: str, timestamp: str, measurement: schemas.MeasurementUpdate):
    # Fetch the measurement based on station_id and timestamp
    db_measurement = db.query(models.MeasurementDB).filter(
        models.MeasurementDB.station_id == station_id,
        models.MeasurementDB.datetime == datetime.fromisoformat(timestamp)
    ).first()

    if db_measurement:
        # Update only the fields provided in the request
        if measurement.temperature is not None:
            db_measurement.temperature = measurement.temperature
        if measurement.humidity is not None:
            db_measurement.humidity = measurement.humidity
        if measurement.wind_speed is not None:
            db_measurement.wind_speed = measurement.wind_speed
        if measurement.wind_direction is not None:
            db_measurement.wind_direction = measurement.wind_direction
        if measurement.rainfall is not None:
            db_measurement.rainfall = measurement.rainfall

        db.commit()  # Commit the changes to the database
        db.refresh(db_measurement)  # Refresh the instance with the latest data from the database
        return db_measurement  # Return the updated measurement object
    else:
        return None  # Return None if no measurement is found
