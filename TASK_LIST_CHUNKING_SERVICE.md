# Task List: Smart Chunking Service Implementation

## Objectif
Créer un service Python dédié (port 5009) qui détecte automatiquement les fichiers >200 lignes et applique le chunking intelligent avec LLM streaming.

---

## Phase 1: Infrastructure de Base

### Task 1.1: Créer le service chunking dédié
- [ ] Créer `deuxieme_cerveau/chunking_service.py`
- [ ] Flask app sur port 5009
- [ ] Routes: `/chunk`, `/status`, `/health`
- [ ] Intégration avec ai_service existant

### Task 1.2: Installer dépendances
- [ ] Créer `requirements_chunking.txt`:
  - `tiktoken==0.5.2`
  - `flask==3.0.0`
  - `flask-cors==4.0.0`
  - `gunicorn==21.2.0`
  - `google-generativeai` (déjà présent)

### Task 1.3: Configuration Gunicorn
- [ ] Créer `gunicorn_config.py`
- [ ] Config: 4 workers, 2 threads
- [ ] Timeout adapté pour LLM (300s)
- [ ] Logging structuré

---

## Phase 2: Implémentation Chunking

### Task 2.1: Module de chunking sémantique
- [ ] Créer `deuxieme_cerveau/services/chunking_service.py`
- [ ] Fonction `chunk_by_semantic_boundary()`
- [ ] Fonction `chunk_by_tokens()` avec tiktoken
- [ ] Fonction `chunk_smart()` (hybrid)

### Task 2.2: Détection automatique
- [ ] Middleware Flask pour détecter taille fichier
- [ ] Seuil: 200 lignes OU 50,000 chars
- [ ] Redirection automatique vers chunking service

### Task 2.3: Streaming LLM
- [ ] Adapter `ai_service.py` pour streaming
- [ ] Classe `LLMChunkProcessor`
- [ ] Context carryover entre chunks
- [ ] Progress tracking

---

## Phase 3: Intégration avec AI Routes

### Task 3.1: Modifier ai_routes.py
- [ ] Ajouter route `/organize_large` 
- [ ] Détection automatique taille
- [ ] Appel au chunking service si >200 lignes
- [ ] Fallback sur méthode actuelle si <200 lignes

### Task 3.2: Mise à jour ai_service.py
- [ ] Remplacer `_chunk_content()` par chunking sémantique
- [ ] Intégrer tiktoken pour comptage tokens
- [ ] Overlap configurable (20-50%)
- [ ] Metadata tracking par chunk

---

## Phase 4: Scripts de Démarrage

### Task 4.1: Script Windows
- [ ] Créer `START_CHUNKING_SERVICE.bat`:
```batch
@echo off
cd /d "%~dp0deuxieme_cerveau"
gunicorn -c gunicorn_config.py chunking_service:app
```

### Task 4.2: Intégration START.bat
- [ ] Modifier `START.bat` pour lancer 3 services:
  - Flask main (5008)
  - Node search (3008)
  - Chunking service (5009)

### Task 4.3: Script STOP
- [ ] Créer `STOP_CHUNKING_SERVICE.bat`
- [ ] Intégrer dans `STOP.bat` global

---

## Phase 5: Frontend Integration

### Task 5.1: Indicateur de chunking
- [ ] Badge UI "Fichier volumineux détecté"
- [ ] Progress bar pour chunks traités
- [ ] Affichage: "Chunk 3/7 en cours..."

### Task 5.2: Mise à jour fusion_intelligente.html
- [ ] Détection côté client (ligne count)
- [ ] Appel automatique `/organize_large`
- [ ] Streaming display des chunks

---

## Phase 6: Optimisations

### Task 6.1: Caching
- [ ] Cache Redis optionnel pour chunks
- [ ] LRU cache pour tokens encoding
- [ ] Invalidation intelligente

### Task 6.2: Monitoring
- [ ] Endpoint `/metrics` (chunks/sec, tokens/sec)
- [ ] Logging des performances
- [ ] Alertes si timeout

### Task 6.3: Error Handling
- [ ] Retry automatique par chunk
- [ ] Fallback sur chunks plus petits
- [ ] Sauvegarde partielle si échec

---

## Phase 7: Testing

### Task 7.1: Tests unitaires
- [ ] Test chunking sémantique
- [ ] Test token counting
- [ ] Test overlap preservation

### Task 7.2: Tests d'intégration
- [ ] Fichier 500 lignes → chunking auto
- [ ] Fichier 150 lignes → méthode normale
- [ ] Streaming end-to-end

### Task 7.3: Tests de charge
- [ ] 10 fichiers simultanés
- [ ] Fichier 10,000 lignes
- [ ] Mesure latence/throughput

---

## Phase 8: Documentation

### Task 8.1: Mise à jour docs
- [ ] Ajouter chunking service dans `structure.md`
- [ ] Documenter endpoints dans `tech.md`
- [ ] Guide utilisation dans README

### Task 8.2: Configuration
- [ ] Variables d'environnement
- [ ] Paramètres de chunking (taille, overlap)
- [ ] Seuils de détection

---

## Priorités d'Implémentation

### 🔴 Critique (Semaine 1)
- Task 1.1, 1.2, 2.1, 2.2, 3.1, 4.1, 4.2

### 🟡 Important (Semaine 2)
- Task 2.3, 3.2, 5.1, 5.2, 7.2

### 🟢 Nice-to-have (Semaine 3+)
- Task 6.1, 6.2, 6.3, 7.1, 7.3, 8.1, 8.2

---

## Commandes Rapides

### Démarrage production
```bash
# Terminal 1 - Main Flask
gunicorn -w 4 --threads 2 -b 0.0.0.0:5008 app:app

# Terminal 2 - Chunking Service
cd deuxieme_cerveau
gunicorn -c gunicorn_config.py chunking_service:app

# Terminal 3 - Search
node search-server.js
```

### Test rapide
```bash
# Test chunking
python -c "from services.chunking_service import chunk_smart; print(len(chunk_smart(open('test.txt').read())))"

# Test service
curl http://localhost:5009/health
```

---

## Métriques de Succès

- ✅ Fichiers >200 lignes traités automatiquement
- ✅ Temps traitement <30s par chunk
- ✅ Aucune perte de contexte entre chunks
- ✅ 0 downtime sur service principal
- ✅ Streaming fluide côté frontend

---

**Estimation totale:** 3-4 semaines  
**Complexité:** Moyenne-Haute  
**Impact:** Très élevé (scalabilité × 10)
