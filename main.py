import time, threading
from datetime import datetime
from flask import Flask, send_from_directory
from fetchers.infosys_playwright import InfosysScraper, init_csv, append_price

SYMBOL = "INFY.NS"
CSV_PATH = "data/stock_data.csv"
DELAY_SEC = 60

app = Flask(__name__)

# ---------- ROUTES ----------
@app.route("/")
def home():
    return send_from_directory("frontend", "frontend.html")

@app.route("/frontend/<path:filename>")
def serve_frontend_files(filename):
    return send_from_directory("frontend", filename)

@app.route("/data/<path:filename>")
def serve_data(filename):
    return send_from_directory("data", filename)

# ---------- SCRAPER LOOP ----------
def scraper_loop():
    init_csv(CSV_PATH)
    scraper = InfosysScraper()

    while True:
        try:
            price = scraper.fetch_price()
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            append_price(CSV_PATH, now, SYMBOL, price)
            print("Saved:", now, price)
        except Exception as e:
            print("Fetch failed:", e)

        time.sleep(DELAY_SEC)

# ---------- START ----------
if __name__ == "__main__":
    t = threading.Thread(target=scraper_loop, daemon=True)
    t.start()

    app.run(host="0.0.0.0", port=5000, debug=True)
