"""
MQTT 訂閱者 Streamlit 應用程式
功能：
1. 訂閱 MQTT 主題（電燈、溫度、濕度）
2. 顯示電燈開/關狀態
3. 顯示溫度和濕度圖表
4. 自動儲存資料為 Excel 檔案
"""

import streamlit as st
import sys
import json
import time
import site
import os
from datetime import datetime
from collections import deque

# 添加系統套件路徑和用戶套件路徑
sys.path.insert(0, '/usr/lib/python3/dist-packages')
try:
    import os
    user_site_313 = os.path.expanduser('~/.local/lib/python3.13/site-packages')
    if os.path.exists(user_site_313) and user_site_313 not in sys.path:
        sys.path.insert(0, user_site_313)
    user_site = site.getusersitepackages()
    if user_site not in sys.path:
        sys.path.insert(0, user_site)
except:
    pass

try:
    import paho.mqtt.client as mqtt
except ImportError:
    st.error("❌ 無法導入 paho-mqtt 套件，請先安裝：pip install paho-mqtt")
    st.stop()

try:
    import pandas as pd
except ImportError as e:
    # 嘗試在用戶目錄中查找 pandas
    try:
        user_site_313 = os.path.expanduser('~/.local/lib/python3.13/site-packages')
        if os.path.exists(user_site_313) and user_site_313 not in sys.path:
            sys.path.insert(0, user_site_313)
            import pandas as pd
        else:
            raise ImportError(f"無法導入 pandas: {e}")
    except Exception as e2:
        st.error(f"❌ 無法導入 pandas 套件：{e2}")
        st.info("請安裝：pip install pandas")
        st.stop()

# 頁面設定
st.set_page_config(
    page_title="MQTT 訂閱者監控",
    page_icon="🏠",
    layout="wide"
)

# MQTT 主題設定
MQTT_TOPICS = {
    'light': '客廳/電燈',      # 電燈狀態
    'temperature': '客廳/溫度', # 溫度
    'humidity': '客廳/濕度'     # 濕度
}

# 初始化 session state
if 'mqtt_client' not in st.session_state:
    st.session_state.mqtt_client = None
if 'is_connected' not in st.session_state:
    st.session_state.is_connected = False
if 'light_status' not in st.session_state:
    st.session_state.light_status = "未知"
if 'temperature_data' not in st.session_state:
    st.session_state.temperature_data = deque(maxlen=100)  # 保留最近100筆
if 'humidity_data' not in st.session_state:
    st.session_state.humidity_data = deque(maxlen=100)  # 保留最近100筆
if 'data_records' not in st.session_state:
    st.session_state.data_records = []  # 儲存所有記錄用於 Excel
if 'last_update' not in st.session_state:
    st.session_state.last_update = None
if 'excel_file' not in st.session_state:
    st.session_state.excel_file = None

# MQTT 回調函數
def on_connect(client, userdata, flags, rc):
    """連接回調函數"""
    if rc == 0:
        st.session_state.is_connected = True
        # 連接成功後訂閱所有主題
        for topic in MQTT_TOPICS.values():
            client.subscribe(topic, qos=1)

