# file: utils/validators.py
import re

def is_valid_email(email: str) -> bool:
    """Check if the email format is valid."""
    # A standard regex for email validation
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(pattern, email) is not None

def is_valid_phone(phone: str) -> bool:
    """Check if the phone number format is valid."""
    # A simple regex for international phone numbers (e.g., +919876543210 or 9876543210)
    # Allows an optional '+' at the start and requires 10-15 digits
    pattern = r"^\+?[0-9]{10,15}$"
    return re.match(pattern, phone) is not None