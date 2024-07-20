# standard_mode.py

import tkinter as tk
import logging
from tkinter import messagebox, filedialog
import re
import os

logger = logging.getLogger(__name__)

class StandardMode:
    def __init__(self, frame, language):
        self.frame = frame
        self.language = language
        self.output_path = None  # Initialize output path
        self.create_ui()

    def create_ui(self):
        label = tk.Label(self.frame, text="这是标准模式的功能区", font=('Helvetica', 16))
        label.pack(padx=10, pady=10)

        # Input field for speech rate
        self.speech_rate_label = tk.Label(self.frame, text="请输入语速（汉字/秒）", font=('Helvetica', 12))
        self.speech_rate_label.pack(padx=10, pady=5)

        self.speech_rate_entry = tk.Entry(self.frame)
        self.speech_rate_entry.pack(padx=10, pady=5)

        # Button to select output path
        self.output_path_button = tk.Button(self.frame, text="选择输出路径", command=self.select_output_path)
        self.output_path_button.pack(padx=10, pady=5)

        # Button to start processing
        self.process_button = tk.Button(self.frame, text="开始处理", command=self.start_processing)
        self.process_button.pack(padx=10, pady=10)

        # Button to clear input
        self.clear_button = tk.Button(self.frame, text="清除输入", command=self.clear_input)
        self.clear_button.pack(padx=10, pady=5)

        logger.info("Standard Mode initialized")

    def select_output_path(self):
        self.output_path = filedialog.askdirectory()  # Open a dialog to select a directory
        if self.output_path:
            messagebox.showinfo("输出路径已选择", f"输出路径: {self.output_path}")
            logger.info(f"Output path selected: {self.output_path}")

    def start_processing(self):
        try:
            speech_rate = float(self.speech_rate_entry.get())
            logger.info(f"Processing started with speech rate: {speech_rate}")

            # Process uploaded SRT files
            file_paths = self.get_srt_file_paths()
            if not file_paths:
                logger.error("No SRT files provided for processing")
                messagebox.showerror("错误", "未提供SRT文件进行处理")
                return

            if not self.output_path:
                logger.error("No output path selected")
                messagebox.showerror("错误", "未选择输出路径")
                return

            for file_path in file_paths:
                try:
                    self.process_srt_file(file_path, speech_rate)
                except Exception as e:
                    logger.error(f"Error processing file: {file_path}. Error: {e}", exc_info=True)
                    messagebox.showerror("错误", f"处理文件时发生错误: {file_path}. Error: {e}")

            messagebox.showinfo("处理完成", "处理成功完成。")
            logger.info("Processing completed successfully in Standard Mode")
        except ValueError as e:
            logger.error("Invalid speech rate input", exc_info=True)
            messagebox.showerror("错误", "请输入有效的语速值")
        except Exception as e:
            logger.error(f"Error during processing in Standard Mode: {e}", exc_info=True)
            messagebox.showerror("错误", f"处理过程中发生错误: {e}")

    def clear_input(self):
        self.speech_rate_entry.delete(0, tk.END)
        logger.info("Input cleared in Standard Mode")

    def get_srt_file_paths(self):
        file_paths = filedialog.askopenfilenames(filetypes=[("SRT files", "*.srt")])
        return list(file_paths)

    def process_srt_file(self, file_path, speech_rate):
        logger.info(f"Processing SRT file: {file_path}")
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        # Remove punctuation from the content
        processed_content = self.remove_punctuation(content)

        # Save the modified file to the selected output path
        output_file_path = os.path.join(self.output_path, os.path.splitext(os.path.basename(file_path))[0] + "_processed.srt")
        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            output_file.write(processed_content)

        logger.info(f"Processed SRT file saved to: {output_file_path}")

    def remove_punctuation(self, content):
        # Remove punctuation using regex
        return re.sub(r'[^\w\s]', '', content)