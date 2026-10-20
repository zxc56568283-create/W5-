import os
import re
import pandas as pd

# 1. 讀取與當前程式同一目錄下的 authors.csv
base_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(base_dir, "authors.csv")

df = pd.read_csv(csv_path)

# 取出第一筆資料
first_row = df.iloc[0]

born_date = str(first_row["born_date"])
born_location = str(first_row["born_location"])
tags = str(first_row["tags"])

# =======================================================
# 利用「字元類 + 量詞」正規表達式 (re) 擷取
# =======================================================

# 任務 1: born_date 的完整年份
# \d 表示數字，{4} 表示連續 4 個量詞
ans1 = re.findall(r"\b\d{4}\b", born_date)

# 任務 2: born_date 的月份 (英文單字)
# [A-Za-z] 字元類，+ 表示 1 個以上
ans2 = re.findall(r"[A-Za-z]+", born_date)

# 任務 3: born_location 的每一個英文單字
# [A-Za-z]+ 匹配所有連續英文字母單字（自動過濾掉逗號與空格）
ans3 = re.findall(r"[A-Za-z]+", born_location)

# 任務 4: tags 拆成一個一個標籤
# [a-z-]+ 匹配小寫英文字母與連字號組成的標籤名稱（例如 deep-thoughts）
ans4 = re.findall(r"[a-z-]+", tags)

# =======================================================
# 印出題目要求的預期輸出格式
# =======================================================
print("預期輸出\n")
print(f"① {ans1}")
print(f"② {ans2}")
print(f"③ {ans3}")
print(f"④ {ans4}")