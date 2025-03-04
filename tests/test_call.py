import os
from twilio.rest import Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Twilio credentials
account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
auth_token = os.environ.get("TWILIO_AUTH_TOKEN")
twilio_number = os.environ.get("TWILIO_PHONE_NUMBER")

# Your ngrok URL (pointing to your server's endpoint)
webhook_url = "https://9511-14-139-241-69.ngrok-free.app/api/v1/twilio-webhook"

# Initialize Twilio client
client = Client(account_sid, auth_token)

# Create a test call
call = client.calls.create(
    url=webhook_url,  # This URL returns the TwiML instructions for the call
    from_=twilio_number,
    to="+917067456439",  # Your verified Indian phone number
    method="POST"
)

print(f"Call initiated with SID: {call.sid}")
print(f"Check call status at: https://www.twilio.com/console/voice/calls/logs/{call.sid}")
