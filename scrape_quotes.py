import pandas as pd
import requests
from bs4 import BeautifulSoup

BASE_URL = "http://quotes.toscrape.com"
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,"
        " like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )
}

# 1. 取得首頁 HTML
response = requests.get(BASE_URL, headers=HEADERS, timeout=10)
response.encoding = "utf-8"
soup = BeautifulSoup(response.text, "html.parser")

# 取得首頁所有名言卡片
quote_blocks = soup.find_all("div", class_="quote")
data_list = []

# 用於快取已抓取過的作者詳細資訊，避免重複向同一個作者頁面發送請求
author_info_cache = {}

print(f"正在爬取首頁名言資訊，共找到 {len(quote_blocks)} 則名言...")

for block in quote_blocks:
    # 擷取名言內容
    quote_text = block.find("span", class_="text").text.strip()

    # 擷取作者姓名
    author_name = block.find("small", class_="author").text.strip()

    # 擷取標籤（以半形逗點或空白合併）
    tag_elements = block.find_all("a", class_="tag")
    tags = ", ".join([tag.text.strip() for tag in tag_elements])

    # 取得作者頁面連結 (about)
    about_link = block.find("a", href=True)
    author_detail_url = BASE_URL + about_link["href"]

    # 2. 進入作者頁面抓取 born_date 與 born_location
    if author_name not in author_info_cache:
        author_resp = requests.get(author_detail_url, headers=HEADERS, timeout=10)
        author_resp.encoding = "utf-8"
        author_soup = BeautifulSoup(author_resp.text, "html.parser")

        born_date = author_soup.find("span", class_="author-born-date").text.strip()
        born_location = author_soup.find("span", class_="author-born-location").text.strip()

        author_info_cache[author_name] = {
            "born_date": born_date,
            "born_location": born_location,
        }
    else:
        born_date = author_info_cache[author_name]["born_date"]
        born_location = author_info_cache[author_name]["born_location"]

    # 儲存單筆名言完整資料
    data_list.append({
        "name": author_name,
        "born_date": born_date,
        "born_location": born_location,
        "quote": quote_text,
        "tags": tags,
    })

# 3. 轉換為 DataFrame 並指定題目要求之欄位名稱
columns = ["name", "born_date", "born_location", "quote", "tags"]
df = pd.DataFrame(data_list, columns=columns)

# 4. 匯出為 authors.csv（encoding='utf-8-sig' 可防止 Excel 打開時中文或特殊符號亂碼）
csv_filename = "authors.csv"
df.to_csv(csv_filename, index=False, encoding="utf-8-sig")

print(f"\n爬取完成！已成功產生 {csv_filename}，共 {len(df)} 筆資料。")
print(df.head())