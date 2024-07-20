import tkinter as tk
from tkinter import filedialog, messagebox
import toml
import logging
from utils import load_config, save_config  # Import the utility functions for loading and saving configuration

logger = logging.getLogger(__name__)

class ConfigUI:
    def __init__(self, root, language='en'):
        self.root = root
        self.language = language
        self.config_file_path = 'config.toml'  # Path to the TOML configuration file
        self.create_ui()

    def create_ui(self):
        self.frame = tk.Frame(self.root)
        self.frame.pack(padx=10, pady=10)

        # Load Configuration Button
        self.load_button = tk.Button(self.frame, text="加载配置", command=self.load_config)
        self.load_button.grid(row=0, column=0, padx=5, pady=5)

        # Save Configuration Button
        self.save_button = tk.Button(self.frame, text="保存配置", command=self.save_config)
        self.save_button.grid(row=0, column=1, padx=5, pady=5)

        # Configuration Display Area
        self.config_text = tk.Text(self.frame, wrap=tk.WORD, width=60, height=20)
        self.config_text.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

        # Speech Rate Input
        self.speech_rate_label = tk.Label(self.frame, text="语速（汉字/秒）")
        self.speech_rate_label.grid(row=2, column=0, padx=5, pady=5)
        self.speech_rate_entry = tk.Entry(self.frame)
        self.speech_rate_entry.grid(row=2, column=1, padx=5, pady=5)

    def load_config(self):
        try:
            config_data = load_config()  # Use the utility function to load config
            self.config_text.delete(1.0, tk.END)  # Clear previous content
            self.config_text.insert(tk.END, toml.dumps(config_data))  # Insert loaded config

            # Load specific fields into entry
            self.speech_rate_entry.delete(0, tk.END)
            self.speech_rate_entry.insert(0, config_data['ui']['speech_rate'])  # Load speech rate

            logger.info("Configuration loaded successfully.")
        except Exception as e:
            logger.error(f"Failed to load configuration: {e}", exc_info=True)
            messagebox.showerror("错误", f"加载配置失败: {e}")

    def save_config(self):
        try:
            config_data = toml.loads(self.config_text.get(1.0, tk.END).strip())  # Validate TOML format before saving

            # Update speech rate from entry
            config_data['ui']['speech_rate'] = float(self.speech_rate_entry.get())

            save_config(config_data)  # Use the utility function to save config
            logger.info("Configuration saved successfully.")
            messagebox.showinfo("信息", "配置已保存成功")
        except toml.TomlDecodeError as e:
            logger.error(f"Invalid TOML format: {e}", exc_info=True)
            messagebox.showerror("错误", f"保存配置失败: 无效的配置格式: {e}")
        except Exception as e:
            logger.error(f"Failed to save configuration: {e}", exc_info=True)
            messagebox.showerror("错误", f"保存配置失败: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ConfigUI(root)
    root.mainloop()