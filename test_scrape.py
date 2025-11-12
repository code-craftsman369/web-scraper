import requests
from bs4 import BeautifulSoup

# テスト用のシンプルなWebページを取得
url = "https://example.com"

# webページを取得
response = requests.get(url)

# HTMLを解析
soup = BeautifulSoup(response.content, 'html.parser')

# タイトルを取得
title = soup.find('title').text
print(f"ページタイトル: {title}")

# すべての段落を取得
paragraphs = soup.find_all('p')
print(f"\n段落数: {len(paragraphs)}")

# 最初の段落を表示
if paragraphs:
    print(f"\n最初の段落:\n{paragraphs[0].text}")


