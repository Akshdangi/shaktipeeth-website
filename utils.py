from validate_email import validate_email # type: ignore
import phonenumbers # type: ignore
from datetime import datetime

def validate_booking_data(data):
    errors = []
    
    # Validate package
    valid_packages = ['eastern', 'northern', 'complete', 'weekend']
    if data.get('package') not in valid_packages:
        errors.append('Invalid package selected')
    
    # Validate travel date
    try:
        travel_date = datetime.strptime(data.get('travel_date'), '%Y-%m-%d').date()
        if travel_date < datetime.now().date():
            errors.append('Travel date cannot be in the past')
    except:
        errors.append('Invalid travel date format')
    
    # Validate number of travelers
    try:
        num_travelers = int(data.get('num_travelers'))
        if not 1 <= num_travelers <= 20:
            errors.append('Number of travelers must be between 1 and 20')
    except:
        errors.append('Invalid number of travelers')
    
    # Validate accommodation
    valid_accommodation = ['budget', 'standard', 'premium']
    if data.get('accommodation') not in valid_accommodation:
        errors.append('Invalid accommodation type')
    
    # Validate email
    if not validate_email(data.get('email', '')):
        errors.append('Invalid email address')
    
    # Validate phone number
    try:
        phone_number = phonenumbers.parse(data.get('mobile'), 'IN')
        if not phonenumbers.is_valid_number(phone_number):
            errors.append('Invalid phone number')
    except:
        errors.append('Invalid phone number format')
    
    return errors
