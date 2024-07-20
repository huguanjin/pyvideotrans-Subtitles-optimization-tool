import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk
import os
import re
import logging
from srt_handler import SRTHandler
from localization import get_translation

logger = logging.getLogger(__name__)

class SubtitleFormatter:
    def __init__(self, root, language='en'):
        self.root = root
        self.root.title(get_translation("Subtitle Content Formatting Toolbox", language))
        self.language = language

        self.file_paths = []
        self.output_path = None
        self.srt_handlers = []

        self.create_ui()

    def create_ui(self):
        self.frame = tk.Frame(self.root)
        self.frame.pack(padx=10, pady=10)

        # Buttons
        self.upload_button = tk.Button(self.frame, text=get_translation("Upload SRT Files", self.language), command=self.upload_files)
        self.upload_button.grid(row=0, column=0, padx=5, pady=5)

        self.output_path_button = tk.Button(self.frame, text=get_translation("Select Output Path", self.language), command=self.select_output_path)
        self.output_path_button.grid(row=0, column=1, padx=5, pady=5)

        self.remove_punctuation_button = tk.Button(self.frame, text=get_translation("Remove Punctuation", self.language), command=self.remove_punctuation)
        self.remove_punctuation_button.grid(row=0, column=2, padx=5, pady=5)

        # Listbox for file paths
        self.file_listbox = tk.Listbox(self.frame, width=60, height=10)
        self.file_listbox.grid(row=1, column=0, columnspan=3, padx=5, pady=5)

        # Text widget to display SRT content
        self.subtitle_text = scrolledtext.ScrolledText(self.frame, wrap=tk.WORD, width=60, height=20)
        self.subtitle_text.grid(row=2, column=0, columnspan=3, padx=5, pady=5)

        # Progress bar
        self.progress = ttk.Progressbar(self.frame, orient="horizontal", length=400, mode="determinate")
        self.progress.grid(row=3, column=0, columnspan=3, padx=5, pady=5)

    def upload_files(self):
        file_paths = filedialog.askopenfilenames(filetypes=[("SRT files", "*.srt")])
        if file_paths:
            self.file_paths = file_paths
            self.srt_handlers = [SRTHandler(file_path) for file_path in file_paths]
            self.file_listbox.delete(0, tk.END)
            for file_path in file_paths:
                self.file_listbox.insert(tk.END, file_path)
                self.display_srt_content(file_path)
            messagebox.showinfo(get_translation("Files Uploaded", self.language), f"{get_translation('Files Uploaded', self.language)}: {', '.join(file_paths)}")
            logger.info(f"Files uploaded: {', '.join(file_paths)}")

    def display_srt_content(self, file_path):
        srt_handler = SRTHandler(file_path)
        subtitles = srt_handler.get_subtitles()
        content = "\n\n".join([f"{subtitle['index']}\n{subtitle['start_time']} --> {subtitle['end_time']}\n{subtitle['text']}" for subtitle in subtitles])
        self.subtitle_text.insert(tk.END, content + "\n\n")

    def select_output_path(self):
        output_path = filedialog.askdirectory()
        if output_path:
            self.output_path = output_path
            messagebox.showinfo(get_translation("Output Path Selected", self.language), f"{get_translation('Output Path Selected', self.language)}: {output_path}")
            logger.info(f"Output path selected: {output_path}")

    def remove_punctuation(self):
        if not self.file_paths:
            messagebox.showerror(get_translation("Error", self.language), get_translation("No files uploaded for processing.", self.language))
            return

        if not self.output_path:
            messagebox.showerror(get_translation("Error", self.language), get_translation("No output path selected.", self.language))
            return

        self.progress["value"] = 0
        self.progress["maximum"] = len(self.file_paths)

        for i, srt_handler in enumerate(self.srt_handlers):
            try:
                subtitles = srt_handler.get_subtitles()
                for subtitle in subtitles:
                    subtitle['text'] = self.process_text(subtitle['text'])
                output_file_path = os.path.join(self.output_path, os.path.basename(srt_handler.file_path))
                srt_handler.save_subtitles(output_file_path)
                self.progress["value"] = i + 1
                self.root.update_idletasks()
                logger.info(f"Processed file: {output_file_path}")
            except Exception as e:
                logger.error(f"Error processing file: {e}", exc_info=True)
                messagebox.showerror(get_translation("Error", self.language), f"{get_translation('An error occurred while processing the file', self.language)}: {e}")

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
            os.startfile(self.output_path)

if __name__ == "__main__":
    root = tk.Tk()
    app = SubtitleFormatter(root, language='zh')
    root.mainloop()