import time, os, csv
from datetime import datetime, timedelta
from playwright.sync_api import sync_playwright

SYMBOL = "INFY.NS"
URL = "https://finance.yahoo.com/quote/INFY.NS"
CSV_PATH = "data/stock_data.csv"
DELAY_SEC = 30   # fetch every 5 seconds

# ---------- SCRAPER ----------
class InfosysScraper:
    def __init__(self):
        self.play = sync_playwright().start()
        self.browser = self.play.chromium.launch(headless=True)
        self.page = self.browser.new_page()

    def fetch_price(self):
        self.page.goto(URL, timeout=60000)
        self.page.wait_for_selector(
            f'fin-streamer[data-symbol="{SYMBOL}"][data-testid="qsp-price"]',
            timeout=30000
        )
        time.sleep(1)

        price = self.page.locator(
            f'fin-streamer[data-symbol="{SYMBOL}"][data-testid="qsp-price"]'
        ).first.inner_text()

        return price.replace(",", "")

    def close(self):
        self.browser.close()
        self.play.stop()

# ---------- CSV HELPERS ----------
def init_csv(path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if not os.path.exists(path):
        with open(path, "w", newline="") as f:
            csv.writer(f).writerow(["timestamp", "symbol", "price"])

def clean_old_data(path):
    if not os.path.exists(path):
        return

    with open(path, "r") as f:
        rows = list(csv.reader(f))

    header, data = rows[0], rows[1:]
    one_week_ago = datetime.now() - timedelta(days=7)

    filtered = []
    for r in data:
        try:
            ts = datetime.strptime(r[0], "%Y-%m-%d %H:%M:%S")
            if ts >= one_week_ago:
                filtered.append(r)
        except:
            pass

    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(filtered)

def append_price(path, timestamp, symbol, price):
    clean_old_data(path)
    with open(path, "a", newline="") as f:
        csv.writer(f).writerow([timestamp, symbol, price])

# ---------- MAIN LOOP ----------
if __name__ == "__main__":
    init_csv(CSV_PATH)
    scraper = InfosysScraper()

    try:
        while True:
            try:
                price = scraper.fetch_price()
                now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                append_price(CSV_PATH, now, SYMBOL, price)
                print("Saved:", now, price)
            except Exception as e:
                print("Fetch failed:", e)

            time.sleep(DELAY_SEC)   # 5 seconds
    finally:
        scraper.close()
