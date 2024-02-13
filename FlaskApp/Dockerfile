# Use an official Python runtime as the parent image
FROM python:3.9.18-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_ENV=production
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000
ENV FLASK_DEBUG=False
ENV DATABASE_URI=sqlite:////data/log_entries.db

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Run Flask app
#CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
CMD ["./run.sh"]