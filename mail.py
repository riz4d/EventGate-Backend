import os
from mailjet_rest import Client
import base64
from jinja2 import Template
from config import api_key,api_secret,event_date,event_location,event_time,sender,sendername

mailjet = Client(auth=(api_key, api_secret), version='v3.1')

def send_email(recipient, subject, text_content, attendee_name, attendee_email, user_id, ticket_type, qr_code_url, attachment_path=None):
    
    html_template = """
    <!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Virtual Ticket</title>
  <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
</head>
<body class="min-h-screen bg-gradient-to-b from-blue-200 to-gray-100 p-4 sm:p-6 flex items-center justify-center">
  <div class="w-full max-w-3xl shadow-lg bg-white rounded-lg">
    <div class="text-center space-y-2 p-6">
      <div class="bg-gray-200 text-gray-700 py-1 px-4 rounded-full inline-block">Registration Successful!</div>
      <h1 class="text-3xl font-bold text-blue-600">TechCon 2024</h1>
      <div class="border border-blue-600 text-blue-600 py-1 px-4 rounded-full inline-block">Virtual Ticket</div>
    </div>
    <div class="p-6">
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <!-- Attendee Information -->
        <div class="space-y-4">
          <h2 class="text-sendername2xl font-semibold text-gray-700">Attendee Information</h2>
          <div class="space-y-2">
            <div class="flex items-center space-x-2">
              <svg class="w-5 h-5 text-blue-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5.121 17.804A4.983 4.983 0 006 16c0-2.761-2.239-5-5-5s-5 2.239-5 5c0 1.08.314 2.084.851 2.929C-.952 19.851-2 22.357-2 25h24c0-2.643-1.048-5.149-3.121-6.804zM17 11c0 3.866-3.134 7-7 7s-7-3.134-7-7 3.134-7 7-7 7 3.134 7 7zM22 21h-5v-1c0-1.105.895-2 2-2s2 .895 2 2v1zM22 21v-1c0-1.105-.895-2-2-2h-5v1h5z" />
              </svg>
              <span class="font-medium">{{ attendee_name }}</span>
            </div>
            <div class="flex items-center space-x-2">
              <svg class="w-5 h-5 text-blue-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 12H8M16 12a4 4 0 01-8 0 4 4 0 018 0zm0 0H8M8 12a4 4 0 011-7.874A7.962 7.962 0 0116 8m0 4v6a2 2 0 002 2h4a2 2 0 002-2v-6m-4 0a4 4 0 00-8 0" />
              </svg>
              <span class="break-all">{{ attendee_email }}</span>
            </div>
            <div class="flex items-center space-x-2">
              <svg class="w-5 h-5 text-blue-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19V6a2 2 0 012-2h2a2 2 0 012 2v13m-6 0h6" />
              </svg>
              <span>User ID: {{ user_id }}</span>
            </div>
            <div class="flex items-center space-x-2">
              <svg class="w-5 h-5 text-blue-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c0-1.105-.895-2-2-2s-2 .895-2 2m0 0c1.105 0 2 .895 2 2m-2 0c1.105 0 2 .895 2 2m-4-2v4a4 4 0 004 4h0a4 4 0 004-4v-4m0 0c1.105 0 2-.895 2-2m0-2c0-1.105-.895-2-2-2s-2 .895-2 2m0 0c-1.105 0-2 .895-2 2" />
              </svg>
              <span>Type: {{ ticket_type }}</span>
            </div>
          </div>
          <!-- Event Details -->
          <h2 class="text-2xl font-semibold text-gray-700 mt-6">Event Details</h2>
          <div class="space-y-2">
            <div class="flex items-center space-x-2">
              <svg class="w-5 h-5 text-blue-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3M3 8h18M4 21h16a2 2 0 002-2V10H2v9a2 2 0 002 2z" />
              </svg>
              <span>{{ event_date }}</span>
            </div>
            <div class="flex items-center space-x-2">
              <svg class="w-5 h-5 text-blue-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-11a9 9 0 11-9 9" />
              </svg>
              <span>{{ event_time }}</span>
            </div>
            <div class="flex items-center space-x-2">
              <svg class="w-5 h-5 text-blue-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 10l-7 7-7-7" />
              </svg>
              <span>{{ event_location }}</span>
            </div>
          </div>
        </div>
        <!-- QR Code -->
        <div class="flex flex-col items-center justify-center space-y-4">
          <h2 class="text-2xl font-semibold text-gray-700 text-center">Your Virtual Ticket QR Code</h2>
          <img src="{{ qr_code_url }}" alt="QR Code" class="w-48 h-48">
          <p class="text-sm text-gray-500 text-center">Scan this QR code to join the virtual event</p>
        </div>
      </div>
    </div>
  </div>
</body>
</html>
    """

    template = Template(html_template)
    html_content = template.render(
        attendee_name=attendee_name,
        attendee_email=attendee_email,
        user_id=user_id,
        ticket_type=ticket_type,
        event_date=event_date,
        event_time=event_time,
        event_location=event_location,
        qr_code_url=qr_code_url
    )

    data = {
        'Messages': [
            {
                "From": {
                    "Email": sender,
                    "Name": sendername
                },
                "To": [
                    {
                        "Email": recipient,
                        "Name": attendee_name
                    }
                ],
                "Subject": subject,
                "TextPart": text_content,
                "HTMLPart": html_content,
                "Attachments": []
            }
        ]
    }

    if attachment_path:
        with open(attachment_path, "rb") as f:
            attachment_content = base64.b64encode(f.read()).decode()
            attachment = {
                "ContentType": "application/pdf",
                "Filename": os.path.basename(attachment_path),
                "Base64Content": attachment_content
            }
            data['Messages'][0]['Attachments'].append(attachment)

    result = mailjet.send.create(data=data)
    return result.status_code, result.json()

