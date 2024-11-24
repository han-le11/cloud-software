# Enter your code below 
# Use an official Python image as the base
FROM python:3.11-alpine3.18

# Set the working directory
WORKDIR /usr/app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the FastAPI app source code from src
COPY .. .

# Expose the port FastAPI will run on
EXPOSE 5000

# Command to run the app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000"]

