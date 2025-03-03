import logging
import json
from datetime import datetime

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

class ConversationLogger:
    @staticmethod
    def log_interaction(phone: str, input: str, output: str):
        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "phone": phone,
            "input": input,
            "output": output
        }
        logging.info(json.dumps(entry))