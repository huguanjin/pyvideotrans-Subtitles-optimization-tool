# config.py

import toml
import logging
import os

logger = logging.getLogger(__name__)

# Load configuration from TOML file
config_file_path = 'config.toml'
if not os.path.exists(config_file_path):
    logger.error(f"Configuration file '{config_file_path}' not found. Falling back to environment variables.")
    DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY')  # Fallback to environment variable
    DEEPSEEK_API_URL = os.getenv('DEEPSEEK_API_URL', 'https://api.deepseek.com/v1')  # Default value with protocol
    if not DEEPSEEK_API_KEY:
        logger.error("DEEPSEEK_API_KEY is not set in the configuration file or environment variables.")
        raise ValueError("DEEPSEEK_API_KEY is not set. Please check the configuration file or environment variables.")
else:
    config = toml.load(config_file_path)
    DEEPSEEK_API_KEY = config.get('deepseek', {}).get('api_key', '') 
    DEEPSEEK_API_URL = config.get('deepseek', {}).get('api_url', '')

if not DEEPSEEK_API_KEY:
    logger.error("DEEPSEEK_API_KEY is not set in the configuration file.")
    raise ValueError("DEEPSEEK_API_KEY is not set. Please check the configuration file.")