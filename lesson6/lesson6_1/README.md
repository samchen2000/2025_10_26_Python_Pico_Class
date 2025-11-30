# MQTT 感測器監控應用程式

根據 [PRD.md](PRD.md) 規格實作的感測器數據即時監控儀表板。

## 📋 專案說明

本專案實作一個基於 Web 的 MQTT 監控系統，用於即時顯示和記錄感測器數據。

### ⚠️ 技術變更說明

由於 Streamlit 及其依賴套件（pandas, pyarrow）與 Raspberry Pi ARM64 架構存在相容性問題（SIGILL 錯誤），專案改用 **Flask + Socket.IO** 實作，提供更好的效能和穩定性。

## ✨ 主要功能

- 💡 **即時電燈狀態顯示** - 大型圓形視覺化指示器
- 🌡️ **客廳溫度監控** - 即時數值顯示和歷史趨勢
- 💧 **客廳濕度監控** - 即時數值顯示和歷史趨勢
- 📈 **雙 Y 軸歷史圖表** - 互動式數據視覺化
- 💾 **自動數據儲存** - CSV 和 Excel 格式
- 🔄 **WebSocket 即時推送** - 無需手動重新整理
- 📱 **響應式設計** - 支援手機和桌面瀏覽器

## 🚀 快速開始

### 方式 1：使用啟動腳本（推薦）

```bash
cd /home/pi/Documents/GitHub/2025_10_26_chihlee_pi_pico/lesson6
./start.sh
```

### 方式 2：手動啟動

```bash
cd /home/pi/Documents/GitHub/2025_10_26_chihlee_pi_pico/lesson6
uv run python app_flask.py
```

### 開啟網頁

在瀏覽器中訪問：
- 本地：http://localhost:8080
- 區域網路：http://172.20.10.3:8080

## 📊 測試數據

專案已包含 50 筆測試數據，啟動後即可看到完整的數據和圖表。

### 重新生成測試數據

```bash
uv run python generate_test_data.py
```

### 發送即時 MQTT 測試數據

在另一個終端機中執行：

```bash
uv run python test_mqtt_publish.py
```

## 📁 檔案結構

### ✅ 主要檔案（可用）

| 檔案 | 說明 |
|------|------|
| `app_flask.py` | **Flask 主應用程式**（推薦使用） |
| `templates/index.html` | 網頁前端介面 |
| `sensor_data.csv` | CSV 格式數據檔案 |
| `sensor_data.xlsx` | Excel 格式數據檔案 |
| `test_mqtt_publish.py` | MQTT 測試發布工具 |
| `generate_test_data.py` | 測試數據生成工具 |
| `start.sh` | 應用程式啟動腳本 |
| `PRD.md` | 產品需求文件 |
| `啟動應用程式.md` | 詳細使用說明 |
| `使用說明.md` | 技術細節和故障排除 |

### ⚠️ 已棄用檔案（相容性問題）

| 檔案 | 狀態 |
|------|------|
| `app.py` | ❌ Streamlit 版本（ARM 不相容） |
| `config.py`, `data_manager.py`, `mqtt_client.py` | ⚠️ 僅供 Streamlit 版本使用 |

## 🔧 MQTT 設定

### 確認 MQTT Broker 運行中

```bash
# 檢查 mosquitto 狀態
sudo systemctl status mosquitto

# 啟動 mosquitto
sudo systemctl start mosquitto

# 設定開機自動啟動
sudo systemctl enable mosquitto
```

### MQTT 訊息格式

發送到主題 `客廳/感測器` 的訊息應為 JSON 格式：

```json
{
  "temperature": 25.5,
  "humidity": 60.0,
  "light_status": "開"
}
```

支援的欄位名稱：
- 溫度：`temperature` 或 `temp`
- 濕度：`humidity` 或 `humi`
- 電燈：`light_status` 或 `light`

## 📱 Pico 裝置 MQTT 訊息格式

