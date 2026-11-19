"""Run:  python demo_email.py   -> sends (or dry-runs) a welcome email."""
from app.emailer import send_email, welcome_email

subject, body = welcome_email("Asha", "Python")
sent = send_email("asha@example.com", subject, body)
print("Really sent!" if sent else "Dry-run only (no SMTP settings in .env).")
