from datetime import datetime
import os
from flask import Flask, request, jsonify, render_template  # type: ignore
from flask_cors import CORS  # type: ignore
from flask_mail import Mail, Message  # type: ignore
from config import Config
from models import db, Booking
from utils import validate_booking_data
import logging

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Enable CORS, DB, and Mail
CORS(app)
db.init_app(app)
mail = Mail(app)

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Ensure DB tables are created once
with app.app_context():
    db.create_all()


# ------------------- ROUTES -------------------

# ✅ Home
@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")


# ✅ Login
@app.route("/login", methods=["GET"])
def login():
    return render_template("login.html")


# ✅ Sacred Map
@app.route("/sacred-map", methods=["GET"])
def sacred_map():
    return render_template("sacred-map.html")


# ✅ Registration
@app.route("/registration", methods=["GET"])
def registration():
    return render_template("shaktipeeth-registration.html")


# ✅ Tour completion
@app.route("/book-tour-complete", methods=["GET"])
def book_tour_complete():
    return render_template("book-tour-complete.html")


# ✅ About page
@app.route("/about", methods=["GET"])
def about_page():
    return render_template("about-page.html")


# ✅ API: Book a tour
@app.route("/api/book", methods=["POST"])
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

        # Send confirmation email (if configured)
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


# ✅ Send confirmation email
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


# ✅ API: Get single booking
@app.route("/api/bookings/<int:booking_id>", methods=["GET"])
def get_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    return jsonify(booking.to_dict())


# ✅ API: Get all bookings
@app.route("/api/bookings", methods=["GET"])
def get_bookings():
    bookings = Booking.query.order_by(Booking.booking_date.desc()).all()
    return jsonify([booking.to_dict() for booking in bookings])

print(app.url_map)


# ------------------- MAIN -------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8001)))


""" if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=8001,     # ✅ Force port 8001
        debug=True     # ✅ Enable debug mode
    )
 """