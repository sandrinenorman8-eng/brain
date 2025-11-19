import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    FLASK_DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    PORT = int(os.getenv('PORT', 5008))
    NOTES_DIR = os.getenv('NOTES_DIR', 'data')
    SEARCH_URL = os.getenv('SEARCH_URL', 'http://localhost:3008')
    CATEGORIES_FILE = os.getenv('CATEGORIES_FILE', 'categories.json')
    CATEGORY_MAPPING_FILE = os.getenv('CATEGORY_MAPPING_FILE', 'category_mapping.json')
    HOST = '0.0.0.0'
    
    EMOJIS = ["📁", "📄", "📝", "💡", "🚀", "🌟", "📚", "📌", "⚙️", "✅", "🎯", "🔧", "📊", "🎨", "🔍", "💼", "📈", "🎪", "🔮", "⭐"]
