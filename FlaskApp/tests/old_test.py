import unittest
import requests
import tests.test_data as td

host = 'http://localhost:5000/api/home'


class FlaskTestCase(unittest.TestCase):
    def setUp(self):
        print("Add Device")
        response = requests.post(url=f'{host}/devices/add', json=td.device_data1)
        data = response.json()
        self.assertEqual(response.status_code, 200, "Failed to add device")
        self.assertEqual(data.get('success'), True, "Failed to add device")

    def tearDown(self):
        print('Delete Device')
        response = requests.delete(url=f'{host}/devices/{td.device_data1.get("id")}')
        data = response.json()
        self.assertEqual(response.status_code, 200, "Failed to delete device")
        self.assertEqual(data.get('success'), True, "Failed to delete device")

    def test_device_endpoints(self):
        print("\ntest_device_endpoints:")

        # Get Devices
        print("Get Devices")
        response = requests.get(url=f'{host}/devices/')
        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 1)

        # Delete Device
        print('Delete Device')
        response = requests.delete(url=f'{host}/devices/{td.device_data1.get("id")}')
        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data.get('success'), True)

        # Get Devices Again
        print('Get Devices Again')
        response = requests.get(url=f'{host}/devices')
        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 0)

    def test_config_endpoints(self):
        print('\ntest_config_endpoints')
        #  Add Config
        print('Add Config')
        device_id = td.device_data1.get('id')
        response = requests.post(url=f'{host}/devices/{device_id}/config', json=td.test_config)
        data = response.json()
        config = data.get('config')
        self.assertEqual(response.status_code, 200)
        ssid = config.get('config').get('wifi').get('ssid')
        self.assertEqual(ssid, 'the_interwebs')

        #  Update Config
        print('Update Config')
        response = requests.put(url=f'{host}/devices/{device_id}/config', json=td.test_config2)
        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data.get('success'), True)

        #  Get Updated Config
        print('Get Updated Config')
        response = requests.get(url=f'{host}/devices/{device_id}/config')
        data = response.json()
        ssid = data.get('config').get('wifi').get('ssid')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(ssid, 'the_other_webs')

        #  Delete Config
        print('Delete Config')
        response = requests.delete(url=f'{host}/devices/{device_id}/config', json=td.test_config2)
        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data.get('success'), True)

    def test_sensor_endpoints(self):
        print('\ntest_sensor_endpoints')
        device_id = td.device_data1.get('id')

        # Add Config
        print('Add Config')
        response = requests.post(url=f'{host}/devices/{device_id}/config', json=td.test_config)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        config_id = data['config'].get('id')

        # Add Weather Sensor
        print('Add Weather Sensor')
        sensor = td.test_weather_sensor
        sensor.update({"device_config_id": config_id})
        response = requests.post(url=f'{host}/sensors/add', json=sensor)
        self.assertEqual(response.status_code, 200)
        device_sensor = response.json()
        self.assertEqual(device_sensor["sensor"]["sensor_config"]["pin"], 28)
        weather_sensor_id = device_sensor["sensor"]['id']

        # Add Motion Sensor
        print('Add Motion Sensor')
        sensor = td.test_motion
        sensor.update({"device_config_id": config_id})
        response = requests.post(url=f'{host}/sensors/add', json=sensor)
        self.assertEqual(response.status_code, 200)
        device_sensor = response.json()
        self.assertEqual(device_sensor["sensor"]["sensor_config"]["pin"], 27)
        motion_sensor_id = device_sensor["sensor"]['id']

        # Add LED
        print('Add LED')
        sensor = td.test_led
        sensor.update({"device_config_id": config_id})
        response = requests.post(url=f'{host}/sensors/add', json=sensor)
        self.assertEqual(response.status_code, 200)
        device_sensor = response.json()
        self.assertEqual(device_sensor["sensor"]["sensor_config"]["pin"], 4)
        led_id = device_sensor["sensor"]['id']

        print('Delete all added stuff')
        response = requests.delete(url=f'{host}/sensors/{led_id}')
        self.assertEqual(response.status_code, 200)
        response = requests.delete(url=f'{host}/sensors/{weather_sensor_id}')
        self.assertEqual(response.status_code, 200)
        response = requests.delete(url=f'{host}/sensors/{motion_sensor_id}')
        self.assertEqual(response.status_code, 200)
        response = requests.delete(url=f'{host}/devices/{device_id}/config')
        self.assertEqual(response.status_code, 200)

    def test_log_endpoints(self):
        print('\ntest_sensor_endpoints')
        device_id = td.device_data1.get('id')

        response = requests.get(url=f'{host}/logs/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 0)

        log1 = td.test_log1
        log2 = td.test_log1
        log1.update({"device_id": device_id})
        log2.update({"device_id": device_id})
        response = requests.post(url=f'{host}/logs/add', json=log1)
        self.assertEqual(response.status_code, 200)
        response = requests.post(url=f'{host}/logs/add', json=log2)
        self.assertEqual(response.status_code, 200)

        response = requests.get(url=f'{host}/logs/')
        logs = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(logs), 2)
        print(logs)

        for i in logs:
            response = requests.delete(url=f'{host}/logs/entries/{i["id"]}')
            self.assertEqual(response.status_code, 200, "Failed to delete Log")


if __name__ == "__main__":
    unittest.main()
