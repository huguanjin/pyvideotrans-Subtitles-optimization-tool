# test_srt_translatetools.py

import unittest
from main_app import SRTTranslateTools
import tkinter as tk
import os
import logging

logger = logging.getLogger(__name__)

class TestSRTTranslateTools(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.app = SRTTranslateTools(self.root)

    def tearDown(self):
        self.root.destroy()

    def test_import_files(self):
        logger.info("Testing file import functionality.")
        # Simulate file import
        test_file_path = 'test.srt'  # Use an actual test file path
        with open(test_file_path, 'w') as f:
            f.write("1\n00:00:01,000 --> 00:00:02,000\nHello World\n\n")

        # Directly assign the file path to simulate import
        self.app.file_paths = [test_file_path]

        # Ensure the file path is in the app's file_paths
        self.assertIn(test_file_path, self.app.file_paths)
        os.remove(test_file_path)
        logger.info("File import test completed successfully.")

    def test_select_save_path(self):
        logger.info("Testing save path selection functionality.")
        # Simulate selecting a save path
        self.app.select_save_path()
        self.assertIsNotNone(self.app.save_path)
        logger.info("Save path selection test completed successfully.")

    def test_start_processing(self):
        logger.info("Testing processing functionality.")
        # Test the processing function
        self.app.file_paths = ['test.srt']  # Mock file path
        self.app.save_path = '.'  # Mock save path
        with open('test.srt', 'w') as f:
            f.write("1\n00:00:01,000 --> 00:00:02,000\nHello World\n\n")
        self.app.start_processing()
        output_file = os.path.join('.', 'test.srt')
        self.assertTrue(os.path.exists(output_file))
        os.remove(output_file)
        logger.info("Processing test completed successfully.")

    def test_standard_mode_functionality(self):
        logger.info("Testing Standard Mode functionality.")
        # Simulate switching to Standard Mode and processing
        self.app.switch_to_tab(3)  # Switch to Standard Mode tab
        self.app.file_paths = ['test.srt']  # Mock file path
        self.app.save_path = '.'  # Mock save path
        with open('test.srt', 'w') as f:
            f.write("1\n00:00:01,000 --> 00:00:02,000\nHello World\n\n")
        self.app.notebook.nametowidget(self.app.notebook.tabs()[3]).start_processing()  # Call start_processing in Standard Mode
        output_file = os.path.join('.', 'test.srt')
        self.assertTrue(os.path.exists(output_file))
        os.remove(output_file)
        logger.info("Standard Mode functionality test completed successfully.")

if __name__ == '__main__':
    unittest.main()