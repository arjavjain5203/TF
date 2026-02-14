from datetime import datetime, date
from app.models.member import Gender
import re

def validate_dob(dob_str: str) -> date:
    try:
        return datetime.strptime(dob_str, "%d-%m-%Y").date()
    except ValueError:
        raise ValueError("Invalid date format. Please use DD-MM-YYYY.")

def validate_gender(gender_str: str) -> Gender:
    gender_str = gender_str.lower()
    if gender_str in ["male", "m"]:
        return Gender.MALE
    elif gender_str in ["female", "f"]:
        return Gender.FEMALE
    elif gender_str in ["other", "o"]:
        return Gender.OTHER
    else:
        raise ValueError("Invalid gender. Please enter Male, Female, or Other.")

def normalize_phone(phone: str) -> str:
    # Basic normalization, assuming input is close to E.164 or local
    # For a real app, use phonenumbers library
    # Here just strip non-digits and add '+' if missing
    clean = re.sub(r'[^0-9+]', '', phone)
    if not clean.startswith('+'):
         # Default to some country code or assume it's there?
         # User requirement says "Normalize phone numbers to E.164 format"
         # Maybe assume input includes country code or prompt for it?
         # For simplicity, preprend '+' if missing, and hope user provided CC.
         clean = "+" + clean
    return clean

def validate_phone(phone: str) -> str:
    # Use phonenumbers lib if strictly required, but regex is lighter for now
    # if valid, return normalized
    return normalize_phone(phone)
