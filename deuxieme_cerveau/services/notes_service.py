import os
from datetime import datetime
from functools import lru_cache
from category_path_resolver import get_category_path
from utils.file_utils import safe_read, safe_category_read
from services.category_service import load_categories

def save_note(category, text):
    if not text or not text.strip():
        raise ValueError("Note text cannot be empty")
    
    category_path = get_category_path(category)
    os.makedirs(category_path, exist_ok=True)
    
    date_str = datetime.now().strftime("%Y-%m-%d")
    filename = os.path.join(category_path, f"{category}_{date_str}.txt")
    
    with open(filename, "a", encoding='utf-8') as f:
        time_str = datetime.now().strftime("%H:%M:%S")
        f.write(f"{time_str}: {text}\n")
    
    _get_all_files_cached.cache_clear()
    
    return filename

def list_notes(category):
    category_path = get_category_path(category)
    
    if not os.path.exists(category_path):
        return []
    
    files = [f for f in os.listdir(category_path)
            if f.startswith(f'{category}_') and f.endswith('.txt')]
    files.sort(reverse=True)
    
    return files

def read_note(category, filename):
    content = safe_category_read(category, filename)
    return content

def extract_file_creation_hour(category_name, filename):
    try:
        category_path = get_category_path(category_name)
        filepath = os.path.join(category_path, filename)
        
        if not os.path.exists(filepath):
            return None
        
        content = safe_read(filepath)
        lines = content.splitlines()
        
        hours = []
        for line in lines:
            line = line.strip()
            if line and ':' in line:
                parts = line.split(':')
                if len(parts) >= 3:
                    try:
                        hour = int(parts[0])
                        minute = int(parts[1])
                        second = int(parts[2])
                        
                        if 0 <= hour <= 23 and 0 <= minute <= 59 and 0 <= second <= 59:
                            hour_str = f"{hour:02d}:{minute:02d}:{second:02d}"
                            hours.append(hour_str)
                    except ValueError:
                        continue
        
        if hours:
            hours.sort(reverse=True)
            return hours[0]
        
        return None
    except Exception as e:
        print(f"Error extracting hour from {filename}: {e}")
        return None

@lru_cache(maxsize=1)
def _get_all_files_cached():
    categories = load_categories()
    all_files_data = []
    
    for cat in categories:
        category_path = get_category_path(cat['name'])
        if os.path.exists(category_path):
            files = [f for f in os.listdir(category_path)
                    if f.startswith(f"{cat['name']}_") and f.endswith('.txt')]
            for file in files:
                file_hour = extract_file_creation_hour(cat['name'], file)
                
                all_files_data.append({
                    'category': cat['name'],
                    'emoji': cat['emoji'],
                    'color': cat['color'],
                    'filename': file,
                    'date': file.replace(f"{cat['name']}_", '').replace('.txt', ''),
                    'hour': file_hour or '00:00:00'
                })
    
    all_files_data.sort(key=lambda x: (x['date'], x['hour']), reverse=True)
    return all_files_data

def get_all_files():
    return _get_all_files_cached()
