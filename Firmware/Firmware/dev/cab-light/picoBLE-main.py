"""
PICO
"""

import uasyncio as asyncio
import aioble
import bluetooth
import struct
from MotionSensor import MotionSensor
from StatusLED import StatusLED

LIGHT_SERVICE_UUID = bluetooth.UUID(0x00A1)
LIGHT_STATE_UUID = bluetooth.UUID(0x00A2)
SENSOR_POLLING_INTERVAL_MS = 100
BT_UPDATE_INTERVAL_MS = 100

led = StatusLED()
motion = MotionSensor(16, 3000)

lock = asyncio.Lock()
last_val = None


def encode_motion(val):
    return struct.pack("<h", val)


async def find_motion_light():
    # Scan for 5 seconds, in active mode, with very low interval/window (to
    # maximise detection rate).
    print("scanning")
    async with aioble.scan(5000, interval_us=30000, window_us=30000, active=True) as scanner:
        async for result in scanner:
            # See if it matches our name and the motion sensing service.
            if result.name() == "mpy-motion-light" and LIGHT_SERVICE_UUID in result.services():
                return result.device
    return None


async def sensor_task():
    while True:
        global last_val

        current_motion = motion.poll()
        async with lock:
            if last_val != current_motion:
                last_val = current_motion
        led.led_pin.value(last_val)
        await asyncio.sleep_ms(SENSOR_POLLING_INTERVAL_MS)


async def connect_light():
    device = await find_motion_light()
    if not device:
        print("Light not found")
        return

    try:
        print("Connecting to", device)
        connection = await device.connect()
        return connection

    except asyncio.TimeoutError:
        print("Timeout during connection")
        return


async def get_light(connection):
    try:
        light_service = await connection.service(LIGHT_SERVICE_UUID)
        light_characteristic = await light_service.characteristic(LIGHT_STATE_UUID)
        print(light_characteristic)
        return light_characteristic
    except asyncio.TimeoutError:
        print("Timeout discovering services/characteristics")
        return


async def manage_connection():
    last_sent_val = None
    while True:
        connection = await connect_light()
        if connection:
            async with connection:
                light_characteristic = await get_light(connection)
                if light_characteristic:
                    await light_characteristic.write(encode_motion(last_val))
                    print("initial value sent: ", last_val)
                    while connection.is_connected():
                        async with lock:
                            if last_sent_val != last_val:
                                try:
                                    await light_characteristic.write(encode_motion(last_val))
                                    last_sent_val = last_val
                                    print("write to light: ", last_sent_val, "\n")
                                except Exception as e:
                                    print("error: ", e)
                        await asyncio.sleep_ms(BT_UPDATE_INTERVAL_MS)
        print("lost light connection")
        await asyncio.sleep_ms(5000)


async def main():
    t1 = asyncio.create_task(sensor_task())
    t2 = asyncio.create_task(manage_connection())
    await asyncio.gather(t1, t2)


asyncio.run(main())
