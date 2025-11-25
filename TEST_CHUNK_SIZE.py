# -*- coding: utf-8 -*-
"""
Test rapide pour vérifier le nombre de chunks
"""

import sys
sys.path.insert(0, 'deuxieme_cerveau')

from services.chunking_service import ChunkingService

TEST_FILE = r"G:\memobrik\deuxieme_cerveau\fusion_global\fusion_globale_2025-11-20_10-14-43.txt"

print("=" * 60)
print("TEST TAILLE CHUNKS")
print("=" * 60)

with open(TEST_FILE, 'r', encoding='utf-8') as f:
    content = f.read()

print(f"\nFichier: {len(content):,} caractères")

chunker = ChunkingService()

# Test différentes tailles
configs = [
    ("Petit (512 tokens)", 512, 128),
    ("Moyen (1500 tokens)", 1500, 300),
    ("Grand (3000 tokens)", 3000, 300),
    ("Très grand (5000 tokens)", 5000, 500),
]

for name, tokens, overlap in configs:
    chunks = chunker.chunk_smart(content, chunk_tokens=tokens, overlap_tokens=overlap)
    stats = chunker.get_chunking_stats(chunks)
    
    duration_estimate = len(chunks) * 30  # 30s par chunk
    hours = duration_estimate / 3600
    
    print(f"\n{name}:")
    print(f"  Chunks: {len(chunks)}")
    print(f"  Avg tokens/chunk: {stats['avg_tokens_per_chunk']}")
    print(f"  Durée estimée: {hours:.1f}h ({duration_estimate/60:.0f} min)")

print("\n" + "=" * 60)
print("RECOMMANDATION: 3000 tokens = ~60-80 chunks = ~30-40 min")
print("=" * 60)
