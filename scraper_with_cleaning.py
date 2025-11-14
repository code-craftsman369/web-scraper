import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import time
import re

def clean_text(text):
    """テキストをクリーニング"""
    # 先頭の数字と記号を削除（例：1,2,など）
    text = re.sub(r'^[\d\s]+', '', text)

    # 末尾の日付や時刻を削除（例：11/13(木)22:30）
    text = re.sub(r'\d{1,2}/\d{1,2}\([月火水木金土日]\)\d{1,2}:\d{2}$', '', text)
    
    # 複数のスペースを1つに
    text = re.sub(r'\s+', '', text)

    # 前後の空白を削除
    text = text.strip()

    return text

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
        except Exception as e:
            print(f"  ⚠️ エラー ({attempt + 1}/{max_retries})")
            time.sleep(2)

    return None

def scrape_yahoo_news_clean():
    """Yahoo!ニュースをスクレイピング（クリーニング付き）"""
    url = "https://news.yahoo.co.jp/"
    
    print("=== Yahoo!ニュース取得開始（クリーニング機能付き） ===\n")
    
    response = scrape_with_retry(url)

    if response is None:
        print("❌ ニュースの取得に失敗しました")
        return None
    
    soup = BeautifulSoup(response.content, 'html.parser')
    links = soup.find_all('a')

    news_data = []
    seen_titles = set()

    for link in links:
        text = link.get_text(strip=True)
        href = link.get('href')

        if text and len(text) >= 20 and href:
            # テキストをクリーニング
            cleaned_text = clean_text(text)

            # 重複チェック（クリーニング後のテキストで）
            if cleaned_text and len(cleaned_text) >= 15 and cleaned_text not in seen_titles:
                seen_titles.add(cleaned_text)

                news_data.append({
                    'title': cleaned_text,
                    'url': href,
                    'scraped_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                })

                print(f"{len(news_data)}. {cleaned_text[:60]}...")
                
                if len(news_data) >= 10:
                    break

    if news_data:
        df = pd.DataFrame(news_data)
        
        # 重複URLを削除
        df = df.drop_duplicates(subset=['url'], keep='first')
        
        filename = f"yahoo_news_cleaned_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        df.to_csv(filename, index=False, encoding='utf-8-sig')
        
        print(f"\n✅ 成功: {len(df)}件の記事を取得（重複削除後）")
        print(f"📁 保存: {filename}")
        
        return df
    else:
        print("❌ 記事が見つかりませんでした")
        return None

# 実行
scrape_yahoo_news_clean()

