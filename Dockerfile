# Use an official Python runtime as the parent image
FROM python:3.8

# Set the working directory in the container
WORKDIR /app

# Copy the Flask application into the container at /app
COPY FlaskApp/ ./FlaskApp

# Install any needed packages specified in FlaskApp/requirements.txt
RUN pip install --no-cache-dir -r FlaskApp/requirements.txt

# Copy the React application build artifacts into the container
# Assuming the React build process has been run before building the Docker image
# COPY ReactApp/build/ ./FlaskApp/static/react

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable for Flask to run in production mode
ENV FLASK_APP=FlaskApp/app.py
ENV FLASK_ENV=production

# Run Flask app
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
