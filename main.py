import serial
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import pandas as pd

# Google Sheets setup
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("arduino-attendance-v1-98c58dae64f9.json", scope)
client = gspread.authorize(creds)

sheet = client.open("Attendance").sheet1  # Your Google Sheet name

# Serial port setup (match your port)
ser = serial.Serial('COM3', 115200)  # Or /dev/ttyUSB0 on Linux

TAG_FILE = "tags.csv"

# Optional: UID to Name mapping (or skip and just log UID)
tag_df = pd.read_csv(TAG_FILE)
uid_to_name = dict(zip(tag_df["UID"], tag_df["Name"]))


while True:
    uid = ser.readline().decode().strip()
    name = uid_to_name.get(uid, "Unknown")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    row = [timestamp, uid, name]
    sheet.append_row(row)
    print(f"Logged: {row}")