### 方式 1：單一主題發送（推薦）

發送到主題 `客廳/感測器`，包含所有資料的 JSON 格式：

```json
{
  "temperature": 25.5,
  "humidity": 60.0,
  "light_status": "開"
}
```

**Pico MicroPython 程式碼範例：**

```python
import network
import time
from umqtt.simple import MQTTClient
import ujson

# WiFi 設定
WIFI_SSID = "您的WiFi名稱"
WIFI_PASSWORD = "您的WiFi密碼"

# MQTT 設定
MQTT_BROKER = "192.168.1.100"  # Raspberry Pi 的 IP 地址
MQTT_PORT = 1883
MQTT_CLIENT_ID = "pico_sensor_001"
MQTT_TOPIC = "客廳/感測器"

def connect_wifi():
    """連接 WiFi"""
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(WIFI_SSID, WIFI_PASSWORD)
    
    max_wait = 10
    while max_wait > 0:
        if wlan.status() < 0 or wlan.status() >= 3:
            break
        max_wait -= 1
        time.sleep(1)
    
    if wlan.status() != 3:
        raise RuntimeError('WiFi 連接失敗')
    print('WiFi 連接成功')

def send_sensor_data(client, temp, hum, light_status):
    """發送感測器資料"""
    data = {
        "temperature": temp,
        "humidity": hum,
        "light_status": "開" if light_status else "關"
    }
    json_data = ujson.dumps(data)
    client.publish(MQTT_TOPIC, json_data)
    print(f"已發送: {json_data}")

# 主程式
connect_wifi()
client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, MQTT_PORT)
client.connect()

while True:
    # 從感測器讀取資料（需根據實際硬體調整）
    temperature = 25.5  # 從感測器讀取
    humidity = 60.0     # 從感測器讀取
    light_on = True     # 從 GPIO 讀取
    
    send_sensor_data(client, temperature, humidity, light_on)
    time.sleep(5)  # 每 5 秒發送一次
```

### 方式 2：分別發送到不同主題

可以分別發送到三個獨立主題：

| 主題 | 說明 | 訊息格式 |
|------|------|---------|
| `客廳/溫度` | 溫度資料 | `25.5` 或 `{"temperature": 25.5}` |
| `客廳/濕度` | 濕度資料 | `60.0` 或 `{"humidity": 60.0}` |
| `客廳/電燈` | 電燈狀態 | `"開"` 或 `{"status": "開"}` |

**Pico 程式碼範例（分別發送）：**

```python
# 主題設定
TOPIC_TEMP = "客廳/溫度"
TOPIC_HUM = "客廳/濕度"
TOPIC_LIGHT = "客廳/電燈"

# 發送溫度（純文字格式）
client.publish(TOPIC_TEMP, str(temperature))

# 發送濕度（純文字格式）
client.publish(TOPIC_HUM, str(humidity))

# 發送電燈狀態（純文字格式）
client.publish(TOPIC_LIGHT, "開" if light_on else "關")

# 或使用 JSON 格式
# temp_data = {"temperature": temperature}
# client.publish(TOPIC_TEMP, ujson.dumps(temp_data))
```

### 電燈狀態格式支援

電燈狀態支援多種格式：

| 格式類型 | 範例值 |
|---------|--------|
| 中文 | `"開"`, `"關"` |
| 英文 | `"on"`, `"off"` |
| 數字 | `"1"` (開), `"0"` (關) |
| 布林 | `true` (開), `false` (關) |

### 重要注意事項

1. **QoS 設定**：建議使用 QoS=1（至少一次傳遞），確保訊息可靠傳送
2. **JSON 編碼**：使用 UTF-8 編碼，避免中文亂碼
3. **數值範圍**：
   - 溫度：通常在 -50°C 到 60°C 之間
   - 濕度：通常在 0% 到 100% 之間
4. **發送頻率**：建議每 5-10 秒發送一次，避免過度佔用網路頻寬
5. **錯誤處理**：建議加入連線重試機制，確保網路斷線時能自動重連

