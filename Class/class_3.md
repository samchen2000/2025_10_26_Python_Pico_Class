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
