# app/utils/logger.py
import logging
from app.config.settings import settings

def setup_logging():
    """Configure logging for the application"""
    logging.basicConfig(
        level=getattr(logging, settings.LOG_LEVEL.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('sales_voice_agent.log')
        ]
    )