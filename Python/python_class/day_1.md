## 🐍 一週 Python 初學課程大綱
### 💡 學習目標
- 理解 Python 的基本語法和程式結構。

- 掌握資料型別、變數、運算子和流程控制的使用。

- 學會如何定義和呼叫函式。

- 能夠處理基本的資料結構（列表、字典）

| 天數  |   學習主題     | 重點內容     | 範例練習 (檔案名)
|----------|--------------|-------------|-----------------|
| 第一天 | 環境與基本輸出 | 變數、資料型別（整數、浮點數、字串）、print() 函式。| day1_basic_io.py
| 第二天 | 運算子與流程控制 (上) | 算術/比較/邏輯運算子、if/elif/else 條件判斷。|day2_conditionals.py
| 第三天 | 流程控制 (下)| for 迴圈、while 迴圈、range() 函式。|day3_loops.py
| 第四天 | 列表 (List) 與元組 (Tuple)|列表的創建、存取、修改、常用方法；元組的基本概念。| day4_data_list.py
| 第五天 | 字典 (Dictionary) 與集合 (Set),字典的創建、鍵值對存取、常用方法；集合的基本概念。|day5_data_dict.py
| 第六天 | 函式 (Function),函式的定義 (def)、參數傳遞、回傳值 (return)、作用域。| day6_functions.py
| 第七天 | 檔案操作 (File I/O) 與綜合應用,"簡單的檔案讀取與寫入 (open(), read(), write())、綜合前六天的知識。"|day7_file_io_review.py

## 💻 第一天範例程式：day1_basic_io.py
- 這是關於變數宣告、資料型別和基本輸出的練習
```
# 檔案名稱: day1_basic_io.py
# 這是 Sam 老師為初學者準備的第一天課程範例！
# 目標：學習變數、基本資料型別 (int, float, str) 和 print() 函式。

# === 區塊一：變數宣告與基本資料型別 ===

# 1. 整數 (Integer) - 用於計數
student_id = 101          # 宣告一個整數變數，代表學號
num_courses = 5           # 宣告修習的課程數量

# 2. 浮點數 (Float) - 用於帶有小數點的數值
pi_value = 3.14159        # 宣告圓周率
average_score = 88.5      # 宣告平均分數

# 3. 字串 (String) - 用於文字信息
student_name = "王小明"    # 宣告學生的名字，請用雙引號或單引號包住
greeting_message = '歡迎學習 Python 程式設計！' 

# 💡 小技巧：使用 type() 函式可以檢查變數的資料型別
# print(type(student_id))
# print(type(student_name))


# === 區塊二：基本輸出 (print 函式) ===

print("--- 學生基本資料 ---")

# 1. 輸出單個變數
print("學生姓名:", student_name)

# 2. 輸出多個變數，中間會自動用空格隔開
print("學號:", student_id, "修習課程數:", num_courses)

# 3. 輸出包含不同資料型別的變數，Python 會自動轉換
print(f"小明的平均分數是: {average_score}") # 💡 這裡我們使用 f-string (格式化字串)，推薦使用！

print("--- 課程訊息 ---")
print(greeting_message)
print("圓周率的近似值為:", pi_value)


# === 區塊三：後續預留程式碼 (Sam 老師的習慣：方便未來擴展) ===

# TODO: 未來可以加入布林值 (Boolean, True/False) 的範例
# is_enrolled = True 
# print("是否註冊:", is_enrolled)

# TODO: 未來可以增加變數賦值運算 (例如：num_courses = num_courses + 1) 的練習
# num_courses += 1
# print("新修習課程數:", num_courses)
```
## 💡 Sam 老師小提醒：
1. 註解的重要性：在 Python 中，# 符號後面的內容都是註解，程式不會執行。請務必養成寫註解的好習慣，這能讓你的程式碼更容易被自己和他人理解！

2. 變數命名：變數名稱請盡量使用英文或拼音，並且要有意義（例如 student_name 比 a 好）。Python 變數名稱是大小寫敏感的。

3. 環境設定：在開始之前，請確保你已經安裝了 Python（建議是 3.8+ 版本）和一個好用的程式碼編輯器（例如 VS Code）。