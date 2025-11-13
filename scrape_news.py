import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

def scrape_yahoo_news():
    """Yahoo!ニュースのトピックスを取得してcsvに保存"""
    url = "https://news.yahoo.co.jp/"

    # Webページを取得
    headers = {
        'User-Agent': 'Mozilla/5.0(Windows NT 10.0; Win64; x64) AppleWebkit/537.36'
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    print("=== Yahoo!ニュースの見出し ===\n")

    # 全てのリンクを取得
    links = soup.find_all('a')
    
    # データを保存するリスト
    news_data = []

    count = 0
    seen_titles = set()  

    for link in links:
        text = link.get_text(strip=True)
        href = link.get('href')

        # 条件　テキストが20文字以上、URLがある、重複していない
        if text and len(text) >= 20 and href and text not in seen_titles:
            count += 1
            seen_titles.add(text)

            print(f"{count}. {text}")
            print(f"  {href}\n")

            # データをリストに追加
            news_data.append({
                'title': text,
                'url': href,
                'scraped_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })

            if count >= 10:  # 10件取得したら終了
                break

    print(f"取得した記事数: {count}")

    # DataFrameに変換
    df = pd.DataFrame(news_data)

    # CSVファイルに保存
    filename = f"yahoo_news_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    df.to_csv(filename, index=False, encoding='utf-8-sig')

    print(f"\nCSVファイルに保存しました： {filename}")

    return df

# 実行
scrape_yahoo_news()



