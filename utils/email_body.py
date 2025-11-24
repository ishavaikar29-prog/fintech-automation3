# email_body.py

from datetime import datetime, timezone
from typing import Sequence, Mapping, Any

def build_email_body(
    users: Sequence[Mapping[str, Any]],
    posts: Sequence[Mapping[str, Any]],
    todos: Sequence[Mapping[str, Any]],
    has_errors: bool
) -> str:
    """Create the email body text with counts and optional warning."""
    body = (
        "Hello,\n\n"
        "Here is your automated multi-API report.\n\n"
        f"Users records: {len(users)}\n"
        f"Posts records: {len(posts)}\n"
        f"Todos records: {len(todos)}\n\n"
    )

    if has_errors:
        body += "⚠ Some errors occurred during processing. See attached error log.\n\n"

    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S %Z")
    body += f"Generated at: {generated_at}\n\n-- Automation Bot"

    return body
