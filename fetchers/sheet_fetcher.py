import os, requests
from dotenv import load_dotenv

load_dotenv()

SHEET_ID = os.getenv("GOOGLE_SHEET_ID")

if not SHEET_ID:
    raise Exception("GOOGLE_SHEET_ID missing in .env")

def get_sheet_csv():
    try:
        url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"
        r = requests.get(url, timeout=15)
        r.raise_for_status()
        return r.text
    except Exception as e:
        print("[SHEET FETCH ERROR]", e)
        raise
