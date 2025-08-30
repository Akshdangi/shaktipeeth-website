from datetime import datetime
from flask import Flask, request, jsonify # type: ignore
from flask_cors import CORS # type: ignore
from flask_mail import Mail, Message # type: ignore
from config import Config
from models import db, Booking
from utils import validate_booking_data
import logging

app = Flask(app.py) # type: ignore
app.config.from_object(Config)
CORS(app)
db.init_app(app)
mail = Mail(app)

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/api/book', methods=['POST'])
def book_tour():
    try:
        data = request.json
        
        # Validate the booking data
        errors = validate_booking_data(data)
        if errors:
            return jsonify({'success': False, 'errors': errors}), 400
        
        # Create new booking
        booking = Booking(
            package=data['package'],
            travel_date=datetime.strptime(data['travel_date'], '%Y-%m-%d').date(),
            num_travelers=int(data['num_travelers']),
            accommodation=data['accommodation'],
            special_requirements=data.get('special_requirements', ''),
            contact_person=data['name'],
            mobile=data['mobile'],
            email=data['email']
        )
        
        db.session.add(booking)
        db.session.commit()
        
        # Send confirmation email
        try:
            send_confirmation_email(booking)
        except Exception as e:
            logger.error(f"Failed to send confirmation email: {str(e)}")
        
        return jsonify({
            'success': True,
            'message': 'Booking successful',
            'booking_id': booking.id
        }), 201
        
    except Exception as e:
        logger.error(f"Booking error: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'An error occurred while processing your booking'
        }), 500

def send_confirmation_email(booking):
    subject = f"Shaktipeeth Tour Booking Confirmation - {booking.id}"
    
    body = f"""
    Dear {booking.contact_person},

    Thank you for booking your Shaktipeeth tour with us. Here are your booking details:

    Booking ID: {booking.id}
    Package: {booking.package.title()} Circuit
    Travel Date: {booking.travel_date.strftime('%d %B, %Y')}
    Number of Travelers: {booking.num_travelers}
    Accommodation: {booking.accommodation.title()}

    We will contact you shortly with additional details about your tour.

    If you have any questions, please don't hesitate to contact us.

    Best regards,
    Shaktipeeth Tourism Team
    """
    
    msg = Message(
        subject=subject,
        recipients=[booking.email],
        body=body
    )
    
    mail.send(msg)

@app.route('/api/bookings/<int:booking_id>', methods=['GET'])
def get_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    return jsonify(booking.to_dict())

@app.route('/api/bookings', methods=['GET'])
def get_bookings():
    bookings = Booking.query.order_by(Booking.booking_date.desc()).all()
    return jsonify([booking.to_dict() for booking in bookings])

if __name__ == '__main__':
    app.run(debug=True)
