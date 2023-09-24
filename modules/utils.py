import re


def sanitize_filename(filename):
    # Define a regular expression pattern to match invalid characters
    invalid_chars_pattern = r'[\/:*?"<>|\\]|[\r\n]'

    # Replace invalid characters with underscores
    sanitized_filename = re.sub(invalid_chars_pattern, '', filename)

    return sanitized_filename
