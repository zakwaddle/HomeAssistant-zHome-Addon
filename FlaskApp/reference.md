## Device Endpoints
**GET** `/api/devices`: \
Fetches all devices. Returns a JSON array of device objects.

**GET** `/api/home/devices/<device_id>/sensors`\
Fetches a device with the given ID

**POST** `/api/devices/add`: \
Adds a new device. Expects a JSON object in the request body with device details. Returns a
JSON object with a success boolean and the added device object.

**DELETE** `/api/devices/<device_id>`: \
Deletes the device with the given ID. Returns a JSON object with a success boolean.

#### Example Device
```json
{
  "id": "PicoW_001",
  "platform": "rp2",
  "display_name": "something-something",
  "device_info": {
    "name": "PicoW_001",
    "manufacturer": "ZRW",
    "model": "RP2-Circuit",
    "identifiers": "PicoW_001"
  }
}
```
- - - 
## Log Endpoints
**GET** `/api/logs`: \
Fetches all logs. Returns a JSON array of device objects.

**POST** `/api/logs/add`: \
Adds a new log. Expects a JSON object in the request body with log details. Returns a
JSON object with a success boolean.

**DELETE** `/api/logs/entries/<int:id>`: \
Deletes the log with the given ID. Returns a JSON object with a success boolean.

#### Example Log
```json
{
  "device_id": "PicoW_001",
  "topic": "z-home/log/PicoW_001",
  "log": {
    "message": "bla bla bla",
    "type": "info"
  }
}
```
- - - 
## Device Config Endpoints
**GET** `/api/devices/<device_id>/config`: \
Fetches the configuration for the device with the given ID. Returns a JSON object
with the device configuration.

**POST** `/api/home/devices/<device_id>/config`\
Updates the configuration for the device with the given ID. Expects a JSON object
in the request body with the new configuration.

**PUT** `/api/devices/<device_id>/config`: \
Updates the configuration for the device with the given ID. Expects a JSON object
in the request body with the new configuration. Returns a JSON object with a success boolean.

**DELETE** `/api/home/devices/<device_id>/config`\
Deletes the configuration for the device with the given ID. Returns a JSON object with a success boolean.

#### Example Device Config
```json
{

    "wifi": {
      "ssid": "the_interwebs",
      "password": "935Ravine"
    },
    "mqtt": {
      "server": "homeassistant.local",
      "port": 1883,
      "username": "Zak",
      "password": "935Ravine"
    },
    "ftp": {
      "host": "homeassistant.local",
      "user": "microcontrollers",
      "password": "microcontrollers"
    }
  
}
```
- - - 
## Sensor Endpoints
**GET** `/api/devices/<device_id>/sensors`:\
Fetches all sensors for the device with the given ID. Returns a JSON array of sensor objects.

**POST** `/api/sensors/add`:\
Adds a new sensor. Expects a JSON object in the request body with sensor details. Returns a
JSON object with a success boolean and the added sensor object.

**PUT** `/api/sensors/<sensor_id>/config`:\
Updates the configuration for the sensor with the given ID. Expects a JSON object
in the request body with the new configuration. Returns a JSON object with a success boolean.

**DELETE** `/api/sensors/<sensor_id>`:\
Deletes the sensor with the given ID. Returns a JSON object with a success boolean.

#### Example Weather Sensor Config
```json
{
  "sensor_type": "weather",
  "device_config_id": 2,
  "name": "Bedroom Weather",
  "sensor_config": {
    "pin": 28,
    "measurement_interval_ms": 10000
  }
}
```
#### Example LED Config
```json
{
  "sensor_type": "led",
  "device_config_id": 2,
  "name": "Shelf Lights",
  "sensor_config": {
        "pin": 4,
        "freq": 300,
        "fade_time_ms": 4,
        "brightness_scale": 255
  }
}
```
#### Example Motion Sensor Config
```json
{
  "sensor_type": "motion",
  "device_config_id": 2,
  "name": "Nook Motion",
  "sensor_config": {
        "pin": 27,
        "retrigger_delay_ms": 120000
  }
}
```
