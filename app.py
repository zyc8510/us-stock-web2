import requests
import pandas as pd
from googletrans import Translator

def fetch_us_stocks():
    url = "https://finance.yahoo.com/screener/predefined/ms_technology"
    response = requests.get(url, timeout=10)
    data = response.json()

    results = data.get("finance", {}).get("result", [])[0].get("quotes", [])

    symbols = []
    names_en = []

    for stock in results:
        symbols.append(stock.get("symbol", ""))
        names_en.append(stock.get("shortName", "N/A"))

    # 翻译为日文
    translator = Translator()
    names_ja = []
    for name in names_en:
        try:
            translated = translator.translate(name, src='en', dest='ja')
            names_ja.append(translated.text)
        except:
            names_ja.append("翻訳失敗")

    df = pd.DataFrame({
        "銘柄コード": symbols,
        "会社名（英語）": names_en,
        "会社名（日本語訳）": names_ja
    })
    df.to_csv("米国株一覧_日本語.csv", index=False, encoding='utf-8-sig')
    return df

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/scrape")
def scrape():
    fetch_us_stocks()
    return send_file("米国株一覧_日本語.csv", as_attachment=True)

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # 从环境变量 PORT 读取端口
    app.run(host="0.0.0.0", port=port, debug=True)
