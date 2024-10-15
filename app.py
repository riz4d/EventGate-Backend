from flask import Flask, request, jsonify
import os
import uuid
from gen_uuid import generate_unique_id
import pyrebase
from flask_cors import CORS
from mail import send_email
from config import firebase_config

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # Allow all origins for demonstration purposes

# In-memory storage for generated IDs
generated_ids = set()

firebase = pyrebase.initialize_app(firebase_config)
db = firebase.database()

@app.route('/api/ticket', methods=['POST'])
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
        attendee_name, attendee_email, user_id, ticket_type, qr_code_url
    )
    print(f"Status Code: {status_code}")
    print(f"Response: {response}")
    return jsonify({'status': True, 'message': 'Ticket created', 'data': data, 'id': new_id})

def get_all_ticket_ids():
    return list(generated_ids)

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
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)