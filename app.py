from flask import Flask, request, jsonify
from flask_cors import CORS
import pyrebase
import random
import os
import string
from mail import send_email
app = Flask(__name__)
CORS(app) 
LOG_FILE = 'generated_ids.log'

def generate_unique_id():
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'w') as file:
            pass

    while True:
        unique_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=7))
        with open(LOG_FILE, 'r') as file:
            if unique_id not in file.read().splitlines():
                with open(LOG_FILE, 'a') as file:
                    file.write(unique_id + '\n')
                return unique_id

 # This will enable CORS for all routes

firebase_config = {
    "apiKey": "AIzaSyBq5B9n-idJ2laC1MSjD2Q5PRWpHFCWwCQ",
    "authDomain": "idluae.firebaseapp.com",
    "projectId": "idluae",
    "storageBucket": "idluae.appspot.com",
    "messagingSenderId": "598089755444",
    "databaseURL": "https://idluae-default-rtdb.firebaseio.com",
    "appId": "1:598089755444:web:ef9aafa02d19f7e3cc9361"
}
firebase = pyrebase.initialize_app(firebase_config)
db = firebase.database()

@app.route('/ticket', methods=['POST'])
def create_ticket():
    data = request.json
    new_id = generate_unique_id()
    data['userId'] = new_id
    data['attendeeType'] = 'participant'
    data['present'] = False
    attendee_name = data['fullname']
    attendee_email = data['email']
    user_id = data['userId']
    ticket_type = data['attendeeType']
    qr_code_url = "https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=" + user_id
    subject = "Your Virtual Event Ticket"
    text_content = f"Hi {attendee_name},\n\nThank you for registering for the event. Here is your ticket information:\n\nUser ID: {user_id}\nTicket Type: {ticket_type}\n\nPlease keep this information safe as it will be used to verify your attendance.\n\nBest regards,\nEvent Team"
    db.child("partipants").child(new_id).set(data)
    print(data)
    status_code, response = send_email(attendee_email, subject, text_content,
        attendee_name, attendee_email, user_id, ticket_type,qr_code_url
    )
    print(f"Status Code: {status_code}")
    print(f"Response: {response}")
    return jsonify({'status':True,'message': 'Ticket created', 'data': data,'id':new_id})

def get_all_ticket_ids():
    if not os.path.exists(LOG_FILE):
        return []

    with open(LOG_FILE, 'r') as file:
        ticket_ids = file.read().splitlines()
    return ticket_ids

@app.route('/api/ticket', methods=['GET'])
def get_ticket():
    ticket_id = request.args.get('id')
    tickets = get_all_ticket_ids()
    if ticket_id in tickets:
        ticket_data = db.child("partipants").child(ticket_id).get().val()
        return jsonify(ticket_data)
    else:
        return jsonify({"error": "Ticket not found"}), 404

if __name__ == '__main__':
    app.run()