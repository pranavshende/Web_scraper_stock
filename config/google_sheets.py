import os, gspread
from dotenv import load_dotenv
from google.oauth2.service_account import Credentials

load_dotenv()

SHEET_ID = os.getenv("GOOGLE_SHEET_ID")

def get_creds():
    private_key = os.getenv("GOOGLE_PRIVATE_KEY")

    # Fix escaped newlines
    if private_key:
        private_key = private_key.replace("\\n", "\n")

    info = {
        "type": os.getenv("GOOGLE_TYPE"),
        "project_id": os.getenv("GOOGLE_PROJECT_ID"),
        "private_key_id": os.getenv("GOOGLE_PRIVATE_KEY_ID"),
        "private_key": private_key,
        "client_email": os.getenv("GOOGLE_CLIENT_EMAIL"),
        "client_id": os.getenv("GOOGLE_CLIENT_ID"),
        "token_uri": os.getenv("GOOGLE_TOKEN_URI"),
    }

    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]

    return Credentials.from_service_account_info(info, scopes=scopes)

_sheet = None

def get_sheet():
    global _sheet
    if _sheet is None:
        creds = get_creds()
        client = gspread.authorize(creds)
        _sheet = client.open_by_key(SHEET_ID).sheet1
    return _sheet

def append_sheet(timestamp, symbol, price):
    try:
        sheet = get_sheet()
        sheet.append_row([timestamp, symbol, price])
        print("[SHEET] Saved")
    except Exception as e:
        print("[SHEET ERROR]", e)
