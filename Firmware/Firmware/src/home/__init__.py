from .Home import Home
import utime

__version__ = '0.0.9'


def run():
    while True:
        home_client = Home()
        try:

            print('Home Version: ', __version__)
            home_client.start_sequence()
            home_client.log("---listening for messages---")
            while True:
                home_client.check_msg()
                utime.sleep_ms(100)

        except KeyboardInterrupt:
            Home.status_led_off()
            raise KeyboardInterrupt
        except Exception as e:
            home_client.restart_on_error(f'Main Loop Error: \n\t{e}')
