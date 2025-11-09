## 在raspberry 安裝 uv
1. 請先確認你的 Raspberry Pi 系統：  
```
cat /etc/os-release
```
## 安裝 uv 的方法
### 方式 1：使用官方一鍵安裝指令（建議）
#### uv 提供官方腳本，可以直接在 Raspberry Pi 上執行：  
```
curl -LsSf https://astral.sh/uv/install.sh | sh
```
#### 安裝完成後，重啟終端機或執行：  
```
source ~/.profile
```
#### 然後測試是否成功：
```
uv --version
```

## 在已有的專案
```
uv init --python 3.10
uv venv
uv sync
```

## 建立新專案
```
uv init my-project
cd my-project
uv sync
```

## 建立虛擬環境
```
uv venv
```
## 啟用虛擬環境
```
source .venv/bin/activate  # macOS/Linux
```
## 或
```
.venv\Scripts\activate     # Windows
```
## 安裝套件
```
uv add requests
```
## 執行 Python 腳本
```
uv run python script.py
```