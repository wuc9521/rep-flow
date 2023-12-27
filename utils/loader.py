import re
from flask import Flask

def read_keywords_from_file(file_path, app: Flask = None):
    try:
        with open(file_path, 'r') as file:
            content = file.read()
            keywords_list = [keyword.strip() for keyword in re.split(',|\n', content) if keyword.strip()]
            app.logger.info(f"Keywords loaded: {keywords_list}")
            return keywords_list

    except FileNotFoundError:
        app.logger.info(f"Error: File '{file_path}' not found.")
        return []

