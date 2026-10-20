import os
import re
import pandas as pd

# 1. 讀取與當前程式同一目錄下的 authors.csv
base_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(base_dir, "authors.csv")

df = pd.read_csv(csv_path)

# 取得第 1 筆與第 2 筆資料（J.K. Rowling 在第 2 筆）
row_1 = df.iloc[0]
row_2 = df.iloc[1]

born_date = str(row_1["born_date"])        # "March 14, 1879"
born_location = str(row_1["born_location"])  # "in Ulm, Germany"
name_2 = str(row_2["name"])                # "J.K. Rowling"

# =======================================================
# 利用「中介字元（Metacharacters）」進行擷取
# =======================================================

# 任務 1: born_date 的「日」（不能把年份切碎）
# 使用 \b\d{1,2}(?=,) 匹配逗號前獨立的 1~2 位數字，或 \b\d{1,2}\b 但排除 4 位數年份
ans1 = re.findall(r"\b\d{1,2}(?=,)", born_date)

# 任務 2: born_date 開頭的月份
# 使用中介字元 ^（開頭錨點）匹配字串最前面的英文單字
ans2 = re.findall(r"^[A-Za-z]+", born_date)

# 任務 3: born_location 的國家（最後一段）
# 方式 A：取最後一段文字（逗號或 "in " 之後直到字串結尾 $）
ans3 = re.findall(r"(?:,\s*|in\s+)([\w\s]+)$", born_location)
ans3 = [s.strip() for s in ans3]

# 任務 4: name 裡的英文縮寫 (J.K. Rowling)
# [A-Z]\. 匹配大寫字母後緊接小數點的中介字元結構
ans4 = re.findall(r"[A-Z]\.", name_2)

# =======================================================
# 印出題目要求的預期輸出格式
# =======================================================
print("預期輸出\n")
print(f"① {ans1}")
print(f"② {ans2}")
print(f"③ {ans3}")
print(f"④ {ans4}")