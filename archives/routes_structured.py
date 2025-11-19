"""
Hierarchical categories endpoint
"""
from flask import jsonify
import json
import os

def get_categories_structured_handler(load_categories_func):
    """Returns categories with hierarchical structure (parents/children)"""
    try:
        categories = load_categories_func()
        
        # Load mapping
        mapping = {}
        if os.path.exists('category_mapping.json'):
            with open('category_mapping.json', 'r', encoding='utf-8') as f:
                mapping = json.load(f)
        
        # Parent folder definitions
        parent_folders = {
            "buziness": {"emoji": "💼", "color": "#f59e0b"},
            "cinema": {"emoji": "🎬", "color": "#ef4444"},
            "livres": {"emoji": "📚", "color": "#8b5cf6"},
            "logiciels": {"emoji": "💻", "color": "#3b82f6"},
            "series": {"emoji": "📺", "color": "#ec4899"},
            "priorité": {"emoji": "🚀", "color": "#10b981"}
        }
        
        structured = {"parents": [], "standalone": []}
        parent_children = {}
        
        for cat in categories:
            cat_name = cat['name']
            cat_path = mapping.get(cat_name, cat_name)
            
            if '/' in cat_path:
                parent_name = cat_path.split('/')[0]
                if parent_name not in parent_children:
                    parent_info = parent_folders.get(parent_name, {"emoji": "📁", "color": "#6b7280"})
                    parent_children[parent_name] = {
                        "name": parent_name,
                        "emoji": parent_info["emoji"],
                        "color": parent_info["color"],
                        "children": [],
                        "isParent": True
                    }
                parent_children[parent_name]["children"].append({
                    "name": cat_name,
                    "emoji": cat['emoji'],
                    "color": cat['color'],
                    "path": cat_path,
                    "isChild": True
                })
            else:
                structured["standalone"].append({
                    "name": cat_name,
                    "emoji": cat['emoji'],
                    "color": cat['color'],
                    "path": cat_path,
                    "isStandalone": True
                })
        
        structured["parents"] = list(parent_children.values())
        for parent in structured["parents"]:
            parent["children"].sort(key=lambda x: x['name'])
        
        return jsonify(structured)
    except Exception as e:
        print(f"Error in get_categories_structured: {e}")
        return jsonify({"parents": [], "standalone": categories}), 500