def on_message(client, userdata, msg):
    """接收訊息回調函數"""
    try:
        message = msg.payload.decode('utf-8')
        timestamp = datetime.now()
        
        topic = msg.topic
        
        # 處理電燈狀態
        if topic == MQTT_TOPICS['light']:
            try:
                data = json.loads(message)
                if isinstance(data, dict):
                    # 如果是 JSON，尋找狀態欄位
                    status = data.get('status', data.get('state', message))
                else:
                    status = message
                
                # 判斷開關狀態
                status_lower = str(status).lower()
                if 'on' in status_lower or '開' in status_lower or status_lower == '1' or status_lower == 'true':
                    st.session_state.light_status = "開"
                elif 'off' in status_lower or '關' in status_lower or status_lower == '0' or status_lower == 'false':
                    st.session_state.light_status = "關"
                else:
                    st.session_state.light_status = str(status)
            except:
                # 如果不是 JSON，直接使用訊息
                status_lower = message.lower()
                if 'on' in status_lower or '開' in status_lower:
                    st.session_state.light_status = "開"
                elif 'off' in status_lower or '關' in status_lower:
                    st.session_state.light_status = "關"
                else:
                    st.session_state.light_status = message
        
        # 處理溫度
        elif topic == MQTT_TOPICS['temperature']:
            try:
                data = json.loads(message)
                if isinstance(data, dict):
                    temp_value = data.get('temperature', data.get('temp', data.get('value', None)))
                    if temp_value is not None:
                        temp_value = float(temp_value)
                    else:
                        # 嘗試從所有數值欄位中找到溫度
                        for key, value in data.items():
                            if isinstance(value, (int, float)) and -50 <= value <= 60:
                                temp_value = float(value)
                                break
                else:
                    temp_value = float(message)
                
                st.session_state.temperature_data.append({
                    'timestamp': timestamp,
                    'value': temp_value
                })
                
                # 記錄到資料列表
                st.session_state.data_records.append({
                    'timestamp': timestamp,
                    'topic': topic,
                    'temperature': temp_value,
                    'humidity': None,
                    'light': None
                })
            except Exception as e:
                # 嘗試直接轉換為數字
                try:
                    temp_value = float(message)
                    st.session_state.temperature_data.append({
                        'timestamp': timestamp,
                        'value': temp_value
                    })
                    st.session_state.data_records.append({
                        'timestamp': timestamp,
                        'topic': topic,
                        'temperature': temp_value,
                        'humidity': None,
                        'light': None
                    })
                except:
                    pass
        
        # 處理濕度
        elif topic == MQTT_TOPICS['humidity']:
            try:
                data = json.loads(message)
                if isinstance(data, dict):
                    hum_value = data.get('humidity', data.get('hum', data.get('value', None)))
                    if hum_value is not None:
                        hum_value = float(hum_value)
                    else:
                        # 嘗試從所有數值欄位中找到濕度
                        for key, value in data.items():
                            if isinstance(value, (int, float)) and 0 <= value <= 100:
                                hum_value = float(value)
                                break
                else:
                    hum_value = float(message)
                
                st.session_state.humidity_data.append({
                    'timestamp': timestamp,
                    'value': hum_value
                })
                
                # 記錄到資料列表
                st.session_state.data_records.append({
                    'timestamp': timestamp,
                    'topic': topic,
                    'temperature': None,
                    'humidity': hum_value,
                    'light': None
                })
            except Exception as e:
                # 嘗試直接轉換為數字
                try:
                    hum_value = float(message)
                    st.session_state.humidity_data.append({
                        'timestamp': timestamp,
                        'value': hum_value
                    })
                    st.session_state.data_records.append({
                        'timestamp': timestamp,
                        'topic': topic,
                        'temperature': None,
                        'humidity': hum_value,
                        'light': None
                    })
                except:
                    pass
        
        # 處理包含多種資料的 JSON
        else:
            try:
                data = json.loads(message)
                if isinstance(data, dict):
                    # 如果 JSON 包含多種資料
                    record = {
                        'timestamp': timestamp,
                        'topic': topic,
                        'temperature': data.get('temperature', data.get('temp', None)),
                        'humidity': data.get('humidity', data.get('hum', None)),
                        'light': data.get('light', data.get('status', None))
                    }
                    st.session_state.data_records.append(record)
                    
                    # 更新對應的資料
                    if record['temperature'] is not None:
                        st.session_state.temperature_data.append({
                            'timestamp': timestamp,
                            'value': float(record['temperature'])
                        })
                    if record['humidity'] is not None:
                        st.session_state.humidity_data.append({
                            'timestamp': timestamp,
                            'value': float(record['humidity'])
                        })
                    if record['light'] is not None:
                        status = str(record['light']).lower()
                        if 'on' in status or '開' in status or status == '1' or status == 'true':
                            st.session_state.light_status = "開"
                        elif 'off' in status or '關' in status or status == '0' or status == 'false':
                            st.session_state.light_status = "關"
            except:
                pass
        
        st.session_state.last_update = timestamp
        
        # 自動儲存為 Excel（每10筆記錄儲存一次）
        if len(st.session_state.data_records) % 10 == 0:
            save_to_excel()
            
    except Exception as e:
        pass

