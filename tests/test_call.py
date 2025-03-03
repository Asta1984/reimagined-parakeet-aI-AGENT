import os
from twilio.rest import Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Twilio credentials
account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
auth_token = os.environ.get("TWILIO_AUTH_TOKEN")
twilio_number = os.environ.get("TWILIO_PHONE_NUMBER")

# Your ngrok URL
webhook_url = "https://c53b-2409-4081-8783-3752-8172-1894-882e-a85a.ngrok-free.app/api/v1/twilio-webhook"

# Initialize Twilio client
client = Client(account_sid, auth_token)

# Create a test call
call = client.calls.create(
    url=webhook_url,  # This is simpler than using TwiML directly
    from_=twilio_number,
    to="+917067456439",  # Your verified phone number
    method="POST"
)

print(f"Call initiated with SID: {call.sid}")
print(f"Check call status at: https://www.twilio.com/console/voice/calls/logs/{call.sid}")