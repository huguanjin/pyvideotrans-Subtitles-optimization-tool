import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk, simpledialog
from localization import get_translation
import logging
from srt_handler import SRTHandler
import os
from translator import Translator
import re
import concurrent.futures
from utils import upload_files, select_output_path, show_error, adjust_speech_rate  # Consolidated utility functions
from config import DEEPSEEK_API_KEY, DEEPSEEK_API_URL  # Import configuration settings

logger = logging.getLogger(__name__)

class SubtitleOptimizer:
    def __init__(self, root, language='en'):
        self.root = root
        self.language = language

        self.file_paths = []
        self.output_path = None

        self.create_ui()

    def create_ui(self):
        self.frame = tk.Frame(self.root)
        self.frame.pack(padx=10, pady=10)

        self.upload_button = tk.Button(self.frame, text=get_translation("上传SRT文件", self.language), command=self.upload_files)
        self.upload_button.grid(row=0, column=0, padx=5, pady=5)

        self.extract_button = tk.Button(self.frame, text=get_translation("提取内容", self.language), command=self.extract_content)
        self.extract_button.grid(row=0, column=1, padx=5, pady=5)

        self.translate_button = tk.Button(self.frame, text=get_translation("翻译内容", self.language), command=self.translate_content)
        self.translate_button.grid(row=0, column=2, padx=5, pady=5)

        self.preview_button = tk.Button(self.frame, text=get_translation("预览字幕", self.language), command=self.preview_subtitles)
        self.preview_button.grid(row=0, column=3, padx=5, pady=5)

        # Listbox for file paths
        self.file_listbox = tk.Listbox(self.frame, width=60, height=10)
        self.file_listbox.grid(row=1, column=0, columnspan=4, padx=5, pady=5)

        # Text widget to display SRT content
        self.subtitle_text = scrolledtext.ScrolledText(self.frame, wrap=tk.WORD, width=60, height=20)
        self.subtitle_text.grid(row=2, column=0, columnspan=4, padx=5, pady=5)

        # Progress bar
        self.progress = ttk.Progressbar(self.frame, orient="horizontal", length=400, mode="determinate")
        self.progress.grid(row=3, column=0, columnspan=4, padx=5, pady=5)

        # Speech rate input field
        self.speech_rate_label = tk.Label(self.frame, text=get_translation("请输入语速（汉字/秒）", self.language))
        self.speech_rate_label.grid(row=4, column=0, padx=5, pady=5)

        self.speech_rate_entry = tk.Entry(self.frame)
        self.speech_rate_entry.grid(row=4, column=1, padx=5, pady=5)

        # Start processing button
        self.start_processing_button = tk.Button(self.frame, text=get_translation("开始处理", self.language), command=self.start_processing)
        self.start_processing_button.grid(row=4, column=2, padx=5, pady=5)

        # Clear input button
        self.clear_input_button = tk.Button(self.frame, text=get_translation("清除输入", self.language), command=self.clear_input)
        self.clear_input_button.grid(row=4, column=3, padx=5, pady=5)

    def upload_files(self):
        file_paths = filedialog.askopenfilenames(filetypes=[("SRT files", "*.srt")])
        if file_paths:
            self.file_paths = file_paths
            self.file_listbox.delete(0, tk.END)
            for file_path in file_paths:
                self.file_listbox.insert(tk.END, file_path)
            messagebox.showinfo(get_translation("文件已上传", self.language), f"{get_translation('文件已上传', self.language)}: {', '.join(file_paths)}")
            logger.info(f"Files uploaded: {', '.join(file_paths)}")

    def extract_content(self):
        if not self.file_paths:
            messagebox.showerror(get_translation("错误", self.language), get_translation("没有文件上传进行处理。", self.language))
            return

        self.progress["value"] = 0
        self.progress["maximum"] = len(self.file_paths)

        extracted_files = []
        for i, file_path in enumerate(self.file_paths):
            try:
                srt_handler = SRTHandler(file_path)
                content = srt_handler.extract_subtitle_text()
                if content:
                    extracted_files.append(content)
                self.progress["value"] = i + 1
                self.root.update_idletasks()
                logger.info(f"Extracted content from file: {file_path}")
            except Exception as e:
                logger.error(f"Error extracting content from file: {file_path}. Error: {e}", exc_info=True)
                messagebox.showerror(get_translation("错误", self.language), f"{get_translation('处理文件时发生错误', self.language)}: {file_path}. Error: {e}")

        if extracted_files:
            try:
                merged_content = SRTHandler.merge_subtitle_texts(extracted_files)
                self.display_extracted_content(merged_content)
            except Exception as e:
                logger.error(f"Error merging subtitle texts: {e}", exc_info=True)
                messagebox.showerror(get_translation("错误", self.language), f"{get_translation('合并字幕内容时发生错误', self.language)}: {e}")

        messagebox.showinfo(get_translation("处理完成", self.language), get_translation("处理成功完成。", self.language))
        logger.info("Content extraction completed successfully.")

    def display_extracted_content(self, content):
        self.subtitle_text.insert(tk.END, content + "\n\n")
        self.merged_content = content

    def translate_content(self):
        if not hasattr(self, 'merged_content') or not self.merged_content:
            messagebox.showerror(get_translation("错误", self.language), get_translation("没有提取的内容进行翻译。", self.language))
            return

        target_language = simpledialog.askstring(get_translation("输入", self.language), get_translation("输入目标语言代码（例如，'en'表示英语）:", self.language))
        if not target_language:
            return

        self.progress["value"] = 0
        self.progress["maximum"] = 100  # Set a fixed maximum for the progress bar

        try:
            translator = Translator()
            with concurrent.futures.ThreadPoolExecutor() as executor:
                chunks = self.split_translated_text(self.merged_content, 10)
                future_to_text = {executor.submit(translator.translate_text, chunk, target_language): chunk for chunk in chunks}
                translated_chunks = []
                for future in concurrent.futures.as_completed(future_to_text):
                    translated_chunks.append(future.result())
            translated_content = ' '.join(translated_chunks)
            self.display_translated_content(translated_content)
            messagebox.showinfo(get_translation("翻译完成", self.language), get_translation("翻译成功完成。", self.language))
            logger.info("Translation completed successfully.")
        except Exception as e:
            logger.error(f"Error translating content: {e}", exc_info=True)
            messagebox.showerror(get_translation("错误", self.language), f"{get_translation('翻译内容时发生错误', self.language)}: {e}")

    def display_translated_content(self, content):
        self.subtitle_text.insert(tk.END, content + "\n\n")

    def preview_subtitles(self):
        if not hasattr(self, 'merged_content') or not self.merged_content:
            messagebox.showerror(get_translation("错误", self.language), get_translation("没有提取的内容进行预览。", self.language))
            return

        preview_window = tk.Toplevel(self.root)
        preview_window.title(get_translation("预览字幕", self.language))

        preview_text = scrolledtext.ScrolledText(preview_window, wrap=tk.WORD, width=80, height=20)
        preview_text.pack(padx=10, pady=10)

        preview_text.insert(tk.END, self.merged_content)
        preview_text.config(state=tk.DISABLED)

    def start_processing(self):
        if not self.file_paths:
            messagebox.showerror(get_translation("错误", self.language), get_translation("没有文件上传进行处理。", self.language))
            return

        try:
            speech_rate = float(self.speech_rate_entry.get())
        except ValueError:
            messagebox.showerror(get_translation("错误", self.language), get_translation("请输入有效的语速值。", self.language))
            return

        self.progress["value"] = 0
        self.progress["maximum"] = len(self.file_paths)

        for i, file_path in enumerate(self.file_paths):
            try:
                srt_handler = SRTHandler(file_path)
                subtitles = srt_handler.get_subtitles()
                for subtitle in subtitles:
                    subtitle['text'] = adjust_speech_rate(subtitle['text'], speech_rate)  # Use utility function

                output_file_path = os.path.join(self.output_path, os.path.basename(file_path))
                srt_handler.save_subtitles(output_file_path)
                self.progress["value"] = i + 1
                self.root.update_idletasks()
                logger.info(f"Processed file: {output_file_path}")
            except Exception as e:
                logger.error(f"Error processing file: {file_path}. Error: {e}", exc_info=True)
                messagebox.showerror(get_translation("错误", self.language), f"{get_translation('处理文件时发生错误', self.language)}: {file_path}. Error: {e}")

        messagebox.showinfo(get_translation("处理完成", self.language), get_translation("文件处理完成。", self.language))
        logger.info("File processing completed")

    def clear_input(self):
        self.speech_rate_entry.delete(0, tk.END)
        logger.info("Input cleared in Subtitle Optimizer")

if __name__ == "__main__":
    root = tk.Tk()
    app = SubtitleOptimizer(root, language='zh')
    root.mainloop()