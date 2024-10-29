from .Home import Home, run
# import utime
# import sys


# def run():
#     while True:
#         home_client = Home()
#         try:
#             home_client.start_sequence()
#             home_client.log("---listening for messages---")
#             while True:
#                 home_client.check_msg()
#                 utime.sleep_ms(100)

#         except KeyboardInterrupt:
#             Home.status_led_off()
#             raise KeyboardInterrupt
#         except Exception as e:
#             home_client.restart_on_error(f'Main Loop Error: \n\t{sys.print_exception(e)}')
