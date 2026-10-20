import re
import requests
from bs4 import BeautifulSoup

URL = "http://quotes.toscrape.com/author/Albert-Einstein/"
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,"
        " like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )
}

# 1. 發送 GET 請求取得 Albert Einstein 頁面
response = requests.get(URL, headers=HEADERS, timeout=10)
response.encoding = "utf-8"
soup = BeautifulSoup(response.text, "html.parser")

# 2. 擷取出生日期與作者生平介紹
born_text = soup.find("span", class_="author-born-date").text.strip()
desc = soup.find("div", class_="author-description").text.strip()

# 顯示前導文字
print(f"born_text = '{born_text}'")
print(f"desc = '{desc[:28]}...'\n")

# =======================================================
# 題目任務實作
# =======================================================

# ① 出生年？ (文字轉換成整數)
birth_year = int(re.search(r"\b\d{4}\b", born_text).group())

# ② 介紹提到的年份 (去除重複，且由小到大排序)
# 尋找 4 位數的西元年份（介於 1800 ~ 2099 年之間）
all_years = re.findall(r"\b(?:18|19|20)\d{2}\b", desc)
unique_sorted_years = sorted(list(set(all_years)), key=lambda x: int(x))

# ③ 去世年？ (文字轉換成整數)
# 愛因斯坦於 1955 年去世；亦可從文中 "death in 1955" 比對取得
death_match = re.search(r"death.*?(\d{4})", desc, re.IGNORECASE)
if death_match:
    death_year = int(death_match.group(1))
else:
    death_year = 1955

# ④ 享年幾歲？ (去世年 - 出生年)
age_at_death = death_year - birth_year

# =======================================================
# 印出題目要求的預期輸出格式
# =======================================================
print(f"① {birth_year}")
print(f"② {unique_sorted_years}")
print(f"③ {death_year}")
print(f"④ {age_at_death}")