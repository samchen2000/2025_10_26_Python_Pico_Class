## 💻 第二天範例程式：day2_conditionals.py
### 📚 學習主題：運算子與流程控制 (上)
第二天我們要學習的是程式設計中非常重要的部分：運算子 (Operators) 和 條件判斷 (Conditional Statements)。這讓你的程式可以根據不同的情況做出不同的反應！

🎯 重點內容
- 比較運算子 (==, !=, >, <, >=, <=)

- 邏輯運算子 (and, or, not)

- 條件判斷結構 (if, elif, else)

```
# 檔案名稱: day2_conditionals.py
# 這是 Sam 老師為初學者準備的第二天課程範例！
# 目標：學習比較運算子、邏輯運算子，以及 if/elif/else 條件判斷。

# --- 區塊一：變數設定 ---
print("--- 模擬學生考試成績與判斷 ---")

# 設定兩個變數來代表學生的成績
math_score = 75
english_score = 90
has_attendance_issue = False # 判斷是否有出席問題，這是一個布林值 (Boolean)

# --- 區塊二：比較運算子 (結果為 True 或 False) ---
print("\n--- 比較運算結果 ---")
is_math_passed = math_score >= 60   # 數學是否及格 (大於等於 60)
is_english_excellent = english_score > 85 # 英文是否優異 (大於 85)

print(f"數學成績 {math_score} 是否及格: {is_math_passed}")
print(f"英文成績 {english_score} 是否優異: {is_english_excellent}")
print(f"兩個成績是否相等: {math_score == english_score}") # 檢查是否相等

# --- 區塊三：邏輯運算子 (and, or, not) ---
print("\n--- 邏輯運算結果 ---")

# 1. 'and': 兩邊都為 True，結果才為 True (例如：兩科都及格)
is_both_passed = is_math_passed and is_english_excellent 
print(f"是否兩科表現都優異: {is_both_passed}")

# 2. 'or': 只要有一邊為 True，結果就為 True (例如：至少一科優異)
is_at_least_one_passed = math_score >= 80 or english_score >= 80
print(f"是否至少有一科達到 80 分: {is_at_least_one_passed}")

# 3. 'not': 反轉結果 (例如：沒有出席問題)
is_attendance_ok = not has_attendance_issue
print(f"出席是否正常 (無問題): {is_attendance_ok}")


# --- 區塊四：條件判斷 (if / elif / else) ---
print("\n--- 條件判斷流程控制 ---")

# if 結構：根據成績進行評級
# 注意：Python 使用**縮排 (Indentation)** 來定義區塊，這是非常重要的！
if math_score >= 90:
    print("數學成績: 優秀 (A+)")
elif math_score >= 80:
    print("數學成績: 良好 (A)")
elif math_score >= 70:
    print("數學成績: 中等 (B)")
else:
    # 當以上所有條件都不成立時，執行 else 區塊
    print("數學成績: 需要再加油 (C)")

# 巢狀條件判斷 (Nested If) 範例：結合邏輯判斷
print("\n--- 綜合評估 ---")

if is_both_passed and is_attendance_ok:
    print("評語: 成績優異且出席良好，表現完美！")
elif is_math_passed or is_english_excellent:
    print("評語: 部分科目表現不錯，繼續保持！")
else:
    # 如果成績或出席有問題
    if has_attendance_issue:
        print("評語: 雖然成績尚可，但請注意出席狀況！")
    else:
        print("評語: 成績未達標，請檢視學習方法。")


# === 區塊五：後續預留程式碼 (方便未來擴展) ===

# TODO: 未來可以加入輸入 (input()) 函式，讓使用者自行輸入成績來測試
# user_input = input("請輸入您的數學成績：")
# score = int(user_input) # 將輸入的字串轉換成整數

# TODO: 未來可以加入三元運算子 (Ternary Operator) 的簡潔寫法
# status = "及格" if math_score >= 60 else "不及格"
# print(f"簡潔判斷結果: {status}")
```
💡 Sam 老師小提醒：
1. 縮排 (Indentation)：這是 Python 的靈魂！在 if, elif, else 後面的程式碼，必須用四個空格或一個 Tab 鍵進行縮排。縮排的程式碼才屬於該條件判斷的分支。

2. 冒號 (:)：在 if, elif, else 語句的結尾，一定要加上冒號 :，表示接下來是一個新的程式碼區塊。

3. elif (Else If)：當你有多個互斥的條件需要判斷時，使用 elif 而不是多個獨立的 if 語句。一旦其中一個條件成立，整個判斷結構就會結束，不會再檢查後續的 elif 和 else，這樣效率更高！