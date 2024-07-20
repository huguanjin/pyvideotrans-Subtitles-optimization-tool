# api_client.py

from openai import OpenAI
from config import DEEPSEEK_API_KEY, DEEPSEEK_API_URL
import logging

logger = logging.getLogger(__name__)

class APIClient:
    def __init__(self):
        if not DEEPSEEK_API_KEY:
            logger.error("DEEPSEEK_API_KEY is not set. Please check the configuration file.")
            raise ValueError("DEEPSEEK_API_KEY is not set. Please check the configuration file.")
        self.client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url=DEEPSEEK_API_URL)
        logger.info(f"OpenAI client initialized with API key and base URL: {DEEPSEEK_API_URL}")

    def create_chat_completion(self, model, messages):
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                stream=False
            )
            logger.info("Chat completion created successfully.")
            return response
        except Exception as e:
            logger.error(f"Error creating chat completion: {e}", exc_info=True)
            raise Exception(f"Error creating chat completion: {e}")