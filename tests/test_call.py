import os
from twilio.rest import Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Twilio credentials
account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
auth_token = os.environ.get("TWILIO_AUTH_TOKEN")
twilio_number = os.environ.get("TWILIO_PHONE_NUMBER")

# Your ngrok URL (ensure this matches your current ngrok forwarding)
webhook_url = "https://9511-14-139-241-69.ngrok-free.app/api/v1/calls/inbound-call"

def initiate_call(to_number):
    """
    Initiate a call to the specified number
    
    Args:
        to_number (str): Phone number to call (with country code)
    """
    try:
        # Initialize Twilio client
        client = Client(account_sid, auth_token)

        # Create a test call
        call = client.calls.create(
            url=webhook_url,  # This URL returns the TwiML instructions for the call
            from_=twilio_number,
            to=to_number,
            method="POST"
        )

        print(f"Call initiated with SID: {call.sid}")
        print(f"Check call status at: https://www.twilio.com/console/voice/calls/logs/{call.sid}")
    
    except Exception as e:
        print(f"Error initiating call: {e}")

# Example usage
if __name__ == "__main__":
    # Replace with the phone number you want to call
    test_number = "+917067456439"  # Your verified phone number
    initiate_call(test_number)