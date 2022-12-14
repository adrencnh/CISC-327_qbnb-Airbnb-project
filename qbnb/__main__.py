import json
from flask import Flask
from flask import request, jsonify
from flask_mongoengine import MongoEngine
from qbnb import app
from qbnb.cli import user_home_page
from qbnb.models import user_register
from mongoengine import ValidationError
from qbnb import app
from qbnb.models import Listing
from qbnb.cli import listing_update_page, update_listing
from qbnb.cli import login_page, register_page
from qbnb.cli import update_user_page, user_home_page


# Route to retrieve all listings
@app.route("/listings")
def get_listings():
    listings = Listing.objects()
    return jsonify(listings), 200


# Route to create a new listing
@app.route("/listings/", methods=["POST"])
def create_listing():
    body = request.get_json()
    listing = Listing(**body)
    try:
        listing.check()
        listing.save()
        return jsonify(listing), 200
    except ValidationError as e:
        print(e.message)
        return jsonify(listing), 500


# Route to request a booking for a listing 
@app.route("/listings/<id>/request_booking", methods=["POST"])
def request_booking(id):
    body = request.get_json()
    # Creates a booking object
    booking = Booking(**body).save()
    # Gets listings by id and updates the bookings with a reference
    listing = Listing.objects.get_or_404(id=id)
    listing.requested_bookings.append(booking)
    listing.save()
    return jsonify(listing), 200


# Route to confirm a requested booking for a listing
@app.route(
    "/listings/<listing_id>/confirm_booking/<booking_id>",

    methods=["GET"])
def confirm_booking(listing_id, booking_id):
    listing = Listing.objects.get_or_404(id=listing_id)
    booking = Booking.objects.get_or_404(id=booking_id)
    booking.confirmed = True
    booking.save()
    # Remove confirmed booking from requested_bookings
    listing.requested_bookings.remove(booking)
    listing.current_booking = booking
    listing.save()
    return jsonify(listing), 200


if __name__ == "__main__":
    while True:
        selection = input(
            'Welcome to qbnb!\n 1. Log in\n 2. Register\n 3. Exit\n: '
        )
        selection = selection.strip()
        if selection == '1':
            user = login_page()
            if user is not False:
                print(f'Welcome {user.user_name}!')
                user_home_page(user)
                break
            else:
                print('Login failed!')
        elif selection == '2':
            register_page()
        elif selection == '3':
            break
    # app.run(debug=True)
