import csv
import smtplib
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# === CONFIGURATION ===
SENDER_EMAIL = "vishnuagarwal27@gmail.com"        # Change this to your Gmail/Outlook
APP_PASSWORD = "Casanova@71#"      # App password (not your real password)

CSV_FILE = "records.csv"                     # Path to the CSV file

# === LOAD RECORDS AND CHECK FOR UPCOMING EXPIRY ===
def load_records():
    today = datetime.today().date()
    reminder_day = today + timedelta(days=30)

    reminders = []

    with open(CSV_FILE, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            expiry_str = str(row['Expiry Date']).strip()
if not expiry_str or expiry_str.lower() == 'nan':
    continue  # Skip rows with empty or invalid expiry dates
expiry_str = str(row['Expiry Date']).strip()

# Skip empty or invalid dates
if not expiry_str or expiry_str.lower() in ['nan', 'none']:
    print(f"Skipping row {index} due to missing expiry date")
    continue

expiry_raw = row['Expiry Date']

try:
    expiry_str = str(expiry_raw).strip()
    if not expiry_str or expiry_str.lower() in ['nan', 'none']:
        print(f"Skipping row {index} due to missing or invalid expiry date: {expiry_raw}")
        continue
    expiry_date = datetime.strptime(expiry_str, "%Y-%m-%d")
except Exception as e:
    print(f"Error parsing date on row {index}: {e} | Value: {expiry_raw}")
    continue

.date()
            if expiry_date == reminder_day:
                reminders.append(row)
    
    return reminders

# === SEND EMAIL ===
def send_email(to_email, agreement_name, expiry_date, assigned_to):
    subject = f"Reminder: {agreement_name} expires on {expiry_date}"
    body = f"""Dear {assigned_to},

This is a reminder that the agreement '{agreement_name}' is set to expire on {expiry_date}.

Please take the necessary steps for renewal.

Regards,
Agreement Tracker
"""

    message = MIMEMultipart()
    message["From"] = SENDER_EMAIL
    message["To"] = to_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(SENDER_EMAIL, APP_PASSWORD)
            server.send_message(message)
            print(f"Reminder sent to {to_email}")
    except Exception as e:
        print(f"Failed to send email to {to_email}: {e}")

# === MAIN FUNCTION ===
def main():
    reminders = load_records()
    if not reminders:
        print("No agreements expiring in the next 30 days.")
        return

    for record in reminders:
        send_email(
            record["Email"],
            record["Agreement Name"],
            record["Expiry Date"],
            record["Assigned To"]
        )

if __name__ == "__main__":
    main()
