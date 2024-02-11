import functools
from paho.mqtt import client as mqtt


def mqtt_decorator(func):
    @functools.wraps(func)
    def wrapped(*args, **kwargs):
        mqtt_client = mqtt.Client()

        def on_pub(*args):
            mqtt_client.disconnect()
            print("disconnected mqtt")

        try:
            mqtt_client.on_publish = on_pub
            mqtt_client.username_pw_set(username="Zak", password="935Ravine")
            mqtt_client.connect(host="homeassistant.local", port=1883, keepalive=60)
            print("connected mqtt")
            func(mqtt_client, *args, **kwargs)
            # mqtt_client.disconnect()
        except Exception as e:
            print(f"An error occurred while sending the MQTT message: {e}")
            # Add additional error handling here as needed

    return wrapped


@mqtt_decorator
def send_mqtt_message(mqtt_client, topic, message):
    mqtt_client.publish(topic, message)
