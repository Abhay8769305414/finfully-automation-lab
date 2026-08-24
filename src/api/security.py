import os
import re

def sanitize_filename(filename: str) -> str:
    """Path traversal protection."""
    cleaned = os.path.basename(filename)
    cleaned = re.sub(r'[^\w\.-]', '_', cleaned)
    return cleaned
