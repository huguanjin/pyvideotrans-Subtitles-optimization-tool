import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkinter import TclError
from subtitle_toolbox import SubtitleToolbox
from timestamp_optimizer import TimestampOptimizer
from subtitle_optimizer import SubtitleOptimizer
from standard_mode import StandardMode
from config_ui import ConfigUI  # Add this import at the top
import logging
from logging_config import setup_logging
import re
from utils import load_config  # Import the utility function for loading configuration

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)

class SRTTranslateTools:
    def __init__(self, root):
        self.root = root
        self.root.title("SRT Translate Tools")

        # Load configuration settings
        try:
            config = load_config()  # Load configuration from TOML file
            self.language = config.get('ui', {}).get('language', 'en')  # Set language
            self.speech_rate = config.get('ui', {}).get('speech_rate', 2)  # Set speech rate
            logger.info("Configuration loaded successfully.")
        except FileNotFoundError as e:
            logger.error(f"Configuration file not found: {e}", exc_info=True)
            messagebox.showerror("错误", "配置文件未找到，请检查文件路径。")
            self.language = 'en'  # Fallback to default language
            self.speech_rate = 2  # Fallback to default speech rate
        except Exception as e:
            logger.error(f"Error loading configuration: {e}", exc_info=True)
            messagebox.showerror("错误", f"加载配置失败: {e}")
            self.language = 'en'  # Fallback to default language
            self.speech_rate = 2  # Fallback to default speech rate

        # Initialize speed_var
        self.speed_var = tk.StringVar(value=str(self.speech_rate))  # Set default speech rate value from config
        self.punctuation_var = tk.BooleanVar(value=False)

        # Set a consistent size for the main window
        self.root.geometry("800x600")

        # Use Tkinter's styling capabilities
        self.configure_styles()

        self.create_ui()

    def configure_styles(self):
        style = ttk.Style()
        style.theme_use('clam')  # Use a modern theme
        style.configure('TButton', font=('Helvetica', 12), padding=6, background='#007bff', foreground='white')
        style.map('TButton', background=[('active', '#0056b3')])
        style.configure('TLabel', font=('Helvetica', 12))
        style.configure('TEntry', font=('Helvetica', 12))
        style.configure('TCheckbutton', font=('Helvetica', 12))
        style.configure('TFrame', background='#f0f0f0')
        style.configure('TNotebook.Tab', font=('Helvetica', 12), padding=[10, 5])

    def create_ui(self):
        # Create a tabbed interface
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=1, fill='both')

        # Create a frame for Subtitle Toolbox directly in the main content area
        self.subtitle_toolbox_frame = tk.Frame(self.notebook)
        self.notebook.add(self.subtitle_toolbox_frame, text='字幕内容格式处理工具箱')
        SubtitleToolbox(self.subtitle_toolbox_frame, self.language)

        # Create a frame for Standard Mode directly in the main content area
        self.standard_mode_frame = tk.Frame(self.notebook)
        self.notebook.add(self.standard_mode_frame, text='标准模式')
        StandardMode(self.standard_mode_frame, self.language)

        # Add Timestamp Optimizer tab using add_tab method
        self.add_tab('字幕时间戳优化工具箱', TimestampOptimizer)

        # Create a frame for Subtitle Optimizer directly in the main content area
        self.subtitle_optimizer_frame = tk.Frame(self.notebook)
        self.notebook.add(self.subtitle_optimizer_frame, text='srt字幕优化神器')
        SubtitleOptimizer(self.subtitle_optimizer_frame, self.language)

        # Add a button to open the configuration UI
        config_button = tk.Button(self.root, text="配置设置", command=self.open_config_ui)
        config_button.pack(side=tk.LEFT, padx=5)

        # Add navigation buttons to switch between tabs
        toolbox_button = tk.Button(self.root, text="字幕内容格式处理工具箱", command=lambda: self.switch_to_tab('字幕内容格式处理工具箱'))
        toolbox_button.pack(side=tk.LEFT, padx=5)

        timestamp_button = tk.Button(self.root, text="字幕时间戳优化工具箱", command=lambda: self.switch_to_tab('字幕时间戳优化工具箱'))
        timestamp_button.pack(side=tk.LEFT, padx=5)

        optimizer_button = tk.Button(self.root, text="srt字幕优化神器", command=lambda: self.switch_to_tab('srt字幕优化神器'))
        optimizer_button.pack(side=tk.LEFT, padx=5)

        standard_mode_button = tk.Button(self.root, text="标准模式", command=lambda: self.switch_to_tab('标准模式'))
        standard_mode_button.pack(side=tk.LEFT, padx=5)

    def open_config_ui(self):
        config_window = tk.Toplevel(self.root)
        config_window.title("配置设置")
        ConfigUI(config_window, language=self.language)

    def switch_to_tab(self, tab_name):
        try:
            tab_index = self.notebook.index(tab_name)
            logger.info(f"Switching to tab: {tab_name} (index: {tab_index})")
            self.notebook.select(tab_index)
        except TclError:
            logger.error(f"Tab '{tab_name}' not found. Unable to switch.")
            messagebox.showerror("错误", f"无法切换到标签: {tab_name}，标签未找到。")

    def add_tab(self, tab_name, widget_class):
        frame = tk.Frame(self.notebook)
        self.notebook.add(frame, text=tab_name)

        # Initialize the corresponding UI component for the tab
        widget_class(frame, self.language)

    def import_files(self):
        file_paths = filedialog.askopenfilenames(filetypes=[("SRT files", "*.srt")])
        if file_paths:
            self.file_paths = file_paths
            messagebox.showinfo("文件已导入", f"已导入文件: {', '.join(file_paths)}")
            logger.info(f"Files imported: {', '.join(file_paths)}")

    def select_save_path(self):
        save_path = filedialog.askdirectory()
        if save_path:
            self.save_path = save_path
            messagebox.showinfo("保存路径已选择", f"保存路径: {save_path}")
            logger.info(f"Save path selected: {save_path}")

    def start_processing(self):
        if not hasattr(self, 'file_paths') or not self.file_paths:
            messagebox.showerror("错误", "未导入文件")
            return
        if not hasattr(self, 'save_path') or not self.save_path:
            messagebox.showerror("错误", "未选择保存路径")
            return
        try:
            speech_rate = float(self.speed_var.get())
        except ValueError:
            messagebox.showerror("错误", "请输入有效的语速值")
            return

        # Process uploaded SRT files
        for file_path in self.file_paths:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()

                # Apply speech rate
                adjusted_content = self.adjust_speech_rate(content, speech_rate)

                # Remove punctuation if selected
                if hasattr(self, 'punctuation_var') and self.punctuation_var.get():
                    adjusted_content = self.remove_punctuation(adjusted_content)

                # Save the processed file
                output_file_path = f"{self.save_path}/{file_path.split('/')[-1]}"
                with open(output_file_path, 'w', encoding='utf-8') as output_file:
                    output_file.write(adjusted_content)

            except Exception as e:
                logger.error(f"Error processing file: {file_path}. Error: {e}", exc_info=True)
                messagebox.showerror("错误", f"处理文件时发生错误: {file_path}. Error: {e}")
                return

        messagebox.showinfo("处理完成", "文件处理完成")
        logger.info("File processing completed")

    def adjust_speech_rate(self, content, speech_rate):
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

    def remove_punctuation(self, content):
        logger.info("Removing punctuation from content")
        return re.sub(r'[^\w\s]', '', content)

    def start_timestamp_optimization(self):
        logger.info("Starting timestamp optimization...")
        optimizer = TimestampOptimizer(self.root, self.language)
        optimizer.process_files()  # Call the process method from TimestampOptimizer

    def start_subtitle_optimization(self):
        logger.info("Starting subtitle optimization...")
        optimizer = SubtitleOptimizer(self.root, self.language)
        optimizer.process_files()  # Call the process method from SubtitleOptimizer

# Define the StandardMode class with implemented functionality
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

if __name__ == "__main__":
    root = tk.Tk()
    app = SRTTranslateTools(root)
    root.mainloop()