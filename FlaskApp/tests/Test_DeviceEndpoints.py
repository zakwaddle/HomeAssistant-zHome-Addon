import unittest
import requests
import tests.test_data as td

host = 'http://localhost:5000/api/home'
"""
These tests still don't really work how I'd like them to. 
However, I'm not sure how exactly I'd like them to work.
"""


class DeviceEndpointsTestCase(unittest.TestCase):
    device_id = 'test_device_1'

    # @classmethod
    # def setUpClass(cls):
    #     print("Setup for tests")
    #     cls.device_id = None

    @classmethod
    def tearDownClass(cls):
        print("Tear down for tests")
        # if cls.device_id is not None:
        print('Delete Device')
        response = requests.delete(url=f'{host}/devices/{cls.device_id}')
        data = response.json()
        print(response.status_code)
        cls.assertEqual(response.status_code, 200, "Failed to delete device")
        cls.assertEqual(data.get('success'), True, "Failed to delete device")

    def test_add_device(self):
        print('Add Device')
        response = requests.post(url=f'{host}/devices/add', json=td.device_data1)
        data = response.json()
        self.assertEqual(response.status_code, 200, "Failed to add device")
        self.assertEqual(data.get('success'), True, "Failed to add device")
        self.assertIsNotNone(data.get('device'), "No device data returned")
        self.device_id = data.get('device').get('id')

    def test_get_all_devices(self):
        print('Get all devices')
        response = requests.get(url=f'{host}/devices')
        data = response.json()
        self.assertEqual(response.status_code, 200, "Failed to fetch devices")
        self.assertIsInstance(data, list, "Data returned is not a list")

    def test_get_device_sensors(self):
        print('Get device sensors')
        response = requests.get(url=f'{host}/devices/{self.device_id}/sensors')
        data = response.json()
        print(data)
        self.assertEqual(response.status_code, 200, "Failed to fetch device sensors")
        self.assertIsInstance(data, list, "Data returned is not a list")

    # def test_delete_device(self):
    #     print('Delete Device')
    #     response = requests.delete(url=f'{host}/devices/{self.device_id}')
    #     data = response.json()
    #     self.assertEqual(response.status_code, 200, "Failed to delete device")
    #     self.assertEqual(data.get('success'), True, "Failed to delete device")


if __name__ == '__main__':
    unittest.main()
