import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import csv
import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

EMAIL_ADDRESS = "vishnuagarwal27@gmail.com"
EMAIL_PASSWORD = "vvnmuzrrzcufbgus"

def load_table():
    for row in tree.get_children():
        tree.delete(row)
    try:
        with open("agreements.csv", newline="") as file:
            reader = csv.reader(file)
            next(reader, None)  # Skip header
            for row in reader:
                tree.insert("", tk.END, values=row)
    except FileNotFoundError:
        with open("agreements.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Agreement Name", "Expiry Date", "Assigned To", "Email"])

def add_agreement():
    name = entry_name.get()
    expiry = entry_expiry.get()
    assigned = entry_assigned.get()
    email = entry_email.get()
    if not name or not expiry or not assigned or not email:
        messagebox.showerror("Error", "All fields are required")
        return
    try:
        datetime.datetime.strptime(expiry, "%Y-%m-%d")
    except ValueError:
        messagebox.showerror("Error", "Date must be YYYY-MM-DD")
        return
    with open("agreements.csv", "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([name, expiry, assigned, email])
    load_table()
    clear_entries()

def clear_entries():
    entry_name.delete(0, tk.END)
    entry_expiry.delete(0, tk.END)
    entry_assigned.delete(0, tk.END)
    entry_email.delete(0, tk.END)

def send_reminders():
    today = datetime.date.today()
    try:
        with open("agreements.csv", newline="") as file:
            reader = csv.reader(file)
            next(reader, None)
            for row in reader:
                if not row or len(row) < 4:
                    continue
                name, expiry, assigned, email = row
                try:
                    expiry_date = datetime.datetime.strptime(expiry, "%Y-%m-%d").date()
                    days_left = (expiry_date - today).days
                    if days_left == 30:
                        send_email(email, name, expiry)
                except ValueError:
                    continue
        messagebox.showinfo("Success", "Reminders sent successfully")
    except FileNotFoundError:
        messagebox.showerror("Error", "agreements.csv not found")

def send_email(to_address, agreement_name, expiry_date):
    try:
        msg = MIMEMultipart()
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = to_address
        msg["Subject"] = f"Reminder: Agreement '{agreement_name}' Expiring Soon"
        body = f"Dear User,\n\nThe agreement '{agreement_name}' will expire on {expiry_date}.\nPlease take necessary action.\n\nRegards,\nAgreement Tracker"
        msg.attach(MIMEText(body, "plain"))

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)
    except Exception as e:
        print(f"Failed to send email to {to_address}: {e}")

root = tk.Tk()
root.title("Agreement Tracker")
root.geometry("700x500")

frame_form = tk.Frame(root)
frame_form.pack(pady=10)

tk.Label(frame_form, text="Agreement Name").grid(row=0, column=0, padx=5, pady=5)
entry_name = tk.Entry(frame_form)
entry_name.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_form, text="Expiry Date (YYYY-MM-DD)").grid(row=1, column=0, padx=5, pady=5)
entry_expiry = tk.Entry(frame_form)
entry_expiry.grid(row=1, column=1, padx=5, pady=5)

tk.Label(frame_form, text="Assigned To").grid(row=2, column=0, padx=5, pady=5)
entry_assigned = tk.Entry(frame_form)
entry_assigned.grid(row=2, column=1, padx=5, pady=5)

tk.Label(frame_form, text="Email").grid(row=3, column=0, padx=5, pady=5)
entry_email = tk.Entry(frame_form)
entry_email.grid(row=3, column=1, padx=5, pady=5)

btn_add = tk.Button(frame_form, text="Add Agreement", command=add_agreement)
btn_add.grid(row=4, column=0, columnspan=2, pady=10)

columns = ("Agreement Name", "Expiry Date", "Assigned To", "Email")
tree = ttk.Treeview(root, columns=columns, show="headings")
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=150)
tree.pack(pady=10, fill="x")

btn_reminder = tk.Button(root, text="Send 30-Day Reminders", command=send_reminders)
btn_reminder.pack(pady=10)

load_table()
root.mainloop()