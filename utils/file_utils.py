import os
import shutil
from datetime import datetime
from category_path_resolver import get_category_path, get_absolute_category_path

def safe_read(filepath, encodings=None):
    if encodings is None:
        encodings = ['utf-8', 'cp1252', 'latin-1', 'iso-8859-1']
    
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")
    
    for encoding in encodings:
        try:
            with open(filepath, 'r', encoding=encoding) as f:
                return f.read()
        except UnicodeDecodeError:
            continue
    
    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
        return f.read()

def safe_write(filepath, content, create_backup=True):
    if create_backup and os.path.exists(filepath):
        backup_path = f"{filepath}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        shutil.copy2(filepath, backup_path)
    
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

def validate_path(filepath, base_dir):
    abs_filepath = os.path.abspath(filepath)
    abs_base_dir = os.path.abspath(base_dir)
    
    if not abs_filepath.startswith(abs_base_dir):
        raise ValueError(f"Path traversal detected: {filepath}")
    
    return abs_filepath

def safe_category_read(category, filename):
    category_dir = get_absolute_category_path(category)
    filepath = os.path.join(category_dir, filename)
    
    validate_path(filepath, category_dir)
    
    return safe_read(filepath)

def safe_category_write(category, filename, content, create_backup=True):
    category_dir = get_absolute_category_path(category)
    filepath = os.path.join(category_dir, filename)
    
    validate_path(filepath, category_dir)
    
    safe_write(filepath, content, create_backup)
