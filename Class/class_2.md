### 安裝Cursor
1. 安裝網址 :
https://cursor.com/zh-Hant/download  


### 在 Raspberry Pi 上安裝 MQTT Broker
1. 在開始之前，先更新套件：
```
sudo apt update && sudo apt upgrade -y
```
2. 安裝 Mosquitto Broker
```
sudo apt install -y mosquitto mosquitto-clients
```
3. 安裝完成後，Mosquitto 通常會自動啟動並設為開機自動啟動。
檢查狀態:
```
sudo systemctl status mosquitto
```
4. 如果沒有啟動，可以手動啟動：
```
sudo systemctl enable mosquitto
sudo systemctl start mosquitto
```
5. 測試 MQTT 功能
. 視窗 1：訂閱一個主題
```
mosquitto_sub -h localhost -t test/topic
```
. 視窗 2：發佈訊息
```
mosquitto_pub -h localhost -t test/topic -m "Hello from Raspberry Pi!"
```

### 安裝 MQTTX
1. 安裝網址: 
https://mqttx.app/downloads

### 老師推薦安裝 Affinity & Canva
1. 安裝網址 : (Affinity)
https://www.affinity.studio/get-affinity

2. 使用網址 : (Canva)
https://www.canva.com/zh_tw/
