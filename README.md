```markdown
# srt_translatetools

srt_translatetools is a Python-based application designed for translating .srt subtitle files using large language model APIs, such as DeepSeek. It features a user-friendly graphical interface that allows users to import, edit, and export subtitle files seamlessly.

## Overview

The architecture of the srt_translatetools project consists of a Python application utilizing the Tkinter library for the graphical user interface (GUI). The application supports importing and exporting .srt files, displaying and editing subtitle content, and leveraging the DeepSeek API for translation services. The project is organized into multiple modules, each responsible for specific functionalities, such as API interaction, subtitle handling, and configuration management.

### Project Structure

- `main_app.py`: The main application file that initializes the GUI and handles user interactions.
- `config.py`: Configuration settings for connecting to the DeepSeek API.
- `config.toml`: TOML file for user-configurable settings.
- `subtitle_toolbox.py`: Module for subtitle formatting functionalities.
- `timestamp_optimizer.py`: Module for optimizing subtitle timestamps.
- `subtitle_optimizer.py`: Module for subtitle content optimization.
- `standard_mode.py`: Implements the standard processing mode for subtitles.
- `localization.py`: Manages translations for the user interface.
- `logging_config.py`: Configures logging for the application.
- `utils.py`: Contains utility functions for file handling and configuration loading.
- Additional supporting modules for specific functionalities.

## Features

- **File Import and Export**: Users can import .srt subtitle files for processing and export the translated files.
- **Subtitle Display and Editing**: Provides an interface to view and edit subtitles before translation.
- **Translation Functionality**: Utilizes the DeepSeek API to translate subtitles into multiple languages.
- **Graphical User Interface**: A simple and intuitive UI that includes buttons for file selection, translation, and export, along with progress indicators.
- **Configuration Management**: Users can easily modify settings via a TOML configuration file.

## Getting started

### Requirements

To run the srt_translatetools application, ensure you have the following installed on your computer:

- Python 3.x
- Required Python libraries specified in `requirements.txt`
- Access to the DeepSeek API (API key and URL)

### Quickstart

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd srt_translatetools
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure the application by editing the `config.toml` file with your DeepSeek API key and other settings.

4. Run the application:
   ```bash
   python main_app.py
   ```

### License

Copyright (c) 2024.
```