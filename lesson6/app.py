"""
MQTT Streamlit 應用程式
整合 MQTT 發布和訂閱功能的 Web 介面
"""

import streamlit as st
import sys
import json
import time
import site
from datetime import datetime

# 添加系統套件路徑和用戶套件路徑
sys.path.insert(0, '/usr/lib/python3/dist-packages')
# 添加用戶安裝的套件路徑（Python 3.13）
try:
    import os
    user_site_313 = os.path.expanduser('~/.local/lib/python3.13/site-packages')
    if os.path.exists(user_site_313) and user_site_313 not in sys.path:
        sys.path.insert(0, user_site_313)
    # 也嘗試添加當前 Python 版本的用戶目錄
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

# 頁面設定
st.set_page_config(
    page_title="MQTT 控制台",
    page_icon="📡",
    layout="wide"
)

# MQTT 設定（可以在側邊欄修改）
st.sidebar.header("⚙️ MQTT 設定")
MQTT_BROKER = st.sidebar.text_input("Broker 地址", value="localhost")
MQTT_PORT = st.sidebar.number_input("連接埠", min_value=1, max_value=65535, value=1883)
MQTT_TOPIC = st.sidebar.text_input("主題", value="客廳/溫度")
MQTT_CLIENT_ID = st.sidebar.text_input("客戶端 ID", value="streamlit_client_001")

# 初始化 session state
if 'mqtt_client' not in st.session_state:
    st.session_state.mqtt_client = None
if 'is_connected' not in st.session_state:
    st.session_state.is_connected = False
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'subscribed' not in st.session_state:
    st.session_state.subscribed = False

# MQTT 回調函數
def on_connect(client, userdata, flags, rc):
    """連接回調函數"""
    if rc == 0:
        st.session_state.is_connected = True
    else:
        st.session_state.is_connected = False

def on_message(client, userdata, msg):
    """接收訊息回調函數"""
    try:
        message = msg.payload.decode('utf-8')
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # 嘗試解析 JSON
        try:
            json_data = json.loads(message)
            message_type = "JSON"
        except:
            json_data = None
            message_type = "文字"
        
        # 將訊息加入列表
        st.session_state.messages.insert(0, {
            'timestamp': timestamp,
            'topic': msg.topic,
            'qos': msg.qos,
            'message': message,
            'json_data': json_data,
            'type': message_type
        })
        
        # 限制訊息數量（保留最近 50 筆）
        if len(st.session_state.messages) > 50:
            st.session_state.messages = st.session_state.messages[:50]
    except Exception as e:
        st.error(f"處理訊息錯誤: {e}")

def on_subscribe(client, userdata, mid, granted_qos):
    """訂閱回調函數"""
    st.session_state.subscribed = True

def on_disconnect(client, userdata, rc):
    """斷線回調函數"""
    st.session_state.is_connected = False
    st.session_state.subscribed = False

# 主標題
st.title("📡 MQTT 控制台")
st.markdown("---")

# 連接控制區域
col1, col2, col3 = st.columns([2, 2, 2])

with col1:
    if st.button("🔌 連接", disabled=st.session_state.is_connected, use_container_width=True):
        try:
            client = mqtt.Client(client_id=MQTT_CLIENT_ID)
            client.on_connect = on_connect
            client.on_message = on_message
            client.on_subscribe = on_subscribe
            client.on_disconnect = on_disconnect
            
            client.connect(MQTT_BROKER, MQTT_PORT, keepalive=60)
            client.loop_start()
            st.session_state.mqtt_client = client
            
            time.sleep(0.5)  # 等待連接
            if st.session_state.is_connected:
                st.success("✓ 連接成功！")
                st.rerun()
            else:
                st.error("✗ 連接失敗")
        except Exception as e:
            st.error(f"連接錯誤: {e}")

with col2:
    if st.button("📥 訂閱主題", disabled=not st.session_state.is_connected or st.session_state.subscribed, use_container_width=True):
        if st.session_state.mqtt_client:
            try:
                st.session_state.mqtt_client.subscribe(MQTT_TOPIC, qos=1)
                time.sleep(0.3)
                if st.session_state.subscribed:
                    st.success(f"✓ 已訂閱主題: {MQTT_TOPIC}")
                else:
                    st.info("訂閱請求已發送...")
                st.rerun()
            except Exception as e:
                st.error(f"訂閱錯誤: {e}")

