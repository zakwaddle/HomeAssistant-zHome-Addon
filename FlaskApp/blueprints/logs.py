from flask import Blueprint, request, jsonify
from database import add_log, get_logs, delete_log
from flask_sse import sse
from mqtt import send_mqtt_message
import json

log_blueprint = Blueprint('log_blueprint', __name__)


@log_blueprint.route('/')
def home():
    data = get_logs()
    return jsonify(data)


@log_blueprint.route('/add', methods=['POST'])
def add_log_entry():
    log_data = request.json
    new_log = add_log(log_data)
    sse.publish({"message": "New log added", "type": "log", "log": new_log})
    return jsonify(success=True)


@log_blueprint.route('/entries/<int:id>', methods=['DELETE'])
def delete_log_entry(id):
    delete_log(id)
    # print(f"deleted id: {id}")
    return jsonify({'message': 'Log entry deleted'})


@log_blueprint.route('/check-in', methods=['POST'])
def send_check_in_message():
    send_mqtt_message("command/all-units", json.dumps({'command': 'check-in'}))
    return jsonify(success=True)
