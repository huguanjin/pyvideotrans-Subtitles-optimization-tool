# srt_handler.py

import re
import logging
import os

logger = logging.getLogger(__name__)

class SRTHandler:
    def __init__(self, file_path):
        self.file_path = file_path
        self.subtitles = []
        self.parse_srt_file()

    def parse_srt_file(self):
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            pattern = re.compile(r'(\d+)\n(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})\n([\s\S]*?)(?=\n\n|\Z)', re.MULTILINE)
            matches = pattern.findall(content)
            self.subtitles = [{
                'index': int(match[0]),
                'start_time': match[1],
                'end_time': match[2],
                'text': match[3].strip()
            } for match in matches]
            logger.info(f"Parsed SRT file: {self.file_path}")
        except Exception as e:
            logger.error(f"Error parsing SRT file: {e}", exc_info=True)

    def get_subtitles(self):
        return self.subtitles

    def extract_subtitle_text(self):
        try:
            base_name = os.path.basename(self.file_path)
            file_name, _ = os.path.splitext(base_name)
            output_file_path = os.path.join(os.path.dirname(self.file_path), f"{file_name}.txt")
            with open(output_file_path, 'w', encoding='utf-8') as file:
                for subtitle in self.subtitles:
                    file.write(f"{subtitle['text']}\n")
            logger.info(f"Extracted subtitle text to: {output_file_path}")
            return output_file_path
        except Exception as e:
            logger.error(f"Error extracting subtitle text: {e}", exc_info=True)
            return None

    @staticmethod
    def merge_subtitle_texts(file_paths):
        merged_text = ""
        for file_path in file_paths:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    merged_text += file.read() + "\n"
            except Exception as e:
                logger.error(f"Error merging subtitle text from file: {file_path}. Error: {e}", exc_info=True)
        return merged_text.strip()

    def save_subtitles(self, output_file_path):
        """
        Saves the subtitles to an SRT file format at the specified path.

        :param output_file_path: Path to save the SRT file
        """
        try:
            with open(output_file_path, 'w', encoding='utf-8') as file:
                for subtitle in self.subtitles:
                    file.write(f"{subtitle['index']}\n")
                    file.write(f"{subtitle['start_time']} --> {subtitle['end_time']}\n")
                    file.write(f"{subtitle['text']}\n\n")
            logger.info(f"Subtitles saved to: {output_file_path}")
        except Exception as e:
            logger.error(f"Error saving subtitles: {e}", exc_info=True)

    def adjust_timestamps(self, speech_rate, shorten_intervals, preview=False):
        adjusted_subtitles = []
        for subtitle in self.subtitles:
            # Adjust subtitle timestamps based on speech_rate and shorten_intervals
            start_time = self.parse_time(subtitle['start_time'])
            end_time = self.parse_time(subtitle['end_time'])
            duration = end_time - start_time
            adjusted_duration = duration / speech_rate
            if shorten_intervals:
                adjusted_duration = max(adjusted_duration, 0)
            adjusted_end_time = start_time + adjusted_duration
            adjusted_subtitle = {
                'index': subtitle['index'],
                'start_time': self.format_time(start_time),
                'end_time': self.format_time(adjusted_end_time),
                'text': subtitle['text']
            }
            adjusted_subtitles.append(adjusted_subtitle)

        if not preview:
            self.subtitles = adjusted_subtitles
            self.save_subtitles(self.file_path)
        else:
            return adjusted_subtitles

    def parse_time(self, time_str):
        hours, minutes, seconds = map(float, time_str.split(':'))
        return hours * 3600 + minutes * 60 + seconds

    def format_time(self, time_value):
        hours = int(time_value // 3600)
        minutes = int((time_value % 3600) // 60)
        seconds = time_value % 60
        return f"{hours:02d}:{minutes:02d}:{seconds:06.3f}".replace('.', ',')