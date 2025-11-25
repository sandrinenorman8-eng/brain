import os
import json
import random
import shutil
from functools import lru_cache
from config.config import Config
from category_path_resolver import get_absolute_category_path

@lru_cache(maxsize=1)
def load_categories():
    if not os.path.exists(Config.CATEGORIES_FILE):
        default_categories = [
            {"name": "scénario", "emoji": "🎬", "color": "#FF6B6B"},
            {"name": "actualité", "emoji": "🗞", "color": "#4ECDC4"},
            {"name": "idées", "emoji": "💡", "color": "#45B7D1"},
            {"name": "projets", "emoji": "🏗", "color": "#FFA94D"},
            {"name": "recherche", "emoji": "🔍", "color": "#6A4C93"},
            {"name": "todo", "emoji": "✅", "color": "#10B981"}
        ]
        save_categories(default_categories)
        return default_categories
    
    try:
        with open(Config.CATEGORIES_FILE, "r", encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return []

def save_categories(categories):
    with open(Config.CATEGORIES_FILE, "w", encoding='utf-8') as f:
        json.dump(categories, f, indent=2, ensure_ascii=False)
    load_categories.cache_clear()

def add_category(name, emoji=None, color=None):
    name = name.strip().lower()
    
    if not name:
        raise ValueError("Category name cannot be empty")
    
    if len(name) > 19:
        raise ValueError(f"Category name cannot exceed 19 characters ({len(name)}/19)")
    
    categories = load_categories()
    
    if any(c['name'] == name for c in categories):
        raise ValueError("Category already exists")
    
    if emoji is None:
        emoji = random.choice(Config.EMOJIS)
    
    if color is None:
        color = f"#{random.randint(0, 0xFFFFFF):06x}"
    
    new_category = {"name": name, "emoji": emoji, "color": color}
    categories.append(new_category)
    save_categories(categories)
    
    return new_category

def delete_category(name):
    categories = load_categories()
    
    if not any(c['name'] == name for c in categories):
        raise ValueError("Category not found")
    
    folder_path = get_absolute_category_path(name)
    
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)
    
    updated_categories = [c for c in categories if c['name'] != name]
    save_categories(updated_categories)
    
    return True

def get_category_info(name):
    categories = load_categories()
    return next((c for c in categories if c['name'] == name), None)
