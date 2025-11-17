import network
import urequests as requests
import time
import rp2
from machine import WDT
import ujson
import urequests
import utime

rp2.country('TW') #設定我們的wifi的地區是台灣(可以不設)

ssid = 'A590301'
password = 'A590301AA'

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)
wlan.config(pm = 0xa11140) #預設是省電模式,可以設為非省電模式

def connect():  
    #等待連線或失敗
    #status=0,1,2正在連線
    #status=3連線成功
    #<1,>=3失敗的連線
    max_wait = 10    

    while max_wait > 0:
        status = wlan.status()
        if status < 0 or status >= 3:
            break
        max_wait -= 1
        print("等待連線")
        time.sleep(1)

    #處理錯誤
    if wlan.status() != 3:
        print('連線失敗,重新開機')
        #raise RuntimeError('連線失敗') #開發階段,出現錯誤,中斷執行
        wdt = WDT(timeout=2000) #無連接電腦時,重新開機(成品時,請使用這個)
        wdt.feed()
    else:
        print('連線成功')
        status = wlan.ifconfig()
        print(f'ip={status[0]}') 
        
        
def reconnect():
    if wlan.status() == 3: #還在連線,只是傳送的server無回應
        print(f"無法連線({wlan.status()})")
        return
    else:
        print("嘗試重新連線")
        wlan.disconnect()
        wlan.connect(ssid, password)
        connect() #再連線一次

def send_json(json_data, url, headers=None):
    """
    發送JSON數據到指定URL
    
    :param json_data: 要發送的JSON數據(字典或列表)
    :param url: 目標URL
    :param headers: 可選的HTTP頭部(字典)
    :return: 響應對象
    """
    try:
        json_string = ujson.dumps(json_data)
        headers = {'Content-Type': 'application/json'}
        response = urequests.post(url, data=json_string, headers=headers)
        return response
    except Exception as e:
        print("Error sending JSON:", e)
        return None

def create_sensor_data(temperature=None, light=None, humidity=None):
    """
    創建包含傳感器數據的字典
    
    :param temperature: 溫度值 (可選)
    :param light: 光敏值 (可選)
    :param humidity: 濕度值 (可選)
    :return: 包含傳感器數據的字典
    """
    data = {}
    if temperature is not None:
        data["temperature"] = temperature
    if light is not None:
        data["light"] = light
    if humidity is not None:
        data["humidity"] = humidity
    return data

def get_formatted_time():
    """
    獲取格式化的時間字符串
    
    :return: 格式為 "yyyy-MM-dd HH:mm:ss" 的時間字符串
    """
    t = utime.localtime()
    return "{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(
        t[0], t[1], t[2], t[3], t[4], t[5]
    )

def optimize_json_data(data):
    """
    優化 JSON 數據以減少大小
    
    :param data: 原始數據（可以是字典或 JSON 字符串）
    :return: 優化後的數據字典
    """
    # 如果輸入是字符串，先將其解析為字典
    if isinstance(data, str):
        try:
            data = ujson.loads(data)
        except ValueError:
            print("Error: Invalid JSON string")
            return {}

    # 現在我們確保 data 是一個字典
    if not isinstance(data, dict):
        print("Error: Input must be a dictionary or a valid JSON string")
        return {}

    optimized = {}
    for key, value in data.items():
        # 移除空值
        if value is not None and value != "":
            # 縮短鍵名
            short_key = key[:3]  # 使用鍵名的前三個字符
            # 如果是浮點數，限制小數位數
            if isinstance(value, float):
                optimized[short_key] = round(value, 2)
            else:
                optimized[short_key] = value
    return optimized

def create_json_payload(sensor_data, device_id="pico01"):
    """
    創建完整的 JSON 數據包
    
    :param sensor_data: 傳感器數據字典
    :param device_id: 設備 ID (可選)
    :return: JSON 字串
    """
    
    payload = {
        #"device_id": device_id,
        #"timestamp": get_formatted_time(),  # 你可能需要一個實際的時間戳
        "sensors": sensor_data
    }
    return ujson.dumps(payload)

def calculate_temperature(value:int):
    '''
    溫度轉換
    
    :param 感應器參數
    '''
    conversion_factor = 3.3 / (65535)
    reading = value * conversion_factor
    temperature = 27 - (reading - 0.706)/0.001721
    return temperature
