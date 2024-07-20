# test_button_navigation.py

import unittest
from main_app import SRTTranslateTools
import tkinter as tk
import logging

logger = logging.getLogger(__name__)

class TestButtonNavigation(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.app = SRTTranslateTools(self.root, language='zh')

    def tearDown(self):
        self.root.destroy()

    def test_switch_to_subtitle_toolbox(self):
        logger.info("Testing switch to Subtitle Toolbox")
        try:
            self.app.switch_to_tab('字幕内容格式处理工具箱')
            current_tab = self.app.notebook.tab(self.app.notebook.select(), "text")
            self.assertEqual(current_tab, '字幕内容格式处理工具箱')
            logger.info("Successfully switched to Subtitle Toolbox")
            # Assert that the expected UI elements are visible
            self.assertTrue(self.app.subtitle_toolbox_frame.winfo_ismapped(), "Subtitle Toolbox frame should be visible")
        except Exception as e:
            logger.error(f"Error switching to Subtitle Toolbox: {e}", exc_info=True)
            self.fail("Failed to switch to Subtitle Toolbox")

    def test_switch_to_timestamp_optimizer(self):
        logger.info("Testing switch to Timestamp Optimizer")
        try:
            self.app.switch_to_tab('字幕时间戳优化工具箱')
            current_tab = self.app.notebook.tab(self.app.notebook.select(), "text")
            self.assertEqual(current_tab, '字幕时间戳优化工具箱')
            logger.info("Successfully switched to Timestamp Optimizer")
            # Assert that the expected UI elements are visible
            self.assertTrue(self.app.notebook.nametowidget(self.app.notebook.select()).winfo_ismapped(), "Timestamp Optimizer frame should be visible")
        except Exception as e:
            logger.error(f"Error switching to Timestamp Optimizer: {e}", exc_info=True)
            self.fail("Failed to switch to Timestamp Optimizer")

    def test_switch_to_subtitle_optimizer(self):
        logger.info("Testing switch to Subtitle Optimizer")
        try:
            self.app.switch_to_tab('srt字幕优化神器')
            current_tab = self.app.notebook.tab(self.app.notebook.select(), "text")
            self.assertEqual(current_tab, 'srt字幕优化神器')
            logger.info("Successfully switched to Subtitle Optimizer")
            # Assert that the expected UI elements are visible
            self.assertTrue(self.app.notebook.nametowidget(self.app.notebook.select()).winfo_ismapped(), "Subtitle Optimizer frame should be visible")
        except Exception as e:
            logger.error(f"Error switching to Subtitle Optimizer: {e}", exc_info=True)
            self.fail("Failed to switch to Subtitle Optimizer")

    def test_switch_to_standard_mode(self):
        logger.info("Testing switch to Standard Mode")
        try:
            self.app.switch_to_tab('标准模式')
            current_tab = self.app.notebook.tab(self.app.notebook.select(), "text")
            self.assertEqual(current_tab, '标准模式')
            logger.info("Successfully switched to Standard Mode")
            # Assert that the expected UI elements are visible
            self.assertTrue(self.app.standard_mode_frame.winfo_ismapped(), "Standard Mode frame should be visible")
        except Exception as e:
            logger.error(f"Error switching to Standard Mode: {e}", exc_info=True)
            self.fail("Failed to switch to Standard Mode")

if __name__ == '__main__':
    unittest.main()