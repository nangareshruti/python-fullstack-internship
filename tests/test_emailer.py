"""Tests for task 11 (email module). No real email is ever sent."""
import os
from unittest.mock import MagicMock, patch

import pytest

from app.emailer import build_message, send_email, welcome_email
from app.models import ValidationError


def test_build_message_fields():
    msg = build_message("a@x.com", "Hello", "Body text", "me@x.com")
    assert msg["To"] == "a@x.com"
    assert msg["From"] == "me@x.com"
    assert msg["Subject"] == "Hello"
    assert "Body text" in msg.get_content()


def test_welcome_email_text():
    subject, body = welcome_email("Asha", "Python")
    assert "Asha" in subject and "Python" in subject
    assert "registration" in body


def test_dry_run_when_no_smtp_host():
    with patch.dict(os.environ, {"SMTP_HOST": ""}):
        assert send_email("a@x.com", "Hi", "Test") is False


def test_invalid_recipient_rejected():
    with pytest.raises(ValidationError):
        send_email("not-an-email", "Hi", "Test")


def test_empty_subject_rejected():
    with pytest.raises(ValidationError):
        send_email("a@x.com", "  ", "Test")


def test_real_send_uses_smtp():
    env = {"SMTP_HOST": "smtp.test.com", "SMTP_USER": "u", "SMTP_PASSWORD": "p"}
    with patch.dict(os.environ, env), patch("app.emailer.smtplib.SMTP") as smtp:
        server = MagicMock()
        smtp.return_value.__enter__.return_value = server
        assert send_email("a@x.com", "Hi", "Test") is True
        server.starttls.assert_called_once()
        server.login.assert_called_once_with("u", "p")
        server.send_message.assert_called_once()
