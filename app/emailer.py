"""Task 11: email automation module.

Settings come from the .env file. If SMTP_HOST is empty, the module runs in
DRY-RUN mode: it prints and logs the email instead of sending it. That makes
it safe to practise without a real email account.
"""
import os
import smtplib
from email.message import EmailMessage

from app import config  # noqa: F401  (importing it loads the .env file)
from app.logger import log
from app.models import EMAIL_RE, ValidationError
from app.retry import retry


def _settings() -> dict:
    # Read at call time so changes in .env / environment are picked up
    return {
        "host": os.getenv("SMTP_HOST", ""),
        "port": int(os.getenv("SMTP_PORT", "587")),
        "user": os.getenv("SMTP_USER", ""),
        "password": os.getenv("SMTP_PASSWORD", ""),
        "sender": os.getenv("EMAIL_FROM", "noreply@example.com"),
    }


def build_message(to: str, subject: str, body: str, sender: str) -> EmailMessage:
    msg = EmailMessage()
    msg["From"] = sender
    msg["To"] = to
    msg["Subject"] = subject
    msg.set_content(body)
    return msg


@retry(max_attempts=3, delay=1.0, exceptions=(smtplib.SMTPException, OSError))
def _send_via_smtp(msg: EmailMessage, s: dict) -> None:
    with smtplib.SMTP(s["host"], s["port"], timeout=10) as server:
        server.starttls()
        if s["user"]:
            server.login(s["user"], s["password"])
        server.send_message(msg)


def send_email(to: str, subject: str, body: str) -> bool:
    """Send an email. Returns True if really sent, False in dry-run mode."""
    if not EMAIL_RE.match(to):
        raise ValidationError(f"Invalid recipient email: {to}")
    if not subject.strip():
        raise ValidationError("Subject cannot be empty")

    s = _settings()
    msg = build_message(to, subject, body, s["sender"])

    if not s["host"]:
        log.info("DRY-RUN email to=%s subject=%s", to, subject)
        print(f"[DRY-RUN] To: {to}\n[DRY-RUN] Subject: {subject}\n{body}")
        return False

    _send_via_smtp(msg, s)
    log.info("EMAIL SENT to=%s subject=%s", to, subject)
    return True


def welcome_email(name: str, course: str) -> tuple:
    """Returns (subject, body) for a new student."""
    subject = f"Welcome to {course}, {name}!"
    body = (
        f"Hi {name},\n\n"
        f"Your registration for {course} is complete.\n"
        "We are happy to have you with us.\n\n"
        "Regards,\nStudent Management Team"
    )
    return subject, body
