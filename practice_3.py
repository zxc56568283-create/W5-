import os
import string
import pandas as pd

# 1. 取得當前程式碼所在目錄，確保正確讀取 authors.csv
base_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(base_dir, "authors.csv")

# 讀取 CSV 檔案
df = pd.read_csv(csv_path)

# 取出第一筆（第一列）資料
first_row = df.iloc[0]

born_date = str(first_row["born_date"])
born_location = str(first_row["born_location"])
tags = str(first_row["tags"])
quote = str(first_row["quote"])

# =======================================================
# 利用字元類別的方法進行篩選
# =======================================================

# 任務 1: born_date 的所有數字 (利用 .isdigit())
ans1 = [char for char in born_date if char.isdigit()]

# 任務 2: born_location 的所有大寫字母 (利用 .isupper())
ans2 = [char for char in born_location if char.isupper()]

# 任務 3: tags 裡所有非小寫字母的字元 (not char.islower())
ans3 = [char for char in tags if not char.islower()]

# 任務 4: quote 裡所有的標點符號
# 注意：quote 常包含中文/特殊引號 “ ”，可一併加入標點符號檢查
punctuation_set = set(string.punctuation + "“”‘’")
ans4 = [char for char in quote if char in punctuation_set]

# =======================================================
# 印出題目要求的預期輸出格式
# =======================================================
print("預期輸出")
print(f"① {ans1}")
print(f"② {ans2}")
print(f"③ {ans3}")
print(f"④ {ans4}")