with col3:
    if st.button("🔌 斷開連接", disabled=not st.session_state.is_connected, use_container_width=True):
        if st.session_state.mqtt_client:
            try:
                st.session_state.mqtt_client.loop_stop()
                st.session_state.mqtt_client.disconnect()
                st.session_state.mqtt_client = None
                st.session_state.is_connected = False
                st.session_state.subscribed = False
                st.success("✓ 已斷開連接")
                st.rerun()
            except Exception as e:
                st.error(f"斷開錯誤: {e}")

# 狀態顯示
st.markdown("### 📊 連接狀態")
status_col1, status_col2, status_col3 = st.columns(3)
with status_col1:
    status_icon = "🟢" if st.session_state.is_connected else "🔴"
    st.metric("連接狀態", f"{status_icon} {'已連接' if st.session_state.is_connected else '未連接'}")
with status_col2:
    subscribe_icon = "✅" if st.session_state.subscribed else "❌"
    st.metric("訂閱狀態", f"{subscribe_icon} {'已訂閱' if st.session_state.subscribed else '未訂閱'}")
with status_col3:
    st.metric("已接收訊息", len(st.session_state.messages))

st.markdown("---")

# 發布訊息區域
st.markdown("### 📤 發布訊息")
publish_tab1, publish_tab2 = st.tabs(["📝 文字訊息", "📊 JSON 訊息"])

with publish_tab1:
    text_message = st.text_area("輸入訊息", height=100, placeholder="輸入要發布的文字訊息...")
    if st.button("🚀 發布文字訊息", disabled=not st.session_state.is_connected, use_container_width=True):
        if st.session_state.mqtt_client and text_message:
            try:
                result = st.session_state.mqtt_client.publish(MQTT_TOPIC, text_message, qos=1)
                if result[0] == 0:
                    st.success(f"✓ 訊息已發布到主題 '{MQTT_TOPIC}'")
                else:
                    st.error(f"✗ 發布失敗，狀態碼: {result[0]}")
            except Exception as e:
                st.error(f"發布錯誤: {e}")

with publish_tab2:
    st.markdown("**JSON 格式範例：**")
    json_example = {
        "device_id": "sensor_001",
        "temperature": 25.5,
        "humidity": 60.0,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    st.json(json_example)
    
    json_message = st.text_area("輸入 JSON 訊息", height=150, value=json.dumps(json_example, indent=2, ensure_ascii=False))
    if st.button("🚀 發布 JSON 訊息", disabled=not st.session_state.is_connected, use_container_width=True):
        if st.session_state.mqtt_client and json_message:
            try:
                # 驗證 JSON 格式
                json.loads(json_message)  # 驗證是否為有效 JSON
                
                result = st.session_state.mqtt_client.publish(MQTT_TOPIC, json_message, qos=1)
                if result[0] == 0:
                    st.success(f"✓ JSON 訊息已發布到主題 '{MQTT_TOPIC}'")
                else:
                    st.error(f"✗ 發布失敗，狀態碼: {result[0]}")
            except json.JSONDecodeError:
                st.error("❌ JSON 格式錯誤，請檢查您的輸入")
            except Exception as e:
                st.error(f"發布錯誤: {e}")

st.markdown("---")

# 接收訊息區域
st.markdown("### 📥 接收訊息")

if st.button("🔄 刷新", use_container_width=False):
    st.rerun()

if st.session_state.messages:
    # 顯示訊息列表
    for idx, msg in enumerate(st.session_state.messages):
        with st.expander(f"📨 [{msg['timestamp']}] {msg['topic']} (QoS: {msg['qos']})", expanded=(idx == 0)):
            col_a, col_b = st.columns([3, 1])
            with col_a:
                st.markdown(f"**訊息內容：**")
                if msg['type'] == 'JSON' and msg['json_data']:
                    st.json(msg['json_data'])
                    st.markdown(f"**原始訊息：**")
                    st.code(msg['message'], language='json')
                else:
                    st.code(msg['message'])
            with col_b:
                st.markdown(f"**主題：** {msg['topic']}")
                st.markdown(f"**QoS：** {msg['qos']}")
                st.markdown(f"**時間：** {msg['timestamp']}")
                st.markdown(f"**類型：** {msg['type']}")
    
    # 清除訊息按鈕
    if st.button("🗑️ 清除所有訊息", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
else:
    st.info("📭 尚未收到任何訊息。請先連接並訂閱主題，然後發布一些訊息進行測試。")

# 頁腳
st.markdown("---")
st.markdown("💡 **提示：** 打開兩個瀏覽器視窗，一個用來發布訊息，另一個用來接收訊息，這樣可以更好地測試 MQTT 功能。")
