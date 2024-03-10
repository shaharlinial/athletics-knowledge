# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Copy only the necessary files for dependency installation
COPY pyproject.toml poetry.lock /app/



RUN pip install poetry

# RUN poetry --version
# # Install dependencies using Poetry
RUN poetry install --no-interaction --no-ansi -vvv

# # Copy the rest of the application code
COPY . /app

# # Make port 5000 available to the world outside this container
EXPOSE 5000

# # Define environment variable
ENV NAME World

# # Run app.py when the container launches
CMD ["poetry","run", "python", "app.py"]