# auth_helpers.py
import bcrypt
import re
from typing import Optional
from src.customer import Customer


from typing import List


# Simple, practical email regex (good for most use-cases; avoids exotic addresses)
EMAIL_RE = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")

def sanitize_string(s: str) -> str:
    """Trim whitespace and collapse multiple internal spaces."""
    if s is None:
        return ""
    return " ".join(s.strip().split())

def is_valid_email(email: str) -> bool:
    if not email:
        return False
    email = email.strip()
    return bool(EMAIL_RE.match(email))

def is_strong_password(pw: str, min_len: int = 8) -> (bool, str):
    """Return (ok, message). Check length, mixed case, number, and symbol."""
    if not pw:
        return False, "Password cannot be empty."
    if len(pw) < min_len:
        return False, f"Password must be at least {min_len} characters."
    if pw.lower() == pw or pw.upper() == pw:
        return False, "Password should include both upper and lower case letters."
    if not re.search(r"\d", pw):
        return False, "Password must include at least one digit."
    if not re.search(r"[^\w\s]", pw):
        return False, "Password must include at least one special character (e.g. !@#$%)."
    return True, "OK"

def name_ok(name: str, max_len: int = 100) -> bool:
    n = sanitize_string(name)
    return len(n) > 0 and len(n) <= max_len

def email_unique(email: str, customers: List[Customer]) -> bool:
    email = email.strip().lower()
    return all(c.email.strip().lower() != email for c in customers)

BCRYPT_ROUNDS = 12  # adjust for your server CPU; 12 is a reasonable default

def hash_password(plain: str) -> str:
    """Return bcrypt hash (utf-8 string) for a plaintext password."""
    if isinstance(plain, str):
        plain = plain.encode('utf-8')
    hashed = bcrypt.hashpw(plain, bcrypt.gensalt(rounds=BCRYPT_ROUNDS))
    # store as utf-8 decoded string so CSV/JSON handling is simple
    return hashed.decode('utf-8')

def verify_password(plain: str, stored_hash: str) -> bool:
    """Verify a plaintext password against stored hash (or plaintext for backward compatibility)."""
    if not stored_hash:
        return False
    # If stored_hash appears to be a bcrypt hash, use bcrypt.checkpw.
    # Bcrypt hashes begin with $2b$ or $2a$ or $2y$ etc.
    if stored_hash.startswith("$2"):
        try:
            return bcrypt.checkpw(plain.encode('utf-8'), stored_hash.encode('utf-8'))
        except ValueError:
            return False
    # Backwards-compat: stored password was plaintext (legacy). Compare and allow re-hash after success.
    return plain == stored_hash

def ensure_hashed_password(user: Customer, save_callback) -> None:
    """
    If the user's password looks like plaintext, replace it with a bcrypt hash and persist via save_callback(user).
    save_callback must save the user (e.g., save_customer_to_csv).
    """
    if not user.password:
        return
    if not user.password.startswith("$2"):
        # re-hash and save
        user.password = hash_password(user.password)
        save_callback(user)
