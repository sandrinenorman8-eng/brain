# -*- coding: utf-8 -*-
"""
Compte les tokens du fichier fusion globale
"""

import tiktoken

FILE = r"G:\memobrik\deuxieme_cerveau\fusion_global\fusion_globale_2025-11-20_10-14-43.txt"

print("=" * 60)
print("ANALYSE TOKENS - FUSION GLOBALE")
print("=" * 60)

# Charger fichier
with open(FILE, 'r', encoding='utf-8') as f:
    content = f.read()

# Compter
lines = content.count('\n') + 1
chars = len(content)

print(f"\n📄 Fichier: fusion_globale_2025-11-20_10-14-43.txt")
print(f"📏 Lignes: {lines:,}")
print(f"📏 Caractères: {chars:,}")

# Tokens avec différents encodings
encodings = [
    ("gpt-4", "cl100k_base"),
    ("gpt-3.5", "cl100k_base"),
]

for model, enc_name in encodings:
    enc = tiktoken.get_encoding(enc_name)
    tokens = enc.encode(content)
    token_count = len(tokens)
    
    print(f"\n🔢 Tokens ({model}): {token_count:,}")
    print(f"   Ratio chars/tokens: {chars/token_count:.2f}")

# Calculs chunking
print("\n" + "=" * 60)
print("SCENARIOS CHUNKING")
print("=" * 60)

enc = tiktoken.get_encoding("cl100k_base")
total_tokens = len(enc.encode(content))

scenarios = [
    ("Petit", 512, 128),
    ("Moyen", 1500, 300),
    ("Grand", 3000, 300),
    ("Très grand", 5000, 500),
    ("Max Gemini", 7000, 700),
]

for name, chunk_size, overlap in scenarios:
    # Estimation simple
    effective_chunk = chunk_size - overlap
    num_chunks = (total_tokens // effective_chunk) + 1
    
    # Durée estimée (30s par chunk AI)
    duration_min = (num_chunks * 30) / 60
    duration_h = duration_min / 60
    
    print(f"\n{name} ({chunk_size} tokens, overlap {overlap}):")
    print(f"  Chunks estimés: ~{num_chunks}")
    print(f"  Durée: {duration_h:.1f}h ({duration_min:.0f} min)")
    
    if duration_h < 1:
        print(f"  ✅ Acceptable")
    elif duration_h < 2:
        print(f"  ⚠️ Long mais faisable")
    else:
        print(f"  ❌ Trop long")

print("\n" + "=" * 60)
print("RECOMMANDATION")
print("=" * 60)
print("\n🎯 Utiliser: 3000-5000 tokens par chunk")
print("   → ~60-100 chunks")
print("   → ~30-50 minutes")
print("\n💡 Alternative: Traiter par catégorie au lieu de fusion globale")
