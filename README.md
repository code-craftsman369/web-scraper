# Web Scraper

Beautiful Soupを使ったWebスクレイピングツール

## 🌟 機能

- ✅ Yahoo!ニュースから記事を自動収集
- ✅ タイトルとURLを抽出
- ✅ CSVファイルに保存
- ✅ タイムスタンプ付き

## 🛠 技術スタック

- **Python** 3.11
- **Beautiful Soup** 4
- **Requests**
- **Pandas**

## 📦 インストール

### 1. リポジトリをクローン
```bash
git clone https://github.com/code-craftsman369/web-scraper.git
cd web-scraper
```

### 2. 依存パッケージをインストール
```bash
pip install beautifulsoup4 requests pandas lxml
```

## 🚀 使い方

### ニュースをスクレイピング
```bash
python scrape_news.py
```

実行すると：
1. Yahoo!ニュースから最新10件の記事を取得
2. `yahoo_news_YYYYMMDD_HHMMSS.csv` という名前でCSVファイルを保存

## 📊 出力データ

### CSVファイルの構造
```csv
title,url,scraped_at
記事タイトル,記事URL,取得日時
```

**例**：
```csv
title,url,scraped_at
インバウンド客「無断キャンセル」続出...,https://news.yahoo.co.jp/articles/...,2025-11-14 05:44:56
```

## 📝 コード例

### 基本的な使い方
```python
import requests
from bs4 import BeautifulSoup

# Webページを取得
url = "https://example.com"
response = requests.get(url)

# HTMLを解析
soup = BeautifulSoup(response.content, 'html.parser')

# タイトルを取得
title = soup.find('title').text
print(title)
```

## 📚 学習内容

このプロジェクトを通じて学んだこと：

- Beautiful Soupの基本的な使い方
- HTML要素の抽出方法
- Webスクレイピングの実践
- Pandasを使ったデータ処理
- CSVファイルへのデータ保存

## 🔜 今後の改善予定

- [ ] 複数のニュースサイトに対応
- [ ] カテゴリ別にスクレイピング
- [ ] 定期実行機能（スケジューラー）
- [ ] データベースへの保存
- [ ] エラーハンドリングの強化

## ⚠️ 注意事項

### Webスクレイピングの倫理

- 対象サイトの利用規約を確認してください
- robots.txtを尊重してください
- サーバーに負荷をかけないよう、適切な間隔を空けてください
- 取得したデータの利用は個人利用の範囲内にしてください

## 📄 ライセンス

MIT License

## 👤 作成者

Tatsu - Python Developer
- GitHub: [@code-craftsman369](https://github.com/code-craftsman369)

## 🙏 謝辞

- [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/) - HTML/XML解析ライブラリ
- [Yahoo!ニュース](https://news.yahoo.co.jp/) - データ提供元
