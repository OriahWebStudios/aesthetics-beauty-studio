from flask import Flask, render_template, request, redirect, url_for, flash, Blueprint, session, jsonify, current_app
from app.models import db, BookingTable, ServiceTable
from app.forms import BookingForm
from app.utils import send_email
from flask_mail import Message
import os
from datetime import datetime
import hashlib
import uuid
import urllib
from urllib.parse import urlencode



main = Blueprint('main', __name__)

@main.route('/')
def index():
    form = BookingForm()
    booking = BookingTable()
    service = ServiceTable()

    return render_template('main.html', form=form, booking=booking, service=service)

def generateSignature(dataArray, passPhrase = ''):
    payload = ""
    for key in dataArray:
        value = str(dataArray[key])
        payload += key + "=" + urllib.parse.quote_plus(value.replace("+", " ")) + "&"
    payload = payload[:-1]
    if passPhrase != '':
        payload += f"&passphrase={passPhrase}"
    return hashlib.md5(payload.encode()).hexdigest()


@main.route('/booking', methods=['GET', 'POST'])
def booking():
    form = BookingForm()
    service = ServiceTable.query.all()
    booking_id = str(uuid.uuid4())



    if form.validate_on_submit():
        selected_service_id = form.selected_service.data
        selected_service = ServiceTable.query.get(selected_service_id)

        selected_details = f'{selected_service.name} - R{selected_service.price:.2f}'
        selected_price = selected_service.price

        session['booking_data'] = {
            'booking_id': booking_id,
            'full_name': form.full_name.data,
            'email': form.email.data,
            'cell_number': form.cell_number.data,
            'selected_service': selected_details,
            'date': form.date.data,
            'time': form.time.data,
            'selected_price': selected_price,
            'created_at': datetime.now()
        }
        return redirect(url_for('main.booking_confirmation'))
    return render_template('main.html', form=form, service=service)


@main.route('/booking_confirmation', methods=['GET', 'POST'])
def booking_confirmation():
    booking_data = session.get('booking_data')
    if request.method == 'POST':
        if 'pay_later' in request.form:
            booking_id = booking_data['booking_id']
            full_name = booking_data['full_name']
            email = booking_data['email']
            cell_number = booking_data['cell_number']
            selected_service = booking_data['selected_service']
            date = booking_data['date']
            time = booking_data['time']
            created_at = booking_data['created_at']
            booking = BookingTable(booking_id=booking_id, full_name=full_name, email=email, cell_number=cell_number, selected_service=selected_service, date=date, time=time, created_at=created_at)
            db.session.add(booking)
            db.session.commit()
            session.pop('booking_data', None)
            flash('Your booking has been successfully confirmed. We are excited to have you with us, we will get back to you shortly.', 'success_booking')
            return redirect(url_for('main.index'))
        
        elif 'pay_now' in request.form:
            booking_id = booking_data['booking_id']
            full_name = booking_data['full_name']
            email = booking_data['email']
            cell_number = booking_data['cell_number']
            selected_service = booking_data['selected_service']
            date = booking_data['date']
            time = booking_data['time']
            created_at = booking_data['created_at']
            booking = BookingTable(
                booking_id=booking_id, full_name=full_name, email=email, 
                cell_number=cell_number, selected_service=selected_service, 
                date=date, time=time, created_at=created_at
            )
            db.session.add(booking)
            db.session.commit()

            payfast_data = {
                'merchant_id': current_app.config['PAYFAST_MERCHANT_ID'],
                'merchant_key': current_app.config['PAYFAST_MERCHANT_KEY'],
                'return_url': 'https://0846-105-214-105-37.ngrok-free.app/payment_return',
                'cancel_url': 'https://0846-105-214-105-37.ngrok-free.app/payment_cancel',
                'notify_url': 'https://0846-105-214-105-37.ngrok-free.app/payment_notify',
                'name_first': booking_data['full_name'],
                'email_address': booking_data['email'],
                'm_payment_id': booking_data['booking_id'],
                'amount': booking_data['selected_price'],
                'item_name': f"Appointment for {booking_data['selected_service']}",
            }

            passphase = 'moleferamotsepane'
            signature = generateSignature(payfast_data, passphase)
            payfast_data['signature'] = signature
            print(signature, payfast_data)

            payfast_url = 'https://sandbox.payfast.co.za/eng/process?' + urllib.parse.urlencode(payfast_data)
            return redirect(payfast_url)

        elif 'cancel' in request.form:
            session.pop('booking_data', None)
            flash('Your booking has been successfully cancelled.', 'error_booking')
            return redirect(url_for('main.index'))
    return render_template('confirm.html', booking_data=booking_data)

@main.route('/payment_return', methods=['GET', 'POST'])
def payment_return():
    form = BookingForm()

    # Verify signature on return url
    payfast_data = request.args.to_dict()
    passphase = 'moleferamotsepane'
    signature = generateSignature(payfast_data, passphase)
    payfast_data['signature'] = signature
    print(signature, payfast_data)

    if signature != payfast_data['signature']:
        return render_template('/error_handling/400.html'), 400
    
    # Pop the booking data from the session
    booking_data = session.get('booking_data')
    if not booking_data:
        return render_template('/error_handling/400.html'), 400    
    session.pop('booking_data', None)
    
    return render_template('main.html', form=form, booking_data=booking_data)


@main.route('/payment_cancel')
def payment_cancel():
    form = BookingForm()
    booking_id = request.args.get('m_payment_id')

    flash('Your booking and payment have were unsuccessful. Please try again.', 'payment_cancel')
    return render_template('main.html', booking_id=booking_id, form=form)

@main.route('/payment_notify', methods=['POST'])
def payment_notify():
    notify_data = session.get('booking_data')
    print("Notify Data Received:", notify_data)
    
    if request.content_type != 'application/x-www-form-urlencoded':
        current_app.logger.error("Invalid Content-Type received")
        return render_template('/error_handling/400.html'), 400

    data = request.form.to_dict()
    current_app.logger.info(f"ITN Data Received: {data}")
    passphase = 'moleferamotsepane'
    signature = generateSignature(data, passphase)
    data['signature'] = signature
    print(signature, data)

    if signature != data['signature']:
        return render_template('/error_handling/400.html'), 400
    
    booking_id = data['m_payment_id']
    booking = BookingTable.query.filter_by(booking_id=booking_id).first()
    if booking:
        booking.payment_status = data['payment_status']
        db.session.commit()
    

    return "Payment notification processed", 200

# Error handling
@main.app_errorhandler(400)
def bad_request(error):
    current_app.logger.error(f"Bad Request: {error}")
    return render_template('/error_handling/400.html'), 400

@main.app_errorhandler(404)
def not_found(error):
    current_app.logger.error(f"Page Not Found: {error}")
    return render_template('/error_handling/404.html'), 404

@main.app_errorhandler(405)
def method_not_allowed(error):
    current_app.logger.error(f"Method Not Allowed: {error}")
    return render_template('/error_handling/405.html'), 405

@main.app_errorhandler(500)
def internal_server_error(error):
    current_app.logger.error(f"Internal Server Error: {error}")
    return render_template('/error_handling/500.html'), 500




    


