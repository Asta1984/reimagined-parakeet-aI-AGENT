import os
from dotenv import load_dotenv

load_dotenv()

required_vars = [
    "TWILIO_ACCOUNT_SID",
    "TWILIO_AUTH_TOKEN",
    "DEEPGRAM_API_KEY",
    "ELEVENLABS_API_KEY",
    "MISTRAL_API_KEY"
]

missing = [var for var in required_vars if not os.getenv(var)]
if missing:
    print(f"Critical missing environment variables: {missing}")
    exit(1)
print("Environment validation passed!")