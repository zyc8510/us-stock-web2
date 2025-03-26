from flask import Flask, render_template, send_file
import requests
from bs4 import BeautifulSoup
import pandas as pd
from googletrans import Translator

app = Flask(__name__)

def fetch_us_stocks():
    url = "https://stockanalysis.com/stocks/"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table')

    symbols, names_en = [], []
    if table:
        rows = table.find_all('tr')[1:]
        for row in rows:
            cols = row.find_all('td')
            if len(cols) >= 2:
                symbols.append(cols[0].text.strip())
                names_en.append(cols[1].text.strip())

    translator = Translator()
    names_ja = []
    for name in names_en:
        try:
            translated = translator.translate(name, src='en', dest='ja')
            names_ja.append(translated.text)
        except:
            names_ja.append("翻訳失敗")

    df = pd.DataFrame({
        '銘柄コード': symbols,
        '会社名（英語）': names_en,
        '会社名（日本語訳）': names_ja
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

if __name__ == "__main__":
    app.run(debug=True)
