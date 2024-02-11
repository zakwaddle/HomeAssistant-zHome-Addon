# MQTT-Controlled Dimmable LED Light

This repository contains Python classes for controlling a dimmable LED light over MQTT. These classes are designed to
run on microcontrollers such as Raspberry Pi Pico or ESP32 using MicroPython.

## Classes

### DimmableLight

`DimmableLight` is a class for controlling a dimmable LED light connected to a microcontroller. It provides methods to
turn the light on and off, to set the brightness of the light, and to smoothly fade the light from its current
brightness to a target brightness.

### MQTTDimmableLight

`MQTTDimmableLight` is a wrapper class for `DimmableLight` that adds MQTT functionality. It provides methods to publish
the state and brightness of the light to an MQTT broker, and to handle incoming MQTT messages that command the light to
turn on or off or set its brightness. It also includes a method to publish a discovery message to the MQTT broker, which
allows the light to be automatically discovered and set up in Home Assistant.

## Usage

First, create an instance of `DimmableLight`, passing the pin number that the LED light is connected to:

```python
light = DimmableLight(pin=5)
```

Then, create an instance of `MQTTDimmableLight`, passing the `DimmableLight` instance and an MQTT client:

```python
mqtt_light = MQTTDimmableLight(mqtt_client, light)
```

The MQTT client should be connected to an MQTT broker, and should be set up to call the on_message method of
MQTTDimmableLight whenever it receives an MQTT message:

```python
mqtt_client.set_callback(mqtt_light.on_message)
```

## Requirements

- MicroPython
- A microcontroller such as Raspberry Pi Pico or ESP32
- An MQTT broker
- Home Assistant (optional)

## Notes

This code is provided as-is, and is intended for educational purposes. Please use it responsibly and respect the privacy
and security of others.