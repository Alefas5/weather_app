from pydantic import BaseModel, validator
from typing import Optional
from datetime import datetime

# Schema for creating/updating measurements
class Measurement(BaseModel):
    station_id: str
    datetime: datetime
    temperature: float
    humidity: float
    wind_speed: float
    wind_direction: float
    rainfall: float

    # Validation for temperature
    @validator('temperature')
    def validate_temperature(cls, value):
        if not (-50.0 <= value <= 60.0):
            raise ValueError('Temperature must be between -50°C and 60°C')
        return value

    # Validation for humidity
    @validator('humidity')
    def validate_humidity(cls, value):
        if not (0.0 <= value <= 100.0):
            raise ValueError('Humidity must be between 0% and 100%')
        return value

    # Validation for wind speed
    @validator('wind_speed')
    def validate_wind_speed(cls, value):
        if not (0.0 <= value <= 150.0):
            raise ValueError('Wind speed must be between 0 and 150 km/h')
        return value

    # Validation for wind direction
    @validator('wind_direction')
    def validate_wind_direction(cls, value):
        if not (0.0 <= value <= 360.0):
            raise ValueError('Wind direction must be between 0° and 360°')
        return value

    # Validation for rainfall
    @validator('rainfall')
    def validate_rainfall(cls, value):
        if value < 0.0:
            raise ValueError('Rainfall must be a non-negative value')
        return value

    class Config:
        orm_mode = True  # Enable compatibility with SQLAlchemy models

# New schema for partial updates of measurements
class MeasurementUpdate(BaseModel):
    temperature: Optional[float]
    humidity: Optional[float]
    wind_speed: Optional[float]
    wind_direction: Optional[float]
    rainfall: Optional[float]

    # Validation for temperature
    @validator('temperature')
    def validate_temperature(cls, value):
        if value is not None and not (-50.0 <= value <= 60.0):
            raise ValueError('Temperature must be between -50°C and 60°C')
        return value

    # Validation for humidity
    @validator('humidity')
    def validate_humidity(cls, value):
        if value is not None and not (0.0 <= value <= 100.0):
            raise ValueError('Humidity must be between 0% and 100%')
        return value

    # Validation for wind speed
    @validator('wind_speed')
    def validate_wind_speed(cls, value):
        if value is not None and not (0.0 <= value <= 150.0):
            raise ValueError('Wind speed must be between 0 and 150 km/h')
        return value

    # Validation for wind direction
    @validator('wind_direction')
    def validate_wind_direction(cls, value):
        if value is not None and not (0.0 <= value <= 360.0):
            raise ValueError('Wind direction must be between 0° and 360°')
        return value

    # Validation for rainfall
    @validator('rainfall')
    def validate_rainfall(cls, value):
        if value is not None and value < 0.0:
            raise ValueError('Rainfall must be a non-negative value')
        return value

    class Config:
        orm_mode = True  # Enable compatibility with SQLAlchemy models

# Schema for measurement response output
class MeasurementResponse(BaseModel):
    id: int
    station_id: str
    datetime: datetime
    temperature: float
    humidity: float
    wind_speed: float
    wind_direction: float
    rainfall: float

    class Config:
        orm_mode = True  # Enable returning data from SQLAlchemy models
