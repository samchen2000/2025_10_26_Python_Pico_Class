import time
import utime
import machine as leds  #將machine 改另一個名稱來替代,但使用原本名稱也可以,兩者都可以用.
import machine as joystick
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
led_15 = leds.Pin(15, leds.Pin.OUT)
led_teams = [led, led_16, led_17, led_18, led_19, led_15]
X_axis = joystick.ADC(26)
Y_axis = joystick.ADC(27)
press = joystick.Pin(22, machine.Pin.IN, machine.Pin.PULL_UP)
cont = 0
def samchen():
    brled = leds.PWM(leds.Pin(led_16))
    brled.freq(1000)
    led_val = 0
    led_step = 5
    cont_1 = 0
    led_15.value(1)
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
        if cont_1 >= 100:
            brled.deinit()
            time.sleep(1)
            led_15.value(0)
            led_16.value(0)
            break      
    print("增加呼吸燈")

def gogo(a, b):
    print(f"user : {a} , player : {b} ")

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
while True:
    X_axis_value = X_axis.read_u16()
    Y_axis_value = Y_axis.read_u16()
    if X_axis_value <= 600:
        led_16.value(1)
        print("X: "+"Left\t\t"+ str(X_axis_value), end='----')
    elif X_axis_value >= 60000:
        led_17.value(1)
        print("X: "+"Right\t"+ str(X_axis_value), end='----')
    elif 600 < X_axis_value < 60000:
        print("X: "+"Middle : \t"+ str(X_axis_value), end='----')        
 
    if Y_axis_value <= 600:
        led_18.value(1)
        print("Y: "+"Down : "+ str(Y_axis_value))
    elif Y_axis_value >= 60000:
        led_19.value(1)
        print("Y: "+"Up : "+ str(Y_axis_value))
    elif 600 < Y_axis_value < 60000:
        print("Y: "+"Middle : "+ str(Y_axis_value))
 
    if press.value() == 0:
        samchen()
        print("Pressed")
         
    utime.sleep(0.2)
    for i in led_teams:
        i.value(0)

        
#samchen()
print("設定完成")
