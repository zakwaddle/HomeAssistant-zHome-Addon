"""
ESP32
"""

import uasyncio as asyncio
import aioble
import bluetooth
import struct
from StatusLED import StatusLED
from DimmableLED import DimmableLight

PIN = 27
L_PIN = 26

LIGHT_SERVICE_UUID = bluetooth.UUID(0x00A1)
LIGHT_STATE_UUID = bluetooth.UUID(0x00A2)
ADV_INTERVAL_US = 250_000

# Register GATT server.
light_service = aioble.Service(LIGHT_SERVICE_UUID)
light_characteristic = aioble.Characteristic(
    light_service, LIGHT_STATE_UUID, read=True, write=True, capture=True
)
aioble.register_services(light_service)

led = StatusLED()
light = DimmableLight(L_PIN, timer_n=2, fade_time_ms=6)


async def peripheral_task():
    while True:
        print("advertising")
        async with await aioble.advertise(
                ADV_INTERVAL_US,
                name="mpy-motion-light",
                services=[LIGHT_SERVICE_UUID],
        ) as connection:
            print("Connection from", connection.device)
            led.on()
            while connection.is_connected():
                try:
                    data = await light_characteristic.written(timeout_ms=3000)
                    if data:
                        val = struct.unpack("<h", data[1])[0]
                        print("received: ", val)
                        light.target_brightness = val * 100
                        light.fade()
                except asyncio.TimeoutError:
                    pass
            print("device disconnected")
            led.off()


async def main():
    t1 = asyncio.create_task(peripheral_task())
    await asyncio.gather(t1)


asyncio.run(main())

