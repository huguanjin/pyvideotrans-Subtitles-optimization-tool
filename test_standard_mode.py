# test_standard_mode.py

import unittest
from standard_mode import StandardMode
import tkinter as tk
import logging
import os

logger = logging.getLogger(__name__)

class TestStandardMode(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.app = StandardMode(self.root, language='zh')

    def tearDown(self):
        self.root.destroy()

    def test_speech_rate_entry(self):
        logger.info("Testing speech rate entry functionality.")
        self.app.speech_rate_entry.insert(0, "2")
        self.assertEqual(self.app.speech_rate_entry.get(), "2")
        logger.info("Speech rate entry test completed successfully.")

    def test_start_processing(self):
        logger.info("Testing start processing functionality.")
        self.app.speech_rate_entry.insert(0, "2")  # Simulate valid speech rate input
        test_file_path = 'test.srt'  # Use an actual test file path
        with open(test_file_path, 'w') as f:
            f.write("1\n00:00:01,000 --> 00:00:02,000\nHello World\n\n")
        self.app.file_paths = [test_file_path]  # Mock file path
        self.app.output_path = '.'  # Mock save path
        self.app.start_processing()  # Call the processing method
        
        output_file = os.path.join('.', 'test_processed.srt')
        self.assertTrue(os.path.exists(output_file), "Output file was not created.")
        
        # Additional verification: Check if the output file contains expected content
        with open(output_file, 'r') as f:
            content = f.read()
            self.assertIn("Hello World", content, "Output file does not contain expected subtitle text.")
        
        os.remove(output_file)
        os.remove(test_file_path)
        logger.info("Start processing test completed successfully.")

    def test_clear_input(self):
        logger.info("Testing clear input functionality.")
        self.app.speech_rate_entry.insert(0, "2")
        self.app.clear_input()  # Call the clear input method
        self.assertEqual(self.app.speech_rate_entry.get(), "")
        logger.info("Clear input test completed successfully.")

if __name__ == '__main__':
    unittest.main()