### 完整的 Pico 範例程式

詳細的完整範例請參考專案中的範例檔案或參考以下結構：

```python
import network
import time
from umqtt.simple import MQTTClient
import ujson
import machine

# WiFi 和 MQTT 設定
WIFI_SSID = "您的WiFi"
WIFI_PASSWORD = "您的密碼"
MQTT_BROKER = "192.168.1.100"  # 改為您的 Raspberry Pi IP
MQTT_PORT = 1883
MQTT_TOPIC = "客廳/感測器"

def connect_wifi():
    # WiFi 連接邏輯
    pass

def read_sensors():
    # 讀取感測器資料
    return temperature, humidity, light_status

def main():
    connect_wifi()
    client = MQTTClient("pico_001", MQTT_BROKER, MQTT_PORT)
    client.connect()
    
    while True:
        temp, hum, light = read_sensors()
        data = {
            "temperature": temp,
            "humidity": hum,
            "light_status": "開" if light else "關"
        }
        client.publish(MQTT_TOPIC, ujson.dumps(data))
        time.sleep(5)

if __name__ == "__main__":
    main()
```

## 📈 效能比較

| 項目 | Streamlit 版本 | Flask 版本 |
|------|---------------|-----------|
| ARM 相容性 | ❌ 不相容（SIGILL） | ✅ 完全相容 |
| 記憶體佔用 | ~300MB | ~50MB |
| 啟動速度 | 5-10 秒 | < 1 秒 |
| 即時更新 | 需重新整理 | WebSocket 自動推送 |
| CPU 佔用 | 高 | 低 |

## 🐛 常見問題

### Q1: 應用程式無法啟動

確認已安裝必要套件：
```bash
cd /home/pi/Documents/GitHub/2025_10_26_chihlee_pi_pico
uv sync
```

### Q2: 網頁無法開啟

檢查防火牆設定：
```bash
sudo ufw allow 8080
```

### Q3: 無法連線 MQTT

```bash
# 確認 mosquitto 正在運行
sudo systemctl status mosquitto

# 測試 MQTT 連線
mosquitto_sub -h localhost -t "客廳/感測器" -v
```

### Q4: 沒有顯示數據

1. 檢查測試數據檔案是否存在：`ls -lh sensor_data.csv`
2. 重新生成測試數據：`uv run python generate_test_data.py`
3. 查看應用程式日誌，確認是否成功載入數據

## 🛠️ 技術棧

- **後端框架**：Flask 3.1.2
- **即時通訊**：Flask-SocketIO 5.5.1
- **MQTT 客戶端**：paho-mqtt 2.1.0+
- **數據儲存**：CSV（標準庫）+ Excel（openpyxl）
- **前端技術**：HTML5 + JavaScript + Chart.js
- **WebSocket**：Socket.IO 4.5.4

## 📖 進階使用

詳細的使用說明和技術細節請參閱：
- [啟動應用程式.md](啟動應用程式.md) - 快速啟動指南
- [使用說明.md](使用說明.md) - 完整技術文檔和故障排除
- [PRD.md](PRD.md) - 產品需求規格

## 📝 數據儲存

數據自動儲存到以下檔案：
- `sensor_data.csv` - CSV 格式（應用程式使用）
- `sensor_data.xlsx` - Excel 格式（人工查看）

包含欄位：
- 時間戳記
- 電燈狀態
- 溫度（°C）
- 濕度（%）

## 🎯 背景運行

如需背景運行應用程式：

```bash
# 啟動
nohup uv run python app_flask.py > app.log 2>&1 &

# 查看日誌
tail -f app.log

# 停止
pkill -f "python app_flask.py"
```

## 📜 授權

本專案遵循 [LICENSE](../LICENSE) 中的授權條款。

## 🙏 致謝

感謝使用本專案！如有問題或建議，歡迎提出 Issue。

