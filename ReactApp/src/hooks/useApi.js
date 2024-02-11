import {useState} from 'react';

const config = require('../../zrc')


const useApi = () => {
    const [loading, setLoading] = useState(false);
    const baseUrl = config.apiHost

    const fetchLogs = async () => {
        setLoading(true);
        const response = await fetch(`${baseUrl}/logs`);
        const data = await response.json();
        setLoading(false);
        return data;
    };

    const deleteLogEntry = async (id) => {
        setLoading(true);
        const response = await fetch(`${baseUrl}/logs/entries/${id}`, {
            method: 'DELETE',
        });
        const data = await response.json();
        setLoading(false);
        return data;
    };

    const fetchDevices = async () => {
        setLoading(true);
        const response = await fetch(`${baseUrl}/devices`);
        const data = await response.json();
        setLoading(false);
        return data;
    };

    const addDevice = async (deviceId, platform, displayName) => {
        setLoading(true);
        const response = await fetch(`${baseUrl}/devices/add`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                id: deviceId,
                platform: platform,
                display_name: displayName,
                device_info: {
                    "name": deviceId,
                    "manufacturer": "ZRW",
                    "model": `${platform.toUpperCase()}-Circuit`,
                    "identifiers": deviceId
                }
            })
        });
        const data = await response.json();
        setLoading(false);
        return data;
    };
    const restartDevice = async (deviceId) => {
        setLoading(true);
        const response = await fetch(`${baseUrl}/devices/${deviceId}/restart`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'}
        });
        const data = await response.json();
        setLoading(false);
        return data;
    };

    const sendMessage = async (deviceId, message) => {
        setLoading(true);
        const response = await fetch(`${baseUrl}/devices/${deviceId}/send-message`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(message)
        });
        const data = await response.json();
        setLoading(false);
        return data;
    };

    const deleteDevice = async (id) => {
        setLoading(true);
        const response = await fetch(`${baseUrl}/devices/${id}`, {
            method: 'DELETE',
        });
        const data = await response.json();
        setLoading(false);
        return data;
    }

    const updateDeviceName = async (id, newName) => {
        setLoading(true);
        const response = await fetch(`${baseUrl}/devices/${id}/display_name`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({display_name: newName})
        });
        const data = await response.json();
        setLoading(false);
        return data;
    };

    const updateDeviceSettings = async (id, newSettings) => {
        setLoading(true);
        const response = await fetch(`${baseUrl}/devices/${id}/settings`, {
            method: 'PUT',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(newSettings)
        });
        const data = await response.json();
        setLoading(false);
        return data;
    };

    const fetchDeviceConfig = async (deviceId) => {
        setLoading(true);
        const response = await fetch(`${baseUrl}/devices/${deviceId}/config`);
        const data = await response.json();
        setLoading(false);
        return data;
    };

    const updateDeviceConfig = async (id, config) => {
        setLoading(true);
        const response = await fetch(`${baseUrl}/devices/${id}/config`, {
            method: 'PUT',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(config)
        });
        const data = await response.json();
        setLoading(false);
        return data;
    };
    const deleteDeviceConfig = async (id) => {
        setLoading(true);
        const response = await fetch(`${baseUrl}/devices/${id}/config`, {
            method: 'DELETE'
        });
        const data = await response.json();
        setLoading(false);
        return data;
    };

    const fetchDeviceSensors = async (id) => {
        setLoading(true);
        const response = await fetch(`${baseUrl}/devices/${id}/sensors`);
        const data = await response.json();
        setLoading(false);
        return data;
    };

    const addSensor = async (sensorType, sensorName, deviceConfigId, sensorConfig) => {
        setLoading(true);
        const response = await fetch(`${baseUrl}/sensors/add`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                    sensor_type: sensorType,
                    name: sensorName,
                    device_config_id: deviceConfigId,
                    sensor_config: sensorConfig
                }
            )
        });
        const data = await response.json();
        setLoading(false);
        return data;
    };

    const updateSensorConfig = async (id, config) => {
        setLoading(true);
        const response = await fetch(`${baseUrl}/sensors/${id}/config`, {
            method: 'PUT',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(config)
        });
        const data = await response.json();
        setLoading(false);
        return data;
    };

    const deleteSensor = async (id) => {
        setLoading(true);
        const response = await fetch(`${baseUrl}/sensors/${id}`, {
            method: 'DELETE',
        });
        const data = await response.json();
        setLoading(false);
        return data;
    };
    const fetchWifiNetworks = async () => {
        setLoading(true);
        const response = await fetch(`${baseUrl}/configs/wifi-networks`);
        const data = await response.json();
        setLoading(false);
        return data;
    };

    const addWifiNetwork = async (ssid, password) => {
        setLoading(true);
        const response = await fetch(`${baseUrl}/configs/wifi-networks`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                ssid: ssid,
                password: password,
                is_default: true
            })
        });
        const data = await response.json();
        setLoading(false);
        return data;
    };

    const updateWifiNetwork = async (wifiNetworkId, wifiNetworkData) => {
        setLoading(true);
        const response = await fetch(`${baseUrl}/configs/wifi-networks/${wifiNetworkId}`, {
            method: 'PUT',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(wifiNetworkData)
        });
        const data = await response.json();
        setLoading(false);
        return data;
    };

    const deleteWifiNetwork = async (wifiNetworkId) => {
        setLoading(true);
        const response = await fetch(`${baseUrl}/configs/wifi-networks/${wifiNetworkId}`, {
            method: 'DELETE'
        });
        const data = await response.json();
        setLoading(false);
        return data;
    };

    const fetchFtpServers = async () => {
        setLoading(true);
        const response = await fetch(`${baseUrl}/configs/ftp-servers`);
        const data = await response.json();
        setLoading(false);
        return data;
    };

    const addFtpServer = async (hostAddress, username, password) => {
        setLoading(true);
        const response = await fetch(`${baseUrl}/configs/ftp-servers`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                host_address: hostAddress,
                username: username,
                password: password,
                is_default: true
            })
        });
        const data = await response.json();
        setLoading(false);
        return data;
    };

    const updateFtpServer = async (ftpServerId, ftpServerData) => {
        setLoading(true);
        const response = await fetch(`${baseUrl}/configs/ftp-servers/${ftpServerId}`, {
            method: 'PUT',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(ftpServerData)
        });
        const data = await response.json();
        setLoading(false);
        return data;
    };

    const deleteFtpServer = async (ftpServerId) => {
        setLoading(true);
        const response = await fetch(`${baseUrl}/configs/ftp-servers/${ftpServerId}`, {
            method: 'DELETE'
        });
        const data = await response.json();
        setLoading(false);
        return data;
    };

    const fetchMqttBrokers = async () => {
        setLoading(true);
        const response = await fetch(`${baseUrl}/configs/mqtt-brokers`);
        const data = await response.json();
        setLoading(false);
        return data;
    };

    const addMqttBroker = async (hostAddress, port, username, password) => {
        setLoading(true);
        const response = await fetch(`${baseUrl}/configs/mqtt-brokers`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                host_address: hostAddress,
                port: port,
                username: username,
                password: password,
                is_default: true
            })
        });
        const data = await response.json();
        setLoading(false);
        return data;
    };

    const updateMqttBroker = async (mqttBrokerId, mqttBrokerData) => {
        setLoading(true);
        const response = await fetch(`${baseUrl}/configs/mqtt-brokers/${mqttBrokerId}`, {
            method: 'PUT',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(mqttBrokerData)
        });
        const data = await response.json();
        setLoading(false);
        return data;
    };
    const deleteMqttBroker = async (mqttBrokerId) => {
        setLoading(true);
        const response = await fetch(`${baseUrl}/configs/mqtt-brokers/${mqttBrokerId}`, {
            method: 'DELETE'
        });
        const data = await response.json();
        setLoading(false);
        return data;
    };


    const checkIn = async () => {
        setLoading(true);
        const response = await fetch(`${baseUrl}/logs/check-in`, {
            method: 'POST',
        });
        const data = await response.json();
        setLoading(false);
        return data;
    };

    return {
        fetchLogs,
        deleteLogEntry,
        fetchDevices,
        addDevice,
        updateDeviceName,
        updateDeviceSettings,
        deleteDevice,
        fetchDeviceConfig,
        updateDeviceConfig,
        deleteDeviceConfig,
        fetchDeviceSensors,
        addSensor,
        updateSensorConfig,
        deleteSensor,
        checkIn,
        restartDevice,
        fetchWifiNetworks,
        addWifiNetwork,
        updateWifiNetwork,
        deleteWifiNetwork,
        fetchFtpServers,
        addFtpServer,
        updateFtpServer,
        deleteFtpServer,
        fetchMqttBrokers,
        addMqttBroker,
        updateMqttBroker,
        deleteMqttBroker,
        sendMessage,
        loading
    };
};


export default useApi;
