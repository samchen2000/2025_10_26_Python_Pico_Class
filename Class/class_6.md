1. 安裝 Antigraity (另一個 vs code 編譯器)
2. git config (要上傳到自己的github)
```
git config --global user.name "XXXXXXX"
git config --global user.email XXXX@export.com
git config --global pull.rebase false
```

## 關於 Cursor 無法使用 AI 的問題
為什麼！有些人cursor的帳號！會ㄧ下就不行使用AI了！原因是cursor有記錄硬體指紋的功能！  

這是一個在開發圈（特別是使用 VS Code 分支編輯器如 Cursor）常見的技術問題。  
Cursor 是基於 VS Code 構建的，因此它的設備識別機制（Device Fingerprinting）與 VS Code 高度相似，通常是為了防止濫用免費額度或是同步設定。  
所謂的「記錄硬體設備」，通常是指它生成了一組唯一的 Machine ID 或 Mac Machine ID 並存儲在本地的設定檔中。如果你希望重置這個身份（例如在電腦教室映像檔複製後避免衝突，或是解決設定損壞問題），你需要清除這些特定的設定檔。  
以下是針對 Windows 和 macOS 的技術操作步驟：  
核心原理  
Cursor 在安裝後，會在本地生成一個 storage.json 文件，裡面包含了一組 UUID（通用唯一識別碼），這就是它用來標記你這台電腦的「身分證」。
要「消除」紀錄，實際上是指刪除這個舊的 ID，強制 Cursor 在下次啟動時生成一個新的 ID。  
操作步驟  
1. Windows 系統  
在 Windows 上，這個資訊通常隱藏在 AppData 資料夾中。
 * 完全關閉 Cursor（確保後台沒有殘留進程）。
 * 使用快捷鍵 Win + R 開啟執行視窗，輸入 %APPDATA% 並按 Enter。
 * 進入路徑：Cursor\User\globalStorage\
 * 找到名為 storage.json 的檔案。
 * 操作方式：
   * 編輯法（推薦）： 用記事本打開它，找到 "telemetry.machineId" 和 "telemetry.macMachineId" 這兩行，修改數值或刪除這兩行，儲存後關閉。
   * 刪除法（暴力）： 直接刪除整個 storage.json（注意：這可能會重置部分全域設定，如歡迎頁面狀態）。
 * 重新啟動 Cursor，它會生成新的 ID。
2. macOS 系統
在 Mac 上，路徑位於 Library（資源庫）中。
 * 完全關閉 Cursor（Cmd + Q）。
 * 開啟 Terminal（終端機）。
 * 輸入以下指令進入設定目錄：
   cd ~/Library/Application\ Support/Cursor/User/globalStorage/

 * 你可以使用編輯器（如 nano 或 vim）修改 storage.json，或者直接刪除它：
   rm storage.json

 * 此外，有時還需要清除快取狀態，建議同時檢查：
   ~/Library/Application Support/Cursor/ 下的其他暫存資料夾。
⚠️ 進階技術說明與限制
身為資深講師，您可能需要了解更深層的機制：
 * 不僅僅是檔案 (Hardware Fingerprinting)：
   現在的軟體驗證機制越來越嚴格。除了上述的 storage.json 軟體層面的 ID 之外，Cursor 的後端驗證可能還會讀取硬體特徵（如網卡 MAC Address、硬碟序號、CPU 序號等）。
   * 如果 Cursor 伺服器端已經鎖定了你的「硬體特徵」，單純刪除本地的 JSON 檔案可能無法繞過限制（例如試用期封鎖）。這在資安上稱為「硬體指紋綁定」。
 * 徹底移除工具 (Clean Uninstall)：
   如果手動刪除無效，建議使用專門的「徹底卸載工具」，這些工具能掃描並刪除註冊表（Registry）殘留：
   * Windows: 推薦使用 Revo Uninstaller 或 Geek Uninstaller。
   * macOS: 推薦使用 AppCleaner。
     這類工具能在移除軟體後，把深藏在系統深處的關聯檔案一併清除。
總結
如果您是為了解決設定衝突（例如多台電腦 ID 重複），刪除 storage.json 是標準解法。但如果您是為了重置試用額度，由於現代的硬體指紋技術，單純刪除檔案可能無法完全騙過伺服器，可能需要更換帳號或網路環境（IP）配合測試。