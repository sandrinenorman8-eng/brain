import os
import json
from pathlib import Path

SEARCH_EXTENSIONS = ['.txt', '.md', '.html']

def search_in_file(file_path, search_term):
    """Search for term in a file and return matches with excerpts"""
    try:
        # Try multiple encodings
        for encoding in ['utf-8', 'cp1252', 'latin-1', 'iso-8859-1']:
            try:
                with open(file_path, 'r', encoding=encoding) as f:
                    content = f.read()
                break
            except UnicodeDecodeError:
                continue
        else:
            return []
        
        lines = content.split('\n')
        matches = []
        search_lower = search_term.lower()
        
        for index, line in enumerate(lines):
            line_lower = line.lower()
            if search_lower in line_lower:
                # Extract excerpt around match
                match_pos = line_lower.index(search_lower)
                start = max(0, match_pos - 50)
                end = min(len(line), match_pos + len(search_term) + 50)
                excerpt = line[start:end]
                
                if start > 0:
                    excerpt = '...' + excerpt
                if end < len(line):
                    excerpt = excerpt + '...'
                
                matches.append({
                    'line_number': index + 1,
                    'text': excerpt,
                    'match_number': len(matches) + 1
                })
        
        return matches
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return []

def search_in_category(category_path, category_name, search_term):
    """Search in all files of a category"""
    results = []
    
    if not os.path.exists(category_path):
        return results
    
    try:
        for filename in os.listdir(category_path):
            file_path = os.path.join(category_path, filename)
            file_ext = os.path.splitext(filename)[1]
            
            if file_ext in SEARCH_EXTENSIONS and os.path.isfile(file_path):
                matches = search_in_file(file_path, search_term)
                
                if matches:
                    # Extract date from filename
                    import re
                    date_match = re.search(r'(\d{4}-\d{2}-\d{2})', filename)
                    file_date = date_match.group(1) if date_match else ''
                    
                    results.append({
                        'category': category_name,
                        'filename': filename,
                        'date': file_date,
                        'match_count': len(matches),
                        'excerpts': matches[:3]  # First 3 matches
                    })
    except Exception as e:
        print(f"Error searching in {category_name}: {e}")
    
    return results

def search_content(search_term):
    """Main search function - searches across all categories"""
    if not search_term or not search_term.strip():
        raise ValueError("Search term cannot be empty")
    
    if len(search_term) < 2:
        return {'results': [], 'message': 'Search term too short'}
    
    # Load categories
    try:
        with open('categories.json', 'r', encoding='utf-8') as f:
            categories = json.load(f)
    except Exception as e:
        raise Exception(f"Failed to load categories: {e}")
    
    all_results = []
    data_dir = 'data'
    
    # Search in each category
    for category in categories:
        category_name = category['name']
        category_path = os.path.join(data_dir, category_name)
        
        category_results = search_in_category(category_path, category_name, search_term)
        all_results.extend(category_results)
    
    return {
        'results': all_results,
        'message': f"{len(all_results)} file(s) found"
    }
