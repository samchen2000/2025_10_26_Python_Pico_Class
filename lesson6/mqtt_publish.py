"""
MQTT Publish 應用程式
使用 paho-mqtt 套件發布訊息到 MQTT Broker
"""

import sys
# 添加系統套件路徑（如果套件安裝在系統目錄）
sys.path.insert(0, '/usr/lib/python3/dist-packages')

import paho.mqtt.client as mqtt
import time
import json

# MQTT 設定
MQTT_BROKER = "localhost"  # MQTT Broker 地址
MQTT_PORT = 1883           # MQTT 連接埠（默認是 1883）
#MQTT_TOPIC = "test/topic"  # 發布的主題
MQTT_TOPIC = "客廳/溫度"  # 發布的主題
MQTT_CLIENT_ID = "publisher_001"  # 客戶端 ID

# 連接回調函數
def on_connect(client, userdata, flags, rc):
    """
    當客戶端連接到 Broker 時的回調函數
    
    rc: 連接結果碼
    0: 連接成功
    1: 連接失敗 - 協議版本不正確
    2: 連接失敗 - 客戶端 ID 無效
    3: 連接失敗 - 伺服器無法使用
    4: 連接失敗 - 用戶名或密碼錯誤
    5: 連接失敗 - 未授權
    """
    if rc == 0:
        print(f"✓ 成功連接到 MQTT Broker: {MQTT_BROKER}:{MQTT_PORT}")
    else:
        print(f"✗ 連接失敗，錯誤碼: {rc}")

# 發布回調函數
def on_publish(client, userdata, mid):
    """
    當訊息發布成功時的回調函數
    
    mid: 訊息 ID
    """
    print(f"✓ 訊息已發布 (訊息 ID: {mid})")

# 斷線回調函數
def on_disconnect(client, userdata, rc):
    """當客戶端斷線時的回調函數"""
    print("已斷開連接")

def publish_message(client, topic, message):
    """
    發布訊息到指定的主題
    
    :param client: MQTT 客戶端物件
    :param topic: 主題名稱
    :param message: 要發布的訊息（字串）
    """
    result = client.publish(topic, message, qos=1)
    
    # 檢查發布狀態
    status = result[0]
    if status == 0:
        print(f"發送訊息到主題 '{topic}': {message}")
    else:
        print(f"發送失敗，狀態碼: {status}")

def main():
    """主程式"""
    # 創建 MQTT 客戶端
    client = mqtt.Client(client_id=MQTT_CLIENT_ID)
    
    # 設置回調函數
    client.on_connect = on_connect
    client.on_publish = on_publish
    client.on_disconnect = on_disconnect
    
    try:
        # 連接到 MQTT Broker
        print(f"正在連接到 MQTT Broker: {MQTT_BROKER}:{MQTT_PORT}...")
        client.connect(MQTT_BROKER, MQTT_PORT, keepalive=60)
        
        # 啟動網路循環（在背景執行）
        client.loop_start()
        
        # 等待連接建立
        time.sleep(1)
        
        # 範例 1: 發布簡單文字訊息
        print("\n--- 範例 1: 發布簡單文字訊息 ---")
        publish_message(client, MQTT_TOPIC, "Hello from MQTT Publisher!")
        time.sleep(1)
        
        # 範例 2: 發布 JSON 格式訊息
        print("\n--- 範例 2: 發布 JSON 格式訊息 ---")
        sensor_data = {
            "device_id": "sensor_001",
            "temperature": 25.5,
            "humidity": 60.0,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        json_message = json.dumps(sensor_data, ensure_ascii=False)
        publish_message(client, MQTT_TOPIC, json_message)
        time.sleep(1)
        
        # 範例 3: 連續發布多筆訊息
        print("\n--- 範例 3: 連續發布多筆訊息 ---")
        for i in range(5):
            message = f"訊息編號: {i+1}, 時間: {time.strftime('%H:%M:%S')}"
            publish_message(client, MQTT_TOPIC, message)
            time.sleep(1)
        
        # 等待所有訊息發送完成
        time.sleep(2)
        
        # 停止網路循環並斷線
        client.loop_stop()
        client.disconnect()
        
        print("\n✓ 程式執行完成")
        
    except Exception as e:
        print(f"✗ 發生錯誤: {e}")
        client.loop_stop()
        client.disconnect()

if __name__ == "__main__":
    main()

