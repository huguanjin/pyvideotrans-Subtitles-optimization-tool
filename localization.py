# localization.py

translations = {
    'en': {
        'Import SRT File': 'Import SRT File',
        'Translate Subtitles': 'Translate Subtitles',
        'Export SRT File': 'Export SRT File',
        'Translation Progress: 0%': 'Translation Progress: 0%',
        'File Imported': 'File Imported',
        'File Exported': 'File Exported',
        'No File Imported': 'No File Imported',
        'Translation Complete': 'Translation Complete',
        'Translation Error': 'Translation Error',
        'Input': 'Input',
        'Enter the target language code (e.g., \'en\' for English):': 'Enter the target language code (e.g., \'en\' for English):',
        'Save Edits': 'Save Edits',
        'Edits Saved': 'Edits Saved',
        'Your edits have been saved.': 'Your edits have been saved.',
        'Upload SRT Files': 'Upload SRT Files',
        'Select Output Path': 'Select Output Path',
        'Remove Punctuation': 'Remove Punctuation',
        'Files Uploaded': 'Files Uploaded',
        'Output Path Selected': 'Output Path Selected',
        'Processing Complete': 'Processing Complete',
        'Processing completed successfully.': 'Processing completed successfully.',
        'Error': 'Error',
        'No files uploaded for processing.': 'No files uploaded for processing.',
        'No output path selected.': 'No output path selected.',
        'An error occurred while processing the file': 'An error occurred while processing the file'
    },
    'zh': {
        'Import SRT File': '导入SRT文件',
        'Translate Subtitles': '翻译字幕',
        'Export SRT File': '导出SRT文件',
        'Translation Progress: 0%': '翻译进度: 0%',
        'File Imported': '文件已导入',
        'File Exported': '文件已导出',
        'No File Imported': '未导入文件',
        'Translation Complete': '翻译完成',
        'Translation Error': '翻译错误',
        'Input': '输入',
        'Enter the target language code (e.g., \'en\' for English):': '输入目标语言代码（例如，\'en\'表示英语）:',
        'Save Edits': '保存编辑',
        'Edits Saved': '编辑已保存',
        'Your edits have been saved.': '您的编辑已保存。',
        'Upload SRT Files': '上传SRT文件',
        'Select Output Path': '选择输出路径',
        'Remove Punctuation': '去除标点符号',
        'Files Uploaded': '文件已上传',
        'Output Path Selected': '输出路径已选择',
        'Processing Complete': '处理完成',
        'Processing completed successfully.': '处理成功完成。',
        'Error': '错误',
        'No files uploaded for processing.': '没有文件上传进行处理。',
        'No output path selected.': '未选择输出路径。',
        'An error occurred while processing the file': '处理文件时发生错误'
    }
}

def get_translation(key, language='en'):
    return translations.get(language, {}).get(key, key)