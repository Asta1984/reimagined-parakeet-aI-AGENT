from vocode.streaming.models.telephony import TwilioCall, TwilioConfig
from app.config.settings import settings

class TelephonyService:
    @staticmethod
    def initialize_twilio():
        return TwilioConfig(
            account_sid=settings.TWILIO_ACCOUNT_SID,
            auth_token=settings.TWILIO_AUTH_TOKEN,
            phone_number=settings.TWILIO_PHONE_NUMBER
        )

    @staticmethod
    def handle_incoming_call(request):
        """Process incoming Twilio call request"""
        try:
            return TwilioCall.from_request(request)
        except Exception as e:
            raise ValueError(f"Error processing call: {str(e)}")