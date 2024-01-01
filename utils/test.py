import re

def extract_and_validate_test_number(query_text, app):
    """
    refer to: https://regex101.com/r/x609CD/1
    """
    match = re.match(r'\/?test (\d+)$', query_text)
    app.logger.info(f"query_text: {query_text}")
    if match:
        test_number = match.group(1)
        if test_number.isdigit():
            return test_number
    return None

