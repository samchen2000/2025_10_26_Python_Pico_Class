import time
import utime
import machine as leds  #將machine 改另一個名稱來替代,但使用原本名稱也可以,兩者都可以用.

led = leds.Pin("LED", leds.Pin.OUT)
led_15 = leds.Pin(15, leds.Pin.OUT)

def samchen():
    brled = leds.PWM(leds.Pin(led_15))
    brled.freq(1000)
    led_val = 0
    led_step = 5
    cont_1 = 0
    led_15.value(1)
    led.value(0)
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
        time.sleep(0.07)
        if cont_1 >= 100:
            brled.deinit()
            time.sleep(1)
            led_15.value(0)
            #led_16.value(0)
            break      
    print("增加呼吸燈")
while True:
    led_15.value(0)
    led.value(1)
    time.sleep(2)
    led.value(0)
    samchen()

print("設定完成")
