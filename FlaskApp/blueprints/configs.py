from flask import Blueprint, request, jsonify
from database import (add_wifi_network, update_wifi_network, delete_wifi_network,
                      get_all_wifi_networks, get_wifi_network, add_ftp_server,
                      update_ftp_server, delete_ftp_server, get_ftp_server,
                      get_all_ftp_servers, add_mqtt_broker, update_mqtt_broker,
                      delete_mqtt_broker, get_mqtt_broker, get_all_mqtt_brokers)

config_blueprint = Blueprint('config_blueprint', __name__)


@config_blueprint.route('/wifi-networks', methods=['GET'])
def get_wifi_networks():
    data = get_all_wifi_networks()
    return jsonify(data)


@config_blueprint.route('/wifi-networks', methods=['POST'])
def add_new_wifi_network():
    wifi_network_data = request.json
    new_wifi_network = add_wifi_network(wifi_network_data)
    return jsonify(success=True, wifi_network=new_wifi_network)


@config_blueprint.route('/wifi-networks/<int:wifi_network_id>', methods=['PUT'])
def update_wifi_network(wifi_network_id):
    new_wifi_network = request.json
    update_wifi_network(wifi_network_id, new_wifi_network)
    return jsonify(success=True)


@config_blueprint.route('/wifi-networks/<int:wifi_network_id>', methods=['DELETE'])
def remove_wifi_network(wifi_network_id):
    delete_wifi_network(wifi_network_id)
    return jsonify(success=True)


@config_blueprint.route('/ftp-servers', methods=['GET'])
def get_ftp_servers():
    data = get_all_ftp_servers()
    return jsonify(data)


@config_blueprint.route('/ftp-servers', methods=['POST'])
def add_new_ftp_server():
    ftp_server_data = request.json
    new_ftp_server = add_ftp_server(ftp_server_data)
    return jsonify(success=True, ftp_server=new_ftp_server)


@config_blueprint.route('/ftp-servers/<int:ftp_server_id>', methods=['PUT'])
def update_ftp_server(ftp_server_id):
    new_ftp_server = request.json
    update_ftp_server(ftp_server_id, new_ftp_server)
    return jsonify(success=True)


@config_blueprint.route('/ftp-servers/<int:ftp_server_id>', methods=['DELETE'])
def remove_ftp_server(ftp_server_id):
    delete_ftp_server(ftp_server_id)
    return jsonify(success=True)


@config_blueprint.route('/mqtt-brokers', methods=['GET'])
def get_mqtt_brokers():
    data = get_all_mqtt_brokers()
    return jsonify(data)


@config_blueprint.route('/mqtt-brokers', methods=['POST'])
def add_new_mqtt_broker():
    mqtt_broker_data = request.json
    new_mqtt_broker = add_mqtt_broker(mqtt_broker_data)
    return jsonify(success=True, mqtt_broker=new_mqtt_broker)


@config_blueprint.route('/mqtt-brokers/<int:mqtt_broker_id>', methods=['PUT'])
def update_mqtt_broker(mqtt_broker_id):
    new_mqtt_broker = request.json
    update_mqtt_broker(mqtt_broker_id, new_mqtt_broker)
    return jsonify(success=True)


@config_blueprint.route('/mqtt-brokers/<int:mqtt_broker_id>', methods=['DELETE'])
def remove_mqtt_broker(mqtt_broker_id):
    delete_mqtt_broker(mqtt_broker_id)
    return jsonify(success=True)
