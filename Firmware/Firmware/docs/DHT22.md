# DHT22 Sensor and MQTTDHT22Sensor

This module contains two classes, DHT22Sensor and MQTTDHT22Sensor, which allow you to work with a DHT22 temperature and
humidity sensor and publish the sensor data to an MQTT broker.

## DHT22Sensor

DHT22Sensor is a class representing a DHT22 temperature and humidity sensor. This class allows you to read measurements
from the sensor and execute a function each time a measurement is taken.

### Methods

- `__init__(self, pin, timer_n=1)`:\
  Initialize the DHT22 sensor. The pin argument is the GPIO pin number the sensor is
  connected to. timer_n is the timer number to be used for retriggering, with a default value of 1.

- `enable_interrupt(self)`:\
  Enable a timer for regular measurements. The timer behavior is platform-dependent.

- `set_on_measurement(self, func)`:\
  Set a function to be called when a measurement is taken. The func argument is the
  function to be called.

- `measure(self, _)`:\
  Measure the temperature and humidity using the sensor and call the function set by
  set_on_measurement().

## MQTTDHT22Sensor

MQTTDHT22Sensor is a class representing an MQTT-connected DHT22 temperature and humidity sensor. This class allows you
to publish the sensor data to an MQTT broker.

### Methods

- `__init__(self, dht22_sensor)`:\
  DHT22Sensor, mqtt_client): Initialize the MQTT DHT22 sensor. dht22_sensor is an
  instance of the DHT22Sensor class. mqtt_client is an MQTT client instance.

- `enable_interrupt(self)`:\
  Enable a timer for regular measurements.

- `publish_measurement(self, temperature, humidity)`:\
  Publish the latest temperature and humidity measurement to the
  MQTT topic. temperature and humidity are the latest measurements.

- `set_name(self, name_temp, name_humidity)`:\
  Set the name of the temperature and humidity sensors. name_temp and
  name_humidity are the names for the sensors.

- `set_topic(self, topic)`:\
  Set the MQTT topic to which the sensor publishes. topic is the MQTT topic.

- `publish_discovery(self)`:\
  Publish discovery messages to the MQTT broker. This function automatically generates the
  discovery topics and messages.

### setup_dht22_sensor

- `setup_dht22_sensor(p, tn, client, name_temp, name_humidity)`:\
  is a utility function that sets up a DHT22 sensor and
  returns an MQTTDHT22Sensor instance. p is the GPIO pin number the sensor is connected to. tn is the timer number to be
  used for retriggering. client is an MQTT client instance. name_temp and name_humidity are the names for the
  temperature
  and humidity sensors, respectively.

