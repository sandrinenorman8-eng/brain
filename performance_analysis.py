#!/usr/bin/env python3
"""
Analyse des résultats de performance et identification des problèmes
"""

import json
import os

def analyze_performance():
    """Analyser les résultats de performance"""
    
    print("🔍 ANALYSE DES RÉSULTATS DE PERFORMANCE")
    print("=" * 60)
    
    # Charger les résultats
    try:
        with open('detailed_performance_results.json', 'r', encoding='utf-8') as f:
            results = json.load(f)
    except FileNotFoundError:
        print("❌ Fichier de résultats non trouvé")
        return
    
    # Analyser les éléments
    elements = results.get('elements', {})
    print(f"\n📊 ANALYSE DES ÉLÉMENTS:")
    print(f"   • Total éléments DOM: {elements.get('totalElements', 0)}")
    print(f"   • Boutons totaux: {elements.get('buttons', 0)}")
    print(f"   • Boutons catégories: {elements.get('categoryButtons', 0)}")
    print(f"   • Boutons suppression: {elements.get('eraseButtons', 0)}")
    print(f"   • Divs: {elements.get('divs', 0)}")
    
    # Problèmes identifiés
    print(f"\n🚨 PROBLÈMES IDENTIFIÉS:")
    
    total_elements = elements.get('totalElements', 0)
    if total_elements > 200:
        print(f"   ❌ TROP D'ÉLÉMENTS DOM ({total_elements}) - Ralentit le rendu")
    
    buttons = elements.get('buttons', 0)
    if buttons > 50:
        print(f"   ❌ TROP DE BOUTONS ({buttons}) - Ralentit l'interaction")
    
    divs = elements.get('divs', 0)
    if divs > 100:
        print(f"   ❌ TROP DE DIVS ({divs}) - Structure DOM complexe")
    
    # Analyser les performances JavaScript
    js_perf = results.get('js_performance', {})
    print(f"\n⚡ PERFORMANCES JAVASCRIPT:")
    print(f"   • First Paint: {js_perf.get('firstPaint', 0):.0f}ms")
    print(f"   • DOM Content Loaded: {js_perf.get('domContentLoaded', 0):.2f}ms")
    print(f"   • Total Transfer Size: {js_perf.get('totalTransferSize', 0)} bytes")
    
    first_paint = js_perf.get('firstPaint', 0)
    if first_paint > 500:
        print(f"   ❌ FIRST PAINT TROP LENT ({first_paint:.0f}ms) - Devrait être < 500ms")
    
    # Analyser les performances backend
    print(f"\n🔧 PERFORMANCES BACKEND:")
    backend_times = []
    for endpoint in ['/', '/categories', '/all_files']:
        if endpoint in results:
            time_ms = results[endpoint]['response_time'] * 1000
            backend_times.append(time_ms)
            print(f"   • {endpoint}: {time_ms:.0f}ms")
    
    if backend_times:
        avg_backend = sum(backend_times) / len(backend_times)
        if avg_backend > 500:
            print(f"   ❌ BACKEND TROP LENT (moyenne: {avg_backend:.0f}ms) - Devrait être < 500ms")
    
    # Analyser les catégories dupliquées
    categories = elements.get('categories', [])
    category_names = [cat['name'] for cat in categories]
    duplicates = []
    seen = set()
    for name in category_names:
        if name in seen:
            duplicates.append(name)
        seen.add(name)
    
    if duplicates:
        print(f"\n🔄 CATÉGORIES DUPLIQUÉES:")
        for dup in set(duplicates):
            count = category_names.count(dup)
            print(f"   ❌ '{dup}' apparaît {count} fois")
    
    # Recommandations
    print(f"\n💡 RECOMMANDATIONS POUR AMÉLIORER LES PERFORMANCES:")
    
    if total_elements > 200:
        print(f"   1. RÉDUIRE LES ÉLÉMENTS DOM:")
        print(f"      • Supprimer les divs inutiles")
        print(f"      • Simplifier la structure HTML")
        print(f"      • Utiliser des éléments plus légers")
    
    if buttons > 50:
        print(f"   2. OPTIMISER LES BOUTONS:")
        print(f"      • Utiliser la virtualisation pour les listes longues")
        print(f"      • Lazy loading des boutons non visibles")
        print(f"      • Regrouper les boutons similaires")
    
    if duplicates:
        print(f"   3. CORRIGER LES DOUBLONS:")
        print(f"      • Supprimer les catégories dupliquées")
        print(f"      • Nettoyer le fichier categories.json")
    
    if first_paint > 500:
        print(f"   4. AMÉLIORER LE RENDU:")
        print(f"      • Réduire le CSS inline")
        print(f"      • Optimiser les images")
        print(f"      • Minimiser le JavaScript")
    
    if avg_backend > 500:
        print(f"   5. OPTIMISER LE BACKEND:")
        print(f"      • Mettre en cache les réponses")
        print(f"      • Optimiser les requêtes de fichiers")
        print(f"      • Utiliser des réponses asynchrones")
    
    # Score de performance
    score = 100
    if total_elements > 200: score -= 20
    if buttons > 50: score -= 15
    if first_paint > 500: score -= 25
    if avg_backend > 500: score -= 20
    if duplicates: score -= 10
    
    print(f"\n📈 SCORE DE PERFORMANCE: {score}/100")
    if score < 70:
        print(f"   ❌ PERFORMANCE INSUFFISANTE - Optimisations nécessaires")
    elif score < 85:
        print(f"   ⚠️  PERFORMANCE MOYENNE - Améliorations recommandées")
    else:
        print(f"   ✅ PERFORMANCE BONNE")

if __name__ == "__main__":
    analyze_performance()
