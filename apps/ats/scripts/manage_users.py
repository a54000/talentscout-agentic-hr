"""Small admin helper for ATS login accounts (works on SQLite or PostgreSQL via the app's DB layer).

Usage (inside the ats container, from the repo root):
  docker compose run --rm ats python scripts/manage_users.py list
  docker compose run --rm ats python scripts/manage_users.py set-password <username>

The new password is read with a hidden prompt; it is never printed or logged.
"""

import getpass
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("SECRET_KEY", "manage-users-only")

import app  # noqa: E402


def list_users() -> None:
    conn = app.get_db()
    try:
        rows = conn.execute(
            "SELECT id, username, email, is_admin, is_active FROM app_users ORDER BY id"
        ).fetchall()
    finally:
        conn.close()
    print(f"{'id':>4}  {'username':<24} {'email':<32} admin active")
    for r in rows:
        print(f"{r['id']:>4}  {str(r['username']):<24} {str(r['email'] or ''):<32} {r['is_admin'] or 0:>5} {r['is_active'] if r['is_active'] is not None else 1:>6}")


def set_password(username: str) -> None:
    pw1 = getpass.getpass(f"New password for {username}: ")
    pw2 = getpass.getpass("Repeat: ")
    if pw1 != pw2:
        raise SystemExit("Passwords do not match.")
    if len(pw1) < 10:
        raise SystemExit("Use at least 10 characters.")
    conn = app.get_db()
    try:
        cur = conn.execute(
            "UPDATE app_users SET password=? WHERE lower(trim(username))=lower(trim(?))",
            (app.hash_password(pw1), username),
        )
        conn.commit()
        if getattr(cur, "rowcount", 1) == 0:
            raise SystemExit(f"No account with username {username!r}. Run 'list' to see accounts.")
    finally:
        conn.close()
    print(f"Password updated for {username}.")


if __name__ == "__main__":
    if len(sys.argv) >= 2 and sys.argv[1] == "list":
        list_users()
    elif len(sys.argv) == 3 and sys.argv[1] == "set-password":
        set_password(sys.argv[2])
    else:
        print(__doc__)
        raise SystemExit(2)
