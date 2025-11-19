import os
from datetime import datetime
from category_path_resolver import get_category_path
from utils.file_utils import safe_read
from services.notes_service import get_all_files

def fusion_global():
    fusion_dir = "fusion_global"
    os.makedirs(fusion_dir, exist_ok=True)
    
    all_files_data = get_all_files()
    all_files_data.sort(key=lambda x: (x['date'], x.get('hour', '00:00:00')), reverse=True)
    
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    fusion_filename = f"fusion_globale_{timestamp}.txt"
    fusion_filepath = os.path.join(fusion_dir, fusion_filename)
    
    with open(fusion_filepath, 'w', encoding='utf-8') as fusion_file:
        fusion_file.write("=" * 80 + "\n")
        fusion_file.write("🔗 FUSION GLOBALE DE TOUTES LES NOTES\n")
        fusion_file.write("=" * 80 + "\n")
        fusion_file.write(f"📅 Date de fusion: {datetime.now().strftime('%d/%m/%Y à %H:%M:%S')}\n")
        fusion_file.write(f"📊 Nombre total de fichiers: {len(all_files_data)}\n")
        fusion_file.write("=" * 80 + "\n\n")
        
        current_category = None
        for file_data in all_files_data:
            category_name = file_data['category']
            filename = file_data['filename']
            file_date = file_data['date']
            
            if current_category != category_name:
                if current_category is not None:
                    fusion_file.write("\n" + "=" * 80 + "\n\n")
                fusion_file.write(f"📁 CATÉGORIE: {category_name.upper()}\n")
                fusion_file.write("-" * 40 + "\n\n")
                current_category = category_name
            
            category_path = get_category_path(category_name)
            filepath = os.path.join(category_path, filename)
            if os.path.exists(filepath):
                try:
                    content = safe_read(filepath)
                    if content.strip():
                        fusion_file.write(f"📄 {filename} ({file_date})\n")
                        fusion_file.write("-" * 30 + "\n")
                        fusion_file.write(content.strip())
                        fusion_file.write("\n\n")
                except Exception as e:
                    print(f"Error reading {filepath}: {e}")
                    fusion_file.write(f"❌ Error reading {filename}\n\n")
    
    return {
        "filename": fusion_filename,
        "filepath": fusion_filepath,
        "total_files": len(all_files_data)
    }

def fusion_by_category(selected_categories):
    if not selected_categories:
        raise ValueError("No categories selected")
    
    fusion_dir = "fusion_categories"
    os.makedirs(fusion_dir, exist_ok=True)
    
    all_files_data = get_all_files()
    filtered_files = [f for f in all_files_data if f['category'] in selected_categories]
    
    if not filtered_files:
        raise ValueError("No files found in selected categories")
    
    filtered_files.sort(key=lambda x: (x['date'], x.get('hour', '00:00:00')), reverse=True)
    
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    categories_str = "_".join(selected_categories[:3])
    if len(selected_categories) > 3:
        categories_str += f"_et_{len(selected_categories)-3}_autres"
    fusion_filename = f"fusion_categories_{categories_str}_{timestamp}.txt"
    fusion_filepath = os.path.join(fusion_dir, fusion_filename)
    
    with open(fusion_filepath, 'w', encoding='utf-8') as fusion_file:
        fusion_file.write("=" * 80 + "\n")
        fusion_file.write("📁 FUSION PAR CATÉGORIES\n")
        fusion_file.write("=" * 80 + "\n")
        fusion_file.write(f"📅 Date de fusion: {datetime.now().strftime('%d/%m/%Y à %H:%M:%S')}\n")
        fusion_file.write(f"📊 Catégories sélectionnées: {', '.join(selected_categories)}\n")
        fusion_file.write(f"📊 Nombre total de fichiers: {len(filtered_files)}\n")
        fusion_file.write("=" * 80 + "\n\n")
        
        current_category = None
        for file_data in filtered_files:
            category_name = file_data['category']
            filename = file_data['filename']
            file_date = file_data['date']
            
            if current_category != category_name:
                if current_category is not None:
                    fusion_file.write("\n" + "=" * 80 + "\n\n")
                fusion_file.write(f"📁 CATÉGORIE: {category_name.upper()}\n")
                fusion_file.write("-" * 40 + "\n\n")
                current_category = category_name
            
            category_path = get_category_path(category_name)
            filepath = os.path.join(category_path, filename)
            if os.path.exists(filepath):
                try:
                    content = safe_read(filepath)
                    if content.strip():
                        fusion_file.write(f"📄 {filename} ({file_date})\n")
                        fusion_file.write("-" * 30 + "\n")
                        fusion_file.write(content.strip())
                        fusion_file.write("\n\n")
                except Exception as e:
                    print(f"Error reading {filepath}: {e}")
                    fusion_file.write(f"❌ Error reading {filename}\n\n")
    
    return {
        "filename": fusion_filename,
        "filepath": fusion_filepath,
        "categories": selected_categories,
        "total_files": len(filtered_files)
    }

def fusion_single_category(category_name):
    if not category_name:
        raise ValueError("Category name is required")
    
    fusion_dir = "fusion_categories"
    os.makedirs(fusion_dir, exist_ok=True)
    
    all_files_data = get_all_files()
    category_files = [f for f in all_files_data if f['category'] == category_name]
    
    if not category_files:
        raise ValueError(f"No files found in category '{category_name}'")
    
    category_files.sort(key=lambda x: (x['date'], x.get('hour', '00:00:00')), reverse=True)
    
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    fusion_filename = f"fusion_{category_name}_{timestamp}.txt"
    fusion_filepath = os.path.join(fusion_dir, fusion_filename)
    
    with open(fusion_filepath, 'w', encoding='utf-8') as fusion_file:
        fusion_file.write("=" * 80 + "\n")
        fusion_file.write(f"📁 FUSION DE LA CATÉGORIE: {category_name.upper()}\n")
        fusion_file.write("=" * 80 + "\n")
        fusion_file.write(f"📅 Date de fusion: {datetime.now().strftime('%d/%m/%Y à %H:%M:%S')}\n")
        fusion_file.write(f"📊 Catégorie: {category_name}\n")
        fusion_file.write(f"📊 Nombre total de fichiers: {len(category_files)}\n")
        fusion_file.write("=" * 80 + "\n\n")
        
        for file_data in category_files:
            filename = file_data['filename']
            file_date = file_data['date']
            
            category_path = get_category_path(category_name)
            filepath = os.path.join(category_path, filename)
            if os.path.exists(filepath):
                try:
                    content = safe_read(filepath)
                    if content.strip():
                        fusion_file.write(f"📄 {filename} ({file_date})\n")
                        fusion_file.write("-" * 30 + "\n")
                        fusion_file.write(content.strip())
                        fusion_file.write("\n\n")
                except Exception as e:
                    print(f"Error reading {filepath}: {e}")
                    fusion_file.write(f"❌ Error reading {filename}\n\n")
    
    return {
        "filename": fusion_filename,
        "filepath": fusion_filepath,
        "category": category_name,
        "total_files": len(category_files)
    }
