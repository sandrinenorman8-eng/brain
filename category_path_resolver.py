"""
Module pour résoudre les chemins des catégories avec mapping hiérarchique
"""
import os
import json

def get_category_path(category_name):
    """
    Résout le chemin d'une catégorie en utilisant le mapping.
    
    Args:
        category_name: Nom de la catégorie (ex: "scénario", "todo")
    
    Returns:
        Chemin complet vers le dossier de la catégorie
    """
    # Charger le mapping
    mapping = {}
    mapping_file = 'category_mapping.json'
    
    if os.path.exists(mapping_file):
        with open(mapping_file, 'r', encoding='utf-8') as f:
            mapping = json.load(f)
    
    # Obtenir le chemin mappé (ex: "cinema/scénario" ou "scénario")
    mapped_path = mapping.get(category_name, category_name)
    
    # Construire le chemin complet
    full_path = os.path.join('data', mapped_path)
    
    return full_path

def get_absolute_category_path(category_name):
    """
    Résout le chemin absolu d'une catégorie.
    
    Args:
        category_name: Nom de la catégorie
    
    Returns:
        Chemin absolu vers le dossier de la catégorie
    """
    relative_path = get_category_path(category_name)
    return os.path.join(os.getcwd(), relative_path)
