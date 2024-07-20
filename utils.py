import logging
from logging.handlers import RotatingFileHandler
from tkinter import filedialog, messagebox
import toml
import os

# Setup logging
logger = logging.getLogger(__name__)

def setup_logging():
    logger.setLevel(logging.INFO)

    # Create a file handler that logs even debug messages
    file_handler = RotatingFileHandler('app.log', maxBytes=100000, backupCount=10)
    file_handler.setLevel(logging.INFO)

    # Create a console handler with a higher log level
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # Create a formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Add the handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

setup_logging()

# Utility function for file upload handling to reduce redundancy
def upload_files(file_paths):
    logger.info("Starting file upload process")
    if not file_paths:
        logger.error("No files provided for upload")
        raise ValueError("No files provided for upload")

    try:
        # Simulate file upload logic
        for file_path in file_paths:
            logger.info(f"Uploading file: {file_path}")
            # Actual upload logic would go here
        logger.info("File upload process completed successfully")
    except Exception as e:
        logger.error(f"Error during file upload: {e}", exc_info=True)
        raise

def select_output_path():
    output_path = filedialog.askdirectory()
    if output_path:
        logger.info(f"Output path selected: {output_path}")
        return output_path
    return None

def show_error(message):
    messagebox.showerror("错误", message)

def adjust_speech_rate(content, speech_rate):
    logger.info("Adjusting speech rate")
    lines = content.split('\n')
    adjusted_lines = []
    for line in lines:
        words = line.split()
        adjusted_words = []
        for word in words:
            adjusted_words.append(word)
            if len(adjusted_words) >= speech_rate:
                adjusted_lines.append(' '.join(adjusted_words))
                adjusted_words = []
        if adjusted_words:
            adjusted_lines.append(' '.join(adjusted_words))
    logger.info("Speech rate adjustment completed")
    return '\n'.join(adjusted_lines)

def load_config():
    logger.info("Loading configuration from TOML file")
    config_file_path = 'config.toml'
    if not os.path.exists(config_file_path):
        logger.error(f"Configuration file '{config_file_path}' not found.")
        messagebox.showerror("错误", "配置文件未找到，请检查文件路径。")
        raise FileNotFoundError(f"Configuration file '{config_file_path}' not found.")

    try:
        config = toml.load(config_file_path)
        logger.info("Configuration loaded successfully.")
        return config
    except Exception as e:
        logger.error(f"Failed to load configuration: {e}", exc_info=True)
        raise

def save_config(config_data):
    logger.info("Saving configuration to TOML file")
    config_file_path = 'config.toml'
    try:
        with open(config_file_path, 'w', encoding='utf-8') as file:
            toml.dump(config_data, file)
            logger.info("Configuration saved successfully.")
    except Exception as e:
        logger.error(f"Failed to save configuration: {e}", exc_info=True)
        raise