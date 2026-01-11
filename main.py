import time, threading
from datetime import datetime
from flask import Flask, send_from_directory
from fetchers.infosys_playwright import InfosysScraper, init_csv, append_price
from config.google_sheets import append_sheet
from fetchers.sheet_fetcher import get_sheet_csv

SYMBOL = "INFY.NS"
CSV_PATH = "data/stock_data.csv"
DELAY_SEC = 60

app = Flask(__name__)

# ---------- FRONTEND ROUTES ----------

@app.route("/")
def home():
    return send_from_directory("frontend", "frontend.html")

@app.route("/frontend/<path:filename>")
def serve_frontend_files(filename):
    return send_from_directory("frontend", filename)

@app.route("/data/<path:filename>")
def serve_data(filename):
    return send_from_directory("data", filename)

# Proxy API to fetch Google Sheet as CSV
@app.route("/api/sheet")
def sheet_api():
    try:
        data = get_sheet_csv()
        return data, 200, {"Content-Type": "text/csv"}
    except Exception as e:
        return str(e), 500

# ---------- SCRAPER LOOP ----------

def scraper_loop():
    init_csv(CSV_PATH)
    scraper = InfosysScraper()

    while True:
        try:
            price = scraper.fetch_price()
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Save to CSV
            append_price(CSV_PATH, now, SYMBOL, price)

            # Save to Google Sheets (env-based creds)
            append_sheet(now, SYMBOL, price)

            print("[OK] Saved:", now, price)

        except Exception as e:
            print("[SCRAPER ERROR]", e)

        time.sleep(DELAY_SEC)

# ---------- START ----------

if __name__ == "__main__":
    t = threading.Thread(target=scraper_loop, daemon=True)
    t.start()

    app.run(host="0.0.0.0", port=5000, debug=True)