def on_subscribe(client, userdata, mid, granted_qos):
    """訂閱回調函數"""
    pass

def on_disconnect(client, userdata, rc):
    """斷線回調函數"""
    st.session_state.is_connected = False

def save_to_excel():
    """將資料儲存為 Excel 檔案"""
    try:
        if not st.session_state.data_records:
            return
        
        # 建立 DataFrame
        df = pd.DataFrame(st.session_state.data_records)
        
        # 確保時間戳格式正確
        if 'timestamp' in df.columns:
            df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        # 建立檔名（包含日期時間）
        filename = f"mqtt_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        filepath = os.path.join(os.getcwd(), filename)
        
        # 儲存為 Excel
        df.to_excel(filepath, index=False, engine='openpyxl')
        st.session_state.excel_file = filepath
    except Exception as e:
        # 如果 openpyxl 不可用，嘗試使用 xlsxwriter
        try:
            filename = f"mqtt_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            filepath = os.path.join(os.getcwd(), filename)
            df.to_excel(filepath, index=False, engine='xlsxwriter')
            st.session_state.excel_file = filepath
        except:
            pass

# 側邊欄設定
st.sidebar.header("⚙️ MQTT 設定")
MQTT_BROKER = st.sidebar.text_input("Broker 地址", value="localhost")
MQTT_PORT = st.sidebar.number_input("連接埠", min_value=1, max_value=65535, value=1883)
MQTT_CLIENT_ID = st.sidebar.text_input("客戶端 ID", value="subscriber_monitor_001")

st.sidebar.markdown("---")
st.sidebar.markdown("### 📡 訂閱主題")
st.sidebar.write(f"- 電燈: `{MQTT_TOPICS['light']}`")
st.sidebar.write(f"- 溫度: `{MQTT_TOPICS['temperature']}`")
st.sidebar.write(f"- 濕度: `{MQTT_TOPICS['humidity']}`")

# 主標題
st.title("🏠 客廳環境監控系統")
st.markdown("---")

# 連接控制
col1, col2 = st.columns([3, 1])

with col1:
    if st.button("🔌 連接 MQTT", disabled=st.session_state.is_connected, use_container_width=True):
        try:
            client = mqtt.Client(client_id=MQTT_CLIENT_ID)
            client.on_connect = on_connect
            client.on_message = on_message
            client.on_subscribe = on_subscribe
            client.on_disconnect = on_disconnect
            
            client.connect(MQTT_BROKER, MQTT_PORT, keepalive=60)
            client.loop_start()
            st.session_state.mqtt_client = client
            
            time.sleep(0.5)
            if st.session_state.is_connected:
                st.success("✓ 連接成功並已訂閱所有主題！")
                st.rerun()
            else:
                st.error("✗ 連接失敗")
        except Exception as e:
            st.error(f"連接錯誤: {e}")

with col2:
    if st.button("🔌 斷開連接", disabled=not st.session_state.is_connected, use_container_width=True):
        if st.session_state.mqtt_client:
            try:
                st.session_state.mqtt_client.loop_stop()
                st.session_state.mqtt_client.disconnect()
                st.session_state.mqtt_client = None
                st.session_state.is_connected = False
                st.success("✓ 已斷開連接")
                st.rerun()
            except Exception as e:
                st.error(f"斷開錯誤: {e}")

# 狀態顯示
status_col1, status_col2 = st.columns(2)
with status_col1:
    status_icon = "🟢" if st.session_state.is_connected else "🔴"
    st.metric("連接狀態", f"{status_icon} {'已連接' if st.session_state.is_connected else '未連接'}")

with status_col2:
    if st.session_state.last_update:
        update_time = st.session_state.last_update.strftime("%Y-%m-%d %H:%M:%S")
        st.metric("最後更新", update_time)
    else:
        st.metric("最後更新", "尚未有資料")

st.markdown("---")

