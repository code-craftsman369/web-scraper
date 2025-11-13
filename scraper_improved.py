import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import time

def scrape_with_retry(url, max_retries=3):
    """リトライ機能付きでWebページを取得"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }

    for attempt in range(max_retries):
        try:
            response = requests.get(url, headers=headers, timeout=10)

            if response.status_code == 200:
                return response
            else:
                print(f"ステータスコード: {response.status_code}")

        except requests.exceptions.Timeout:
            print(f"タイムアウト: {attempt + 1}回目")
            time.sleep(2)

        except requests.exceptions.RequestException as e:
            print(f"エラー: {e}")
            time.sleep(2)

    return None

def scrape_yahoo_news():
    """Yahoo!ニュースをスクレイピング（改善版）"""
    url = "https://news.yahoo.co.jp/"

    print("=== Yahoo!ニュース取得開始 ===\n")

    # リトライ機能付きで取得
    response = scrape_with_retry(url)

    if response is None:
        print("❌ ニュースの取得に失敗しました")
        return None
    
    soup = BeautifulSoup(response.content, "html.parser")
    links = soup.find_all('a')

    news_data = []
    count = 0
    seen_titles = set()

    for link in links:
        text = link.get_text(strip=True)
        href = link.get('href')

        if text and len(text) >= 20 and href and text not in seen_titles:
            count += 1
            seen_titles.add(text)

            print(f"{count}. {text[ :50]}...")

            news_data.append({
                'title': text,
                'url': href,
                'scraped_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })

            if count >= 10:
                break
    
    if news_data:
        df = pd.DataFrame(news_data)
        filename = f"yahoo_news_{datetime.now().strftime('%Y-%m-%d_%H:%M:%S')}.csv"
        df.to_csv(filename, index=False, encoding='utf-8-sig')

        print(f"\n✅ 成功: {len(news_data)}件の記事を取得")
        print(f"📁 保存: {filename}")

        return df
    else:
        print("❌ 記事が見つかりませんでした")
        return None
    
# 実行
scrape_yahoo_news()

