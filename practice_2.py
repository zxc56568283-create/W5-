import os
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

# 1. 爬取首頁 HTML
response = requests.get(BASE_URL, headers=HEADERS, timeout=10)
response.encoding = "utf-8"
soup = BeautifulSoup(response.text, "html.parser")

quote_blocks = soup.find_all("div", class_="quote")
data_list = []
author_cache = {}

print("正在爬取 Quotes to Scrape 首頁名言與作者詳細資訊...")

for block in quote_blocks:
    # 取得名言文字並【去掉頭尾引號】（含一般引號與特殊雙引號 “ ”）
    raw_quote = block.find("span", class_="text").text.strip()
    clean_quote = raw_quote.strip('“”"')

    # 取得作者姓名
    author_name = block.find("small", class_="author").text.strip()

    # 取得標籤
    tag_elements = block.find_all("a", class_="tag")
    tags = ", ".join([tag.text.strip() for tag in tag_elements])

    # 取得作者頁面連結並爬取作者資訊
    about_link = block.find("a", href=True)
    author_url = BASE_URL + about_link["href"]

    if author_name not in author_cache:
        author_resp = requests.get(author_url, headers=HEADERS, timeout=10)
        author_resp.encoding = "utf-8"
        author_soup = BeautifulSoup(author_resp.text, "html.parser")

        born_date = author_soup.find("span", class_="author-born-date").text.strip()
        born_location = author_soup.find("span", class_="author-born-location").text.strip()

        author_cache[author_name] = {
            "born_date": born_date,
            "born_location": born_location,
        }
    else:
        born_date = author_cache[author_name]["born_date"]
        born_location = author_cache[author_name]["born_location"]

    data_list.append({
        "name": author_name,
        "born_date": born_date,
        "born_location": born_location,
        "quote": clean_quote,
        "tags": tags,
    })

# 2. 轉換為 DataFrame 並指定欄位名稱
columns = ["name", "born_date", "born_location", "quote", "tags"]
df = pd.DataFrame(data_list, columns=columns)

# 存成 authors.csv（存於當前程式碼同目錄）
base_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(base_dir, "authors.csv")
df.to_csv(csv_path, index=False, encoding="utf-8-sig")
print(f"已成功匯出至 {csv_path}\n")

# =======================================================
# 題目統計分析部分（針對首頁出現的作者進行去重分析）
# =======================================================

# 建立獨立作者的 DataFrame（去掉重複的作者）
unique_authors = df[["name", "born_date", "born_location"]].drop_duplicates(subset=["name"]).copy()

# --- 題目要求 2: 統計各國有幾位作者？ ---
# born_location 格式通常為 "in Ulm, Germany" 或 "in Paris, France"
# 透過逗號切分取最後一段，並去掉多餘空格與 "in " 字眼
def extract_country(loc):
    if not isinstance(loc, str):
        return "Unknown"
    parts = loc.split(",")
    country = parts[-1].strip()
    if country.startswith("in "):
        country = country[3:].strip()
    return country

unique_authors["country"] = unique_authors["born_location"].apply(extract_country)
country_counts = unique_authors["country"].value_counts()

print("================ 各國作者人數統計 ================")
print(country_counts)

# --- 題目要求 3: 誰最早出生？ ---
# 將 born_date (例如 "March 14, 1879") 轉換為日期格式進行排序
unique_authors["parsed_birth_date"] = pd.to_datetime(unique_authors["born_date"], format="%B %d, %Y", errors="coerce")
earliest_author = unique_authors.sort_values(by="parsed_birth_date").iloc[0]

print("\n================ 最早出生的作者 ================")
print(f"姓名: {earliest_author['name']}")
print(f"出生日期: {earliest_author['born_date']}")
print(f"出生地點: {earliest_author['born_location']}")