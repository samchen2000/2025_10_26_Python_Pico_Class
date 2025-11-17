import time
import machine as leds  #將machine 改另一個名稱來替代,但使用原本名稱也可以,兩者都可以用.
#led = Pin(25, Pin.OUT)
#while True:
   # print("Hello Pico!!!")
   # led.value(1)
   # time.sleep(3)
   # led.value(0)
   # time.sleep(1)
led = leds.Pin("LED", leds.Pin.OUT)
led_16 = leds.Pin(16, leds.Pin.OUT)
led_17 = leds.Pin(17, leds.Pin.OUT)
led_18 = leds.Pin(18, leds.Pin.OUT)
led_19 = leds.Pin(19, leds.Pin.OUT)
led_teams = [led, led_16, led_17, led_18, led_19]
cont = 0
while True:
    for i in led_teams:
        i.value(1)
        time.sleep(0.1)
        i.value(0)
    cont += 1
    print(f"Run : {cont}")
    if cont >= 10:
        led.value(0)
        led_16.value(0)
        led_17.value(0)
        led_18.value(0)
        led_19.value(0)
        cont = 0
        break

def samchen():
    brled = leds.PWM(leds.Pin(led_16))
    brled.freq(1000)
    led_val = 0
    led_step = 5
    cont_1 = 0
    while True :
        led_val += led_step
        if led_val >= 100:
            led_val = 100
            led_step = -5
        elif led_val <= 0:
            led_val = 0
            led_step = 5
        brled.duty_u16(int(led_val * 500))
        cont_1 += 1
        print(f"Run : {cont_1}")
        time.sleep(0.05)
        if cont_1 >= 200:
            brled.deinit()
            led_16.value(0)
            break      
    print("增加呼吸燈")

def gogo(a, b):
    print(f"user : {a} , player : {b} ")

        
samchen()
print("設定完成")

