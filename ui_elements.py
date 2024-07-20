# ui_elements.py

import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk
from localization import get_translation
import logging

logger = logging.getLogger(__name__)

class SubtitleToolbox:
    def __init__(self, root, language='en'):
        self.root = root
        self.language = language

        self.toolbox_window = tk.Toplevel(self.root)
        self.toolbox_window.title(get_translation("字幕内容格式处理工具箱", self.language))

        self.create_ui()

    def create_ui(self):
        self.frame = tk.Frame(self.toolbox_window)
        self.frame.pack(padx=10, pady=10)

        self.upload_button = tk.Button(self.frame, text=get_translation("批量导入srt字幕文件", self.language), command=self.upload_files)
        self.upload_button.grid(row=0, column=0, padx=5, pady=5)

        self.output_path_button = tk.Button(self.frame, text=get_translation("选择文件保存路径", self.language), command=self.select_output_path)
        self.output_path_button.grid(row=0, column=1, padx=5, pady=5)

        self.remove_punctuation_button = tk.Button(self.frame, text=get_translation("批量去除空格", self.language), command=self.remove_punctuation)
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
            self.file_listbox.delete(0, tk.END)
            for file_path in file_paths:
                self.file_listbox.insert(tk.END, file_path)
            messagebox.showinfo(get_translation("Files Uploaded", self.language), f"{get_translation('Files Uploaded', self.language)}: {', '.join(file_paths)}")
            logger.info(f"Files uploaded: {', '.join(file_paths)}")

    def select_output_path(self):
        output_path = filedialog.askdirectory()
        if output_path:
            messagebox.showinfo(get_translation("Output Path Selected", self.language), f"{get_translation('Output Path Selected', self.language)}: {output_path}")
            logger.info(f"Output path selected: {output_path}")

    def remove_punctuation(self):
        # Placeholder for future implementation
        pass

if __name__ == "__main__":
    root = tk.Tk()
    app = SubtitleToolbox(root, language='zh')
    root.mainloop()