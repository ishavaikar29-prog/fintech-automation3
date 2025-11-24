# report_parent.py

import os
from typing import Dict

from utils.error_handler import LOG_FILE
from utils.api_client import fetch_api_data
from utils.excel_utils import create_excel
from utils.email_body import build_email_body
from utils.email_sender import send_email_with_attachments


def get_env(name: str, default: str | None = None, required: bool = False) -> str | None:
    """Simple helper to read environment variables with optional required flag."""
    value = os.getenv(name, default)
    if required and not value:
        raise RuntimeError(f"Required environment variable '{name}' is not set.")
    return value

def main() -> None:
    print("Starting Multi-API Report (parent script)...")

    # ---------------- SMTP Config ----------------
    SMTP_HOST = get_env("SMTP_HOST", required=True)
    SMTP_PORT_STR = get_env("SMTP_PORT", "587")
    SMTP_USER = get_env("SMTP_USER", required=True)
    SMTP_PASS = get_env("SMTP_PASS", required=True)
    TO_EMAIL   = get_env("TO_EMAIL", required=True)

    SMTP_PORT = int(SMTP_PORT_STR)

    # ---------------- API URLs ----------------
    API1_URL = get_env("API1_URL", "https://jsonplaceholder.typicode.com/users")
    API2_URL = get_env("API2_URL", "https://jsonplaceholder.typicode.com/posts")
    API3_URL = get_env("API3_URL", "https://jsonplaceholder.typicode.com/todos")

    API_KEY = get_env("API_KEY")
    headers: Dict[str, str] = {"Authorization": f"Bearer {API_KEY}"} if API_KEY else {}

    # ---------------- API Calls ----------------
    users = fetch_api_data(API1_URL, headers)
    posts = fetch_api_data(API2_URL, headers)
    todos = fetch_api_data(API3_URL, headers)

    # ---------------- Excel Creation ----------------
    excel_file = create_excel(users, posts, todos)

    # ---------------- Check for errors ----------------
    attach_logs = False
    if os.path.exists(LOG_FILE) and os.path.getsize(LOG_FILE) > 0:
        attach_logs = True

    # ---------------- Build Email Body ----------------
    body = build_email_body(users, posts, todos, has_errors=attach_logs)

    # ---------------- Attachments ----------------
    attachments = [excel_file]
    if attach_logs:
        attachments.append(LOG_FILE)

    # ---------------- Send Email ----------------
    send_email_with_attachments(
        smtp_host=SMTP_HOST,
        smtp_port=SMTP_PORT,
        smtp_user=SMTP_USER,
        smtp_pass=SMTP_PASS,
        to_email=TO_EMAIL,
        subject="Daily Multi-API Report",
        body=body,
        attachments=attachments,
    )

    print("Parent script finished.")

if __name__ == "__main__":
    main()

