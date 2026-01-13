# Use official Python base image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /code

# Copy requirements and install dependencies
COPY app/requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy the rest of your application code
COPY ./app /code/app

# Command to run the application using Uvicorn
# CMD ["fastapi", "run", "app/main.py", "--port", "80"]
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]