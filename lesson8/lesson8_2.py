from machine import pin
from time import sleep

but_pin = 14
button = Pin(btn_pin,Pin_IN,Pin.PULL_UP)

while(True ):
    print(button.value())
    sleep(1)
#led_14 = pin.Pin(14, leds.Pin.IN)
#led_15 = pin.Pin(15, leds.Pin.OUT)