import machine
import time
import utime
# from pico_oled_i2c import PicoOLED
from pico_oled import PicoOLED
import home


keyA = machine.Pin(15, machine.Pin.IN, machine.Pin.PULL_UP)
keyB = machine.Pin(17, machine.Pin.IN, machine.Pin.PULL_UP)
OLED = PicoOLED()

WHITE = 0xffff
BLACK = 0x0000

def blank():
    OLED.fill(BLACK)
    OLED.show()

def press_the_button():
    OLED.fill_rect(0,22,128,20,OLED.white)
    OLED.text("press the button",0,28,OLED.black)

def key_a_is_pressed():
    return keyA.value() == 0

def key_b_is_pressed():
    return keyB.value() == 0

def get_ms(t1, t2):
    return time.ticks_diff(t1, t2)

def check_key_a():
    if key_a_is_pressed():
        t1 = time.ticks_ms()
        while key_a_is_pressed():
            time.sleep(0.1)
        t2 = time.ticks_ms()
        ms = get_ms(t2, t1)
        if ms > 500:
            print("key a long press", ms)
        else:
            print("key a ", ms)

def check_key_b():
    if key_b_is_pressed():
        t1 = time.ticks_ms()
        while key_b_is_pressed():
            time.sleep(0.1)
        t2 = time.ticks_ms()
        ms = get_ms(t2, t1)
        if ms > 500:
            print("key b long press", ms)
        else:
            print("key b ", ms)


def text(input_text):
    OLED.text(input_text,1,46,WHITE)
    OLED.text(input_text,1,56,WHITE)
    
def menu_text(menu_text):
    OLED.fill_rect(0, 0, 128, 12, WHITE)
    OLED.text(menu_text,1,2,BLACK)
    
def line1_text(input_text):
    OLED.fill_rect(0, 13, 128, 12, BLACK)
    OLED.text(input_text,1,16,WHITE)

def line2_text(input_text):
    OLED.fill_rect(0, 24, 128, 12, BLACK)
    OLED.text(input_text,1,26,WHITE)
    
def line3_text(input_text):
    OLED.fill_rect(0, 34, 128, 12, BLACK)
    OLED.text(input_text,1,36,WHITE)
    
def line4_text(input_text):
    OLED.fill_rect(0, 44, 128, 12, BLACK)
    OLED.text(input_text,1,46,WHITE)
    
def line5_text(input_text):
    OLED.fill_rect(0, 54, 128, 12, BLACK)
    OLED.text(input_text,1,56,WHITE)
    
    
def show():
    OLED.show()
    

def setup_screen():
    blank()
    menu_text("stupid")
    line1_text("dumb guy")
    line2_text("fart guy")
    #line3_text("really tall guy")
    line4_text("poop")
    line5_text("weather: 68 F")    
    show()


def update_henry_temp(new_temp):
    line1_text(f"henry's room:")
    line2_text(f" {new_temp} F")

def update_garage_temp(new_temp):
    line4_text("garage:")
    line5_text(f" {new_temp} F")

def to_f_degree(c):
    return round(c * (9/5) + 32, 1)

henry_temp = "homeassistant/sensor/henry_weather/weather-temperature"
garage_temp = "homeassistant/sensor/garage/garageweather-temperature"

def on_msg(topic, msg):
    topic = topic.decode("utf-8")
    msg = msg.decode("utf-8")
    if topic == henry_temp:
        msg = to_f_degree(float(msg))
        #print("got henry temp: ", msg)
        update_henry_temp(msg)
    if topic == garage_temp:
        msg = to_f_degree(float(msg))
        #print("got garage temp: ", msg)
        update_garage_temp(msg)
    show()
        

if __name__=='__main__':
    home_client = home.Home()
    try:
        
        setup_screen()
        home_client.add_subscriptions(
            garage_temp,
            henry_temp
            )
        home_client.set_msg_observer(on_msg)
        # print('Home Version: ', __version__)
        home_client.start_sequence()
        home_client.log("---listening for messages---")
        while True:
            home_client.check_msg()
            check_key_a()
            check_key_b()
            utime.sleep_ms(100)

    except KeyboardInterrupt:
        Home.status_led_off()
        raise KeyboardInterrupt
    except Exception as e:
        home_client.restart_on_error(f'Main Loop Error: \n\t{e}')
    

        
            
    
 

