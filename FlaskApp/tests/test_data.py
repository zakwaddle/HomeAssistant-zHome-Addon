device_data1 = {
    "id": "test_device_1",
    "platform": "rp2",
    "display_name": "test_device_1",
    "device_info": {
        "name": "test_device_1",
        "manufacturer": "ZRW",
        "model": "RP2-Circuit",
        "identifiers": "test_device_1"
    }
}
test_config = {

    "wifi": {
        "ssid": "the_interwebs",
        "password": "935Ravine"
    },
    "mqtt": {
        "server": "homeassistant.local",
        "port": 1883,
        "username": "Zak",
        "password": "935Ravine"
    },
    "ftp": {
        "host": "homeassistant.local",
        "user": "microcontrollers",
        "password": "microcontrollers"
    }

}
test_config2 = {

    "wifi": {
        "ssid": "the_other_webs",
        "password": "935Ravine"
    },
    "mqtt": {
        "server": "homeassistant.local",
        "port": 1883,
        "username": "Zak",
        "password": "935Ravine"
    },
    "ftp": {
        "host": "homeassistant.local",
        "user": "microcontrollers",
        "password": "microcontrollers"
    }

}
test_weather_sensor = {
    "sensor_type": "weather",
    "name": "Bedroom Weather",
    "device_config_id": None,
    "sensor_config": {
        "pin": 28,
        "measurement_interval_ms": 10000
    }
}
test_led = {
    "sensor_type": "led",
    "device_config_id": None,
    "name": "Shelf Lights",
    "sensor_config": {
        "pin": 4,
        "freq": 300,
        "fade_time_ms": 4,
        "brightness_scale": 255
    }
}

test_motion = {
    "sensor_type": "motion",
    "device_config_id": None,
    "name": "Nook Motion",
    "sensor_config": {
        "pin": 27,
        "retrigger_delay_ms": 120000,
    }
}

test_log1 = {
  "device_id": None,
  "topic": "test/topic",
  "log": {
    "message": "bla bla bla",
    "type": "info"
  }
}
test_log2 = {
  "device_id": None,
  "topic": "test/topic",
  "log": {
    "message": "blo blo blo blo",
    "type": "update"
  }
}
