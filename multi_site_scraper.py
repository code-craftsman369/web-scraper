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
        except Exception as e:
            print(f"  ⚠️ エラー ({attempt + 1}/{max_retries}): {str(e)[:50]}...")
            time.sleep(2)
    
    return None

def scrape_site(site_name, url):
    """指定したサイトをスクレイピング"""
    print(f"\n📰 {site_name} を取得中...")
    
    response = scrape_with_retry(url)
    
    if response is None:
        print(f"  ❌ 取得失敗")
        return []
    
    soup = BeautifulSoup(response.content, 'html.parser')
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
            
            news_data.append({
                'site': site_name,
                'title': text,
                'url': href,
                'scraped_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })
            
            if count >= 5:
                break
    
    print(f"  ✅ {len(news_data)}件取得")
    return news_data

def scrape_multiple_sites():
    """複数のサイトからニュースを収集"""
    print("=== 複数サイトからニュース収集 ===")
    
    sites = [
        ('Yahoo!ニュース', 'https://news.yahoo.co.jp/'),
        ('NHK NEWS WEB', 'https://www3.nhk.or.jp/news/'),
    ]
    
    all_news = []
    
    for site_name, url in sites:
        news = scrape_site(site_name, url)
        all_news.extend(news)
        time.sleep(2)
    
    if all_news:
        df = pd.DataFrame(all_news)
        filename = f"multi_news_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        df.to_csv(filename, index=False, encoding='utf-8-sig')
        
        print(f"\n📊 合計: {len(all_news)}件の記事を取得")
        print(f"📁 保存: {filename}")
        
        return df
    else:
        print("\n❌ 記事が見つかりませんでした")
        return None

# 実行
scrape_multiple_sites()