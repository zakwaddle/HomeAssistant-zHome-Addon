#!/usr/bin/env bash
# Fetch MQTT service details using Bashio
MQTT_HOST="$(bashio::services mqtt 'host')"
MQTT_PORT="$(bashio::services mqtt 'port')"
MQTT_USER="$(bashio::services mqtt 'username')"
MQTT_PASSWORD="$(bashio::services mqtt 'password')"

# Export fetched details as environment variables
export MQTT_HOST MQTT_PORT MQTT_USER MQTT_PASSWORD

# Then start your Flask application
#python /path/to/your/app.py
flask run --host="0.0.0.0" --port=5000