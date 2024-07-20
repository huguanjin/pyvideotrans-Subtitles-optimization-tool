import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk
from localization import get_translation
import logging
from srt_handler import SRTHandler
import os
import re
from utils import upload_files, select_output_path, show_error

logger = logging.getLogger(__name__)

class SubtitleToolbox:
    def __init__(self, root, language='en'):
        self.root = root
        self.language = language

        self.file_paths = []  # Initialize an empty list to store file paths
        self.output_path = None
        self.srt_handlers = []

        self.create_ui()

    def create_ui(self):
        self.frame = tk.Frame(self.root)
        self.frame.pack(padx=10, pady=10)

        # Buttons
        self.upload_button = tk.Button(self.frame, text=get_translation("批量导入srt字幕文件", self.language), command=self.upload_files)
        self.upload_button.grid(row=0, column=0, padx=5, pady=5)

        self.output_path_button = tk.Button(self.frame, text=get_translation("选择文件保存路径", self.language), command=self.select_output_path)
        self.output_path_button.grid(row=0, column=1, padx=5, pady=5)

        self.remove_punctuation_button = tk.Button(self.frame, text=get_translation("批量去除空格", self.language), command=self.remove_punctuation)
        self.remove_punctuation_button.grid(row=0, column=2, padx=5, pady=5)

        # Add a button to process files
        self.process_button = tk.Button(self.frame, text=get_translation("开始处理", self.language), command=self.process_files)
        self.process_button.grid(row=0, column=3, padx=5, pady=5)

        # Listbox for file paths
        self.file_listbox = tk.Listbox(self.frame, width=60, height=10)
        self.file_listbox.grid(row=1, column=0, columnspan=4, padx=5, pady=5)

        # Text widget to display SRT content
        self.subtitle_text = scrolledtext.ScrolledText(self.frame, wrap=tk.WORD, width=60, height=20)
        self.subtitle_text.grid(row=2, column=0, columnspan=4, padx=5, pady=5)

        # Progress bar
        self.progress = ttk.Progressbar(self.frame, orient="horizontal", length=400, mode="determinate")
        self.progress.grid(row=3, column=0, columnspan=4, padx=5, pady=5)

        # Status label
        self.status_label = tk.Label(self.frame, text="", wraplength=400)
        self.status_label.grid(row=4, column=0, columnspan=4, padx=5, pady=5)

        # Standard Mode button
        self.standard_mode_button = tk.Button(self.frame, text=get_translation("标准模式", self.language), command=self.open_standard_mode)
        self.standard_mode_button.grid(row=5, column=0, columnspan=4, padx=5, pady=5)

    def open_standard_mode(self):
        logger.info("Opening Standard Mode")
        from standard_mode import StandardMode
        StandardMode(self.frame, self.language)

    def upload_files(self):
        file_paths = filedialog.askopenfilenames(filetypes=[("SRT files", "*.srt")])  # Open file dialog to select SRT files
        if file_paths:
            self.file_paths = file_paths  # Store the selected file paths
            self.srt_handlers = [SRTHandler(file_path) for file_path in file_paths]  # Initialize SRT handlers
            self.file_listbox.delete(0, tk.END)  # Clear the listbox
            for file_path in file_paths:
                self.file_listbox.insert(tk.END, file_path)  # Insert each file path into the listbox
                self.display_srt_content(file_path)  # Display the content of the SRT file
            messagebox.showinfo(get_translation("Files Uploaded", self.language), f"{get_translation('Files Uploaded', self.language)}: {', '.join(file_paths)}")
            logger.info(f"Files uploaded: {', '.join(file_paths)}")

    def display_srt_content(self, file_path):
        srt_handler = SRTHandler(file_path)
        subtitles = srt_handler.get_subtitles()
        content = "\n\n".join([f"{subtitle['index']}\n{subtitle['start_time']} --> {subtitle['end_time']}\n{subtitle['text']}" for subtitle in subtitles])
        self.subtitle_text.insert(tk.END, content + "\n\n")

    def select_output_path(self):
        self.output_path = select_output_path()  # Use utility function
        if self.output_path:
            messagebox.showinfo(get_translation("Output Path Selected", self.language), f"{get_translation('Output Path Selected', self.language)}: {self.output_path}")

    def validate_paths(self):
        if not self.file_paths:
            logger.error("No files uploaded for processing.")
            show_error(get_translation("No files uploaded for processing.", self.language))
            return False

        if not self.output_path:
            logger.error("No output path selected.")
            show_error(get_translation("No output path selected.", self.language))
            return False

        return True

    def process_files(self):
        if not self.validate_paths():
            return

        self.progress["value"] = 0
        self.progress["maximum"] = len(self.file_paths)
        self.status_label.config(text="Processing files...")

        for i, file_path in enumerate(self.file_paths):
            try:
                srt_handler = SRTHandler(file_path)
                subtitles = srt_handler.get_subtitles()
                for subtitle in subtitles:
                    subtitle['text'] = self.process_text(subtitle['text'])  # Remove punctuation from subtitle text
                output_file_path = os.path.join(self.output_path, os.path.basename(srt_handler.file_path))
                srt_handler.save_subtitles(output_file_path)  # Save the modified subtitles
                self.progress["value"] = i + 1
                self.status_label.config(text=f"Processed {i + 1} of {len(self.file_paths)} files")
                self.root.update_idletasks()
                logger.info(f"Processed file: {output_file_path}")
            except Exception as e:
                logger.error(f"Error processing file: {file_path}. Error: {e}", exc_info=True)
                show_error(f"{get_translation('An error occurred while processing the file', self.language)}: {file_path}. Error: {e}")

        self.status_label.config(text="Processing completed successfully.")
        messagebox.showinfo(get_translation("Processing Complete", self.language), get_translation("Processing completed successfully.", self.language))
        logger.info("Processing completed successfully.")
        self.open_file_location()

    def remove_punctuation(self):
        if not self.validate_paths():
            return

        self.progress["value"] = 0
        self.progress["maximum"] = len(self.file_paths)
        self.status_label.config(text="Processing files...")

        for i, srt_handler in enumerate(self.srt_handlers):
            try:
                subtitles = srt_handler.get_subtitles()
                for subtitle in subtitles:
                    subtitle['text'] = self.process_text(subtitle['text'])  # Remove punctuation from subtitle text
                output_file_path = os.path.join(self.output_path, os.path.basename(srt_handler.file_path))
                srt_handler.save_subtitles(output_file_path)  # Save the modified subtitles
                self.progress["value"] = i + 1
                self.status_label.config(text=f"Processed {i + 1} of {len(self.file_paths)} files")
                self.root.update_idletasks()
                logger.info(f"Processed file: {output_file_path}")
            except Exception as e:
                logger.error(f"Error processing file: {srt_handler.file_path}. Error: {e}", exc_info=True)
                show_error(f"{get_translation('An error occurred while processing the file', self.language)}: {srt_handler.file_path}. Error: {e}")

        self.status_label.config(text="Processing completed successfully.")
        messagebox.showinfo(get_translation("Processing Complete", self.language), get_translation("Processing completed successfully.", self.language))
        logger.info("Processing completed successfully.")
        self.open_file_location()

    def process_text(self, text):
        # Remove punctuation at the beginning and end of lines
        text = re.sub(r'^[^\w\s]+|[^\w\s]+$', '', text)
        # Replace punctuation within lines with spaces
        text = re.sub(r'[^\w\s]', ' ', text)
        return text

    def open_file_location(self):
        if self.output_path:
            try:
                os.startfile(self.output_path)
            except Exception as e:
                logger.error(f"Error opening file location: {self.output_path}. Error: {e}", exc_info=True)
                show_error(f"{get_translation('An error occurred while opening the file location', self.language)}: {self.output_path}. Error: {e}")

    def validate_file_paths(self):
        if not self.file_paths:
            logger.error("No files uploaded for processing.")
            show_error(get_translation("No files uploaded for processing.", self.language))
            return False

        if not self.output_path:
            logger.error("No output path selected.")
            show_error(get_translation("No output path selected.", self.language))
            return False

        return True

if __name__ == "__main__":
    root = tk.Tk()
    app = SubtitleToolbox(root, language='zh')
    root.mainloop()