from flask import Blueprint, request, jsonify
from database import add_sensor, update_sensor_config, delete_sensor, get_sensor

sensor_blueprint = Blueprint('sensor_blueprint', __name__)


@sensor_blueprint.route('/<string:sensor_id>')
def get_sensor_by_id(sensor_id):
    sensor = get_sensor(sensor_id)
    return jsonify(success=True, sensor=sensor)


@sensor_blueprint.route('/add', methods=['POST'])
def add_new_sensor():
    sensor_data = request.json
    new_sensor = add_sensor(sensor_data)
    return jsonify(success=True, sensor=new_sensor)


@sensor_blueprint.route('/<string:sensor_id>/config', methods=['PUT'])
def update_sensor(sensor_id):
    new_config = request.json
    update_sensor_config(sensor_id, new_config)
    return jsonify(success=True)


@sensor_blueprint.route('/<string:sensor_id>', methods=['DELETE'])
def remove_sensor(sensor_id):
    delete_sensor(sensor_id)
    return jsonify(success=True)
