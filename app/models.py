from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, types
from app.database import Base
import pytz

# Define the Athens timezone using pytz
ATHENS_TZ = pytz.timezone('Europe/Athens')

# Define a Custom SQLAlchemy Type for DateTime objects aware of the Athens timezone
class DateTimeAthens(types.TypeDecorator):
    # The underlying SQL type is DateTime
    impl = types.DateTime

    # Set cache_ok to True to indicate that this type is safe for caching
    cache_ok = True

    def process_bind_param(self, value: datetime, _):
        # Convert a naive datetime to the Athens timezone, if it's not already timezone-aware
        if value.tzinfo is None:
            value = ATHENS_TZ.localize(value)  # Localize naive datetime to Athens timezone
        return value  # Return the timezone-aware datetime

    def process_result_value(self, value, _):
        # Ensure datetime is in the Athens timezone when retrieved from the database
        if value is not None:
            if value.tzinfo is None:
                # Localize naive datetime to Athens timezone
                value = ATHENS_TZ.localize(value)
            else:
                # Convert to Athens timezone if it's already timezone-aware
                value = value.astimezone(ATHENS_TZ)
        return value

# Define the MeasurementDB table schema for storing weather data
class MeasurementDB(Base):
    __tablename__ = "measurements"

    # Primary key column for unique identifier
    id = Column(Integer, primary_key=True, index=True)

    # Date and time of the measurement with Athens timezone awareness
    datetime = Column(DateTimeAthens, nullable=False)

    # Identifier for the weather station
    station_id = Column(String, index=True, nullable=False)

    # Temperature measurement
    temperature = Column(Float, nullable=False, default=0.0)

    # Humidity measurement
    humidity = Column(Float, nullable=False, default=0.0)

    # Wind speed measurement
    wind_speed = Column(Float, nullable=False, default=0.0)

    # Wind direction measurement
    wind_direction = Column(Float, nullable=False)

    # Rainfall measurement
    rainfall = Column(Float, nullable=False, default=0.0)
