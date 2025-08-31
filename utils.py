from validate_email_address import validate_email
import re
from datetime import datetime

def validate_booking_data(data):
    errors = []

    # Validate name
    if not data.get("name") or len(data["name"].strip()) < 2:
        errors.append("Name must be at least 2 characters long.")

    # Validate email
    if not data.get("email") or not validate_email(data["email"]):
        errors.append("Invalid email address.")

    # Validate mobile number (basic check for 10 digits in India)
    if not data.get("mobile") or not re.match(r"^[6-9]\d{9}$", data["mobile"]):
        errors.append("Invalid mobile number.")

    # Validate number of travelers
    if not data.get("num_travelers") or int(data["num_travelers"]) < 1:
        errors.append("Number of travelers must be at least 1.")

    # Validate travel date
    try:
        travel_date = datetime.strptime(data.get("travel_date", ""), "%Y-%m-%d").date()
        if travel_date < datetime.today().date():
            errors.append("Travel date cannot be in the past.")
    except ValueError:
        errors.append("Invalid travel date format. Use YYYY-MM-DD.")

    # Validate package
    if not data.get("package"):
        errors.append("Package selection is required.")

    # Validate accommodation
    if not data.get("accommodation"):
        errors.append("Accommodation type is required.")

    return errors
