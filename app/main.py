from fastapi import FastAPI
from dotenv import load_dotenv  # Import dotenv to load environment variables
import os  # Import os to access environment variables
from app import models, database
from app.routes import router as measurement_router
from fastapi.responses import RedirectResponse

# Load environment variables from the .env file
load_dotenv()

# Initialize the FastAPI app
app = FastAPI()

# Redirect the root URL to the /docs endpoint (Swagger UI documentation)
@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")

# Create the database tables based on the models defined in the application
models.Base.metadata.create_all(bind=database.engine)

# Include the routes from the measurement_router
app.include_router(measurement_router)
