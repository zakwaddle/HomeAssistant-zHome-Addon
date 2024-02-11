# MQTT and Motion Sensor Classes

This repository contains two classes, `MotionSensor` and `MQTTMotionSensor`, which are designed to interact with a motion sensor and an MQTT broker respectively.

## MotionSensor

The `MotionSensor` class represents a motion sensor. It uses interrupts to detect changes in the sensor's state.

### Usage

To instantiate a `MotionSensor` object, you need to provide the pin number to which the sensor is connected and a delay in milliseconds before retriggering the sensor. Optionally, you can also provide a timer number to be used for retriggering.

```python
motion_sensor = MotionSensor(pin=2, retrigger_delay_ms=500, timer_n=1)
```

The MotionSensor class provides methods to set functions to be called when motion is detected (set_on_motion_detected) and when motion is not detected (set_on_motion_not_detected).

```python
def on_motion_detected():
    print("Motion detected!")

def on_motion_not_detected():
    print("No motion detected!")

motion_sensor.set_on_motion_detected(on_motion_detected)
motion_sensor.set_on_motion_not_detected(on_motion_not_detected)
```

You can also enable interrupts for the motion sensor pin using the enable_interrupt method.

## MQTTMotionSensor
The MQTTMotionSensor class represents an MQTT motion sensor. It utilizes an instance of the MotionSensor class and an MQTT client to publish motion sensor data to an MQTT broker.

### Usage
To instantiate an MQTTMotionSensor object, you need to provide an instance of the MotionSensor class and an MQTT client instance.

```python
mqtt_motion_sensor = MQTTMotionSensor(motion_sensor=motion_sensor, mqtt_client=mqtt_client)
```

The MQTTMotionSensor class provides methods to set the name of the MQTT motion sensor (set_name), the MQTT topic to which the motion sensor publishes (set_topic), and to publish the last motion detected to the MQTT topic (publish_last_motion).

```python
mqtt_motion_sensor.set_name('motion-1')
mqtt_motion_sensor.set_topic('sensors/motion/1')
mqtt_motion_sensor.publish_last_motion()
```

The MQTTMotionSensor class also provides methods to publish discovery (publish_discovery) and null discovery (publish_null_discovery) messages to the MQTT broker.
