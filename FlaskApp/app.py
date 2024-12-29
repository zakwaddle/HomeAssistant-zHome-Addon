from flask import Flask, send_from_directory, jsonify, request
from blueprints.logs import log_blueprint
from blueprints.devices import device_blueprint
from blueprints.sensors import sensor_blueprint
from blueprints.configs import config_blueprint
from flask_cors import CORS
from paho.mqtt import client as mqtt
from paho.mqtt.enums import CallbackAPIVersion
from threading import Thread
from database import add_log
from mqtt import send_mqtt_message
import json
import os
import requests

app = Flask(__name__, static_folder='static')
CORS(app)


def get_ha_token():
    return os.getenv("HA_TOKEN")

def get_ha_scenes():
    HA_TOKEN = get_ha_token()
    if HA_TOKEN is not None:
        req = requests.get(f"http://homeassistant.local:8123/api/states", headers={"Authorization": f"Bearer {HA_TOKEN}"})
        if req.status_code == 200:
            try:
                data = req.json()
                scenes = [(i["attributes"]["friendly_name"], i['entity_id']) for i in data if i['entity_id'].startswith("scene.")]
                return {"status_code": 200, "scenes": scenes}
            except json.JSONDecodeError:
                pass
        else:
            return {"status_code": req.status_code, "error": req.text}
        
def get_mqtt_details():
    SUP_TOK = os.getenv("SUPERVISOR_TOKEN")
    if SUP_TOK is not None:
        print("obtained HA superviser token")
        req = requests.get("http://supervisor/services/mqtt", headers={"Authorization": f"Bearer {SUP_TOK}"})
        if req.status_code == 200:
            print("obtained mqtt details")
            try:
                return req.json()['data']
            except Exception as e:
                print(e)


def on_connect(client, userdata, flags, rc, props):
    print("Connected with result code " + str(rc))
    client.subscribe("z-home/log/#")
    client.subscribe("z-home/disconnect")


def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload), flush=True)
    # Logic to log message to database
    if msg.topic.startswith("z-home/log"):
        log_mes = json.loads(msg.payload)
        log = {"log": log_mes, "topic": msg.topic}
        add_log(log)
    if msg.topic.startswith("z-home/disconnect"):
        mes = json.loads(msg.payload)
        print(f"got disconnect: {mes}", flush=True)
        topics = mes.get('availability_topics')
        print(f"topics: {topics}", flush=True)
        if topics and topics is not None:
            for i in topics:
                print(f"sending 'offline' to: {i}", flush=True)
                client.publish(i, "offline")


def start_mqtt_loop():
    mqtt_details = get_mqtt_details()
    un = mqtt_details.get('username')
    pw = mqtt_details.get('password')
    host = mqtt_details.get('host')
    port = mqtt_details.get('port')

    mqtt_client = mqtt.Client(CallbackAPIVersion(2))
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message

    mqtt_client.username_pw_set(un, pw)

    mqtt_client.connect(host, port, 60)
    mqtt_client.loop_forever()


thread = Thread(target=start_mqtt_loop)
thread.start()


# Serve React App
@app.route('/dashboard', defaults={'path': ''})
@app.route('/<path:path>')
def serve_react_app(path):
    if path != "" and os.path.exists(app.static_folder + '/react/' + path):
        return send_from_directory(app.static_folder + '/react', path)
    else:
        return send_from_directory(app.static_folder + '/react', 'index.html')
    
@app.route('/api/mqtt')
def serve_mqtt_details():
    mqtt_details = get_mqtt_details()
    return jsonify(mqtt_details)
    
@app.route('/api/ha_token')
def get_token():
    data = get_ha_token()
    print(data)
    return jsonify({"token": data})

@app.route('/api/ha/scenes')
def get_scenes():
    data = get_ha_scenes()
    return jsonify(data)

@app.route('/api/ha/scenes/activate', methods=["POST"])
def activate_scene():
    data = request.json
    token = get_ha_token()
    scene = data.get('scene')
    if scene is not None:
        target = { "entity_id": scene }
        req = requests.post(f"http://homeassistant.local:8123/api/services/scene/turn_on", headers={"Authorization": f"Bearer {token}"}, json=target)
        return jsonify({"status_code": req.status_code})


app.register_blueprint(log_blueprint, url_prefix='/api/home/logs')
app.register_blueprint(device_blueprint, url_prefix='/api/home/devices')
app.register_blueprint(sensor_blueprint, url_prefix='/api/home/sensors')
app.register_blueprint(config_blueprint, url_prefix='/api/home/configs')

if __name__ == "__main__":
    app.run("0.0.0.0")