# 電燈狀態顯示
st.markdown("### 💡 電燈狀態")
light_col1, light_col2 = st.columns([1, 3])
with light_col1:
    if st.session_state.light_status == "開":
        st.markdown("<h1 style='text-align: center; color: #FFD700;'>💡</h1>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align: center; color: green;'>開</h2>", unsafe_allow_html=True)
    elif st.session_state.light_status == "關":
        st.markdown("<h1 style='text-align: center; color: #808080;'>💡</h1>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align: center; color: gray;'>關</h2>", unsafe_allow_html=True)
    else:
        st.markdown("<h1 style='text-align: center;'>❓</h1>", unsafe_allow_html=True)
        st.markdown(f"<h3 style='text-align: center;'>{st.session_state.light_status}</h3>", unsafe_allow_html=True)

st.markdown("---")

# 溫度和濕度圖表
st.markdown("### 📊 溫度和濕度監控")

if len(st.session_state.temperature_data) > 0 or len(st.session_state.humidity_data) > 0:
    # 準備圖表資料
    temp_df = pd.DataFrame(list(st.session_state.temperature_data))
    hum_df = pd.DataFrame(list(st.session_state.humidity_data))
    
    if len(temp_df) > 0:
        temp_df['timestamp'] = pd.to_datetime(temp_df['timestamp'])
        temp_df = temp_df.set_index('timestamp')
    
    if len(hum_df) > 0:
        hum_df['timestamp'] = pd.to_datetime(hum_df['timestamp'])
        hum_df = hum_df.set_index('timestamp')
    
    # 顯示圖表
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        st.markdown("#### 🌡️ 溫度 (°C)")
        if len(temp_df) > 0:
            st.line_chart(temp_df['value'])
            if len(temp_df) > 0:
                current_temp = temp_df['value'].iloc[-1]
                st.metric("當前溫度", f"{current_temp:.1f} °C")
        else:
            st.info("等待溫度資料...")
    
    with chart_col2:
        st.markdown("#### 💧 濕度 (%)")
        if len(hum_df) > 0:
            st.line_chart(hum_df['value'])
            if len(hum_df) > 0:
                current_hum = hum_df['value'].iloc[-1]
                st.metric("當前濕度", f"{current_hum:.1f} %")
        else:
            st.info("等待濕度資料...")
    
    # 合併圖表
    if len(temp_df) > 0 and len(hum_df) > 0:
        st.markdown("#### 📈 溫度與濕度趨勢")
        combined_df = pd.DataFrame({
            '溫度 (°C)': temp_df['value'] if len(temp_df) > 0 else None,
            '濕度 (%)': hum_df['value'] if len(hum_df) > 0 else None
        }).dropna()
        if len(combined_df) > 0:
            st.line_chart(combined_df)
else:
    st.info("📭 尚未收到任何資料。請確保已連接 MQTT 並且有設備在發布資料。")

st.markdown("---")

# 資料統計與 Excel 下載
st.markdown("### 📥 資料管理")

stat_col1, stat_col2, stat_col3 = st.columns(3)
with stat_col1:
    st.metric("溫度資料點", len(st.session_state.temperature_data))
with stat_col2:
    st.metric("濕度資料點", len(st.session_state.humidity_data))
with stat_col3:
    st.metric("總記錄數", len(st.session_state.data_records))

# Excel 下載按鈕
if len(st.session_state.data_records) > 0:
    if st.button("💾 儲存資料為 Excel", use_container_width=True):
        try:
            save_to_excel()
            if st.session_state.excel_file and os.path.exists(st.session_state.excel_file):
                with open(st.session_state.excel_file, 'rb') as f:
                    st.download_button(
                        label="📥 下載 Excel 檔案",
                        data=f.read(),
                        file_name=os.path.basename(st.session_state.excel_file),
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        use_container_width=True
                    )
                st.success("✓ Excel 檔案已生成！")
            else:
                st.error("生成 Excel 檔案時發生錯誤")
        except Exception as e:
            st.error(f"儲存錯誤: {e}")
            st.info("提示：請安裝 openpyxl 或 xlsxwriter：pip install openpyxl")

# 自動刷新（使用 st.rerun() 會在 Streamlit 中自動處理，這裡不需要手動刷新）
# Streamlit 會自動檢測 session_state 的變化並更新介面

