import os, requests
from dotenv import load_dotenv

load_dotenv()

SHEET_ID = os.getenv("GOOGLE_SHEET_ID")

def get_sheet_csv():
    url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"
    r = requests.get(url, timeout=15)
    r.raise_for_status()
    return r.text
