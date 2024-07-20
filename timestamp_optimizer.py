import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from localization import get_translation
import logging
from srt_handler import SRTHandler
import os
from utils import upload_files, select_output_path, show_error, adjust_speech_rate  # Import the adjust_speech_rate function

logger = logging.getLogger(__name__)

class TimestampOptimizer:
    def __init__(self, root, language='en'):
        self.root = root
        self.language = language

        self.file_paths = []
        self.output_path = None
        self.speech_rate = 2  # Default speech rate in characters per second
        self.shorten_intervals = tk.BooleanVar(value=False)

        self.create_ui()

    def create_ui(self):
        self.frame = tk.Frame(self.root)
        self.frame.pack(padx=10, pady=10)

        # Buttons
        self.upload_button = tk.Button(self.frame, text=get_translation("批量导入srt字幕文件", self.language), command=self.upload_files)
        self.upload_button.grid(row=0, column=0, padx=5, pady=5)

        self.output_path_button = tk.Button(self.frame, text=get_translation("选择文件输出路径", self.language), command=self.select_output_path)
        self.output_path_button.grid(row=0, column=1, padx=5, pady=5)

        self.process_button = tk.Button(self.frame, text=get_translation("批量处理字幕文件", self.language), command=self.process_files)
        self.process_button.grid(row=0, column=2, padx=5, pady=5)

        self.preview_button = tk.Button(self.frame, text=get_translation("预览调整后的时间戳", self.language), command=self.preview_timestamps)
        self.preview_button.grid(row=0, column=3, padx=5, pady=5)

        # Speech rate input
        self.speech_rate_label = tk.Label(self.frame, text=get_translation("请输入语速（汉字/秒）", self.language))
        self.speech_rate_label.grid(row=1, column=0, padx=5, pady=5)
        self.speech_rate_entry = tk.Entry(self.frame)
        self.speech_rate_entry.insert(0, str(self.speech_rate))
        self.speech_rate_entry.grid(row=1, column=1, padx=5, pady=5)

        # Shorten intervals checkbox
        self.shorten_intervals_checkbox = tk.Checkbutton(self.frame, text=get_translation("允许缩短时间间隔", self.language), variable=self.shorten_intervals)
        self.shorten_intervals_checkbox.grid(row=1, column=2, padx=5, pady=5)

        # Listbox for file paths
        self.file_listbox = tk.Listbox(self.frame, width=60, height=10)
        self.file_listbox.grid(row=2, column=0, columnspan=4, padx=5, pady=5)

        # Label to display the selected output path
        self.output_path_label = tk.Label(self.frame, text="", wraplength=400)
        self.output_path_label.grid(row=3, column=0, columnspan=4, padx=5, pady=5)

        # Progress bar
        self.progress = ttk.Progressbar(self.frame, orient="horizontal", length=400, mode="determinate")
        self.progress.grid(row=4, column=0, columnspan=4, padx=5, pady=5)

        # Status label
        self.status_label = tk.Label(self.frame, text="", wraplength=400)
        self.status_label.grid(row=5, column=0, columnspan=4, padx=5, pady=5)

    def upload_files(self):
        file_paths = filedialog.askopenfilenames(filetypes=[("SRT files", "*.srt")])
        if file_paths:
            self.file_paths = file_paths
            self.file_listbox.delete(0, tk.END)
            for file_path in file_paths:
                self.file_listbox.insert(tk.END, file_path)
            messagebox.showinfo(get_translation("Files Uploaded", self.language), f"{get_translation('Files Uploaded', self.language)}: {', '.join(file_paths)}")
            logger.info(f"Files uploaded: {', '.join(file_paths)}")

    def select_output_path(self):
        output_path = select_output_path()  # Use utility function
        if output_path:
            self.output_path = output_path
            self.output_path_label.config(text=f"{get_translation('输出路径', self.language)}: {output_path}")
            messagebox.showinfo(get_translation("Output Path Selected", self.language), f"{get_translation('Output Path Selected', self.language)}: {output_path}")
            logger.info(f"Output path selected: {output_path}")

    def process_files(self):
        if not self.file_paths:
            show_error(get_translation("No files uploaded for processing.", self.language))
            logger.error("No files uploaded for processing.")
            return

        if not self.output_path:
            show_error(get_translation("No output path selected.", self.language))
            logger.error("No output path selected.")
            return

        try:
            self.speech_rate = float(self.speech_rate_entry.get())
        except ValueError:
            show_error(get_translation("Invalid speech rate. Please enter a valid number.", self.language))
            logger.error("Invalid speech rate input.")
            return

        self.progress["value"] = 0
        self.progress["maximum"] = len(self.file_paths)
        self.status_label.config(text="Processing files...")

        for i, file_path in enumerate(self.file_paths):
            try:
                srt_handler = SRTHandler(file_path)
                srt_handler.adjust_timestamps(self.speech_rate, self.shorten_intervals.get())
                output_file_path = os.path.join(self.output_path, os.path.basename(file_path))
                srt_handler.save_subtitles(output_file_path)
                self.progress["value"] = i + 1
                self.status_label.config(text=f"Processed {i + 1} of {len(self.file_paths)} files")
                self.root.update_idletasks()
                logger.info(f"Processed file: {file_path}")
            except Exception as e:
                logger.error(f"Error processing file: {file_path}. Error: {e}", exc_info=True)
                show_error(f"{get_translation('An error occurred while processing the file', self.language)}: {file_path}. Error: {e}")

        self.status_label.config(text="Processing completed successfully.")
        messagebox.showinfo(get_translation("Processing Complete", self.language), get_translation("Processing completed successfully.", self.language))
        logger.info("Processing completed successfully.")

    def preview_timestamps(self):
        if not self.file_paths:
            show_error(get_translation("No files uploaded for preview.", self.language))
            logger.error("No files uploaded for preview.")
            return

        try:
            self.speech_rate = float(self.speech_rate_entry.get())
        except ValueError:
            show_error(get_translation("Invalid speech rate. Please enter a valid number.", self.language))
            logger.error("Invalid speech rate input.")
            return

        preview_window = tk.Toplevel(self.root)
        preview_window.title(get_translation("预览调整后的时间戳", self.language))

        preview_text = tk.Text(preview_window, wrap=tk.WORD, width=80, height=20)
        preview_text.pack(padx=10, pady=10)

        for file_path in self.file_paths:
            try:
                srt_handler = SRTHandler(file_path)
                adjusted_subtitles = srt_handler.adjust_timestamps(self.speech_rate, self.shorten_intervals.get(), preview=True)
                preview_text.insert(tk.END, f"File: {file_path}\n")
                for subtitle in adjusted_subtitles:
                    preview_text.insert(tk.END, f"{subtitle['index']}\n{subtitle['start_time']} --> {subtitle['end_time']}\n{subtitle['text']}\n\n")
            except Exception as e:
                logger.error(f"Error previewing file: {file_path}. Error: {e}", exc_info=True)
                show_error(f"{get_translation('An error occurred while previewing the file', self.language)}: {file_path}. Error: {e}")

        preview_text.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = TimestampOptimizer(root, language='zh')
    root.mainloop()