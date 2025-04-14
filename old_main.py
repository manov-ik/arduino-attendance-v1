import serial
import pandas as pd
from datetime import datetime

TAG_FILE = "tags.csv"
LOG_FILE = "attendance_log.csv"

# Load UID-to-name mappings
tag_df = pd.read_csv(TAG_FILE)
uid_to_name = dict(zip(tag_df["UID"], tag_df["Name"]))

# Set up serial connection (change 'COM3' to your actual port)
ser = serial.Serial('COM3', 115200)  # Or '/dev/ttyUSB0' on Linux/Mac

print("📡 Listening for RFID tags...")

while True:
    try:
        line = ser.readline().decode().strip()
        if line:
            uid = line
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            name = uid_to_name.get(uid, "Unknown")

            print(f"✅ {name} ({uid}) at {timestamp}")

            # Save to CSV
            pd.DataFrame([[name, uid, timestamp]], columns=["Name", "UID", "Timestamp"]) \
              .to_csv(LOG_FILE, mode='a', header=not pd.io.common.file_exists(LOG_FILE), index=False)

    except Exception as e:
        print(f"Error: {e}")
