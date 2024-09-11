# Use the official Python image
FROM python:3.11-slim

# Set the working directory inside the Docker container
WORKDIR /app

# Copy requirements.txt to the container
COPY requirements.txt .

# Install dependencies with retries
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project to the container
COPY . .

# Expose port 80 to the outside world
EXPOSE 80

# Command to run the FastAPI app with uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
