# Guide Test Chunking Service - Fichier Réel

## Fichier de Test
**Fichier:** `G:\memobrik\deuxieme_cerveau\fusion_global\fusion_globale_2025-11-20_10-14-43.txt`
- **Lignes:** 11,115
- **Caractères:** 760,144
- **Seuil chunking:** >200 lignes OU >50,000 chars
- **Résultat:** ✅ CHUNKING REQUIS (55x seuil lignes, 15x seuil chars)

---

## Démarrage Rapide

### 1. Démarrer les services
```bash
# Terminal 1 - Tous les services
START_ALL_SERVICES.bat

# OU séparément:
# Terminal 1 - Flask Main
cd deuxieme_cerveau
python app.py

# Terminal 2 - Chunking Service
START_CHUNKING_SERVICE.bat

# Terminal 3 - Search (optionnel)
node search-server.js
```

### 2. Installer dépendances chunking
```bash
pip install -r requirements_chunking.txt
```

### 3. Lancer test automatique
```bash
RUN_CHUNKING_TEST.bat
```

---

## Tests Disponibles

### Test 1: Détection automatique
Vérifie si le fichier nécessite chunking:
```python
python TEST_CHUNKING_LARGE_FILE.py
# Sélectionner: Test détection uniquement
```

**Résultat attendu:**
```
Lignes: 11115 (seuil: 200)
Chars: 760,144 (seuil: 50,000)
Chunking requis: ✅ OUI
```

### Test 2: Comparaison méthodes
Compare les 3 méthodes de chunking:
```python
python TEST_CHUNKING_LARGE_FILE.py
# Sélectionner: Test méthodes chunking
```

**Méthodes testées:**
1. **Semantic** - Frontières naturelles (headers, paragraphes)
2. **Tokens** - Comptage exact avec tiktoken
3. **Smart** - Hybrid (recommandé)

**Résultat attendu:**
```
semantic   |  XX chunks | XXX,XXX tokens | X.XXs
tokens     |  XX chunks | XXX,XXX tokens | X.XXs
smart      |  XX chunks | XXX,XXX tokens | X.XXs
```

### Test 3: Organisation AI complète
Test complet avec appel Gemini AI:
```python
python TEST_CHUNKING_LARGE_FILE.py
# Sélectionner: y pour test AI
```

**⚠️ Attention:**
- Appelle API Gemini (coût possible)
- Durée: 5-15 minutes selon taille
- Timeout: 10 minutes max

**Résultat attendu:**
- Fichier organisé en markdown structuré
- Sauvegardé dans `TEST_CHUNKING_OUTPUT.md`
- Stats: chunks traités, tokens, durée

### Test 4: Via route Flask (auto-détection)
Test l'intégration complète avec Flask:
```python
python TEST_CHUNKING_LARGE_FILE.py
# Sélectionner: y pour test Flask
```

**Flow:**
1. Flask reçoit requête `/ai/organize`
2. Détecte fichier >200 lignes
3. Redirige automatiquement vers chunking service (port 5009)
4. Chunking service traite avec méthode smart
5. Résultat sauvegardé dans `data/ai fusion/`

---

## Architecture du Test

```
┌─────────────────────────────────────────────────────────┐
│  TEST_CHUNKING_LARGE_FILE.py                            │
│  ┌───────────────────────────────────────────────────┐  │
│  │ 1. Check Services (5008, 5009)                    │  │
│  │ 2. Load File (11,115 lignes)                      │  │
│  │ 3. Test Detection (>200 lignes?)                  │  │
│  │ 4. Test Chunking Methods (semantic/tokens/smart)  │  │
│  │ 5. Test AI Organization (Gemini)                  │  │
│  │ 6. Test Flask Route (auto-detection)              │  │
│  └───────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
        ┌─────────────────────────────────┐
        │  Chunking Service (Port 5009)   │
        │  ┌───────────────────────────┐  │
        │  │ /detect                   │  │
        │  │ /chunk                    │  │
        │  │ /organize_large           │  │
        │  └───────────────────────────┘  │
        └─────────────────────────────────┘
                          │
                          ▼
        ┌─────────────────────────────────┐
        │  AI Service (Gemini)            │
        │  ┌───────────────────────────┐  │
        │  │ organize_fusion()         │  │
        │  │ _organize_chunk()         │  │
        │  └───────────────────────────┘  │
        └─────────────────────────────────┘
```

---

## Résultats Attendus

### Chunking Smart (Recommandé)
Pour fichier 760k chars:
- **Chunks:** ~150-200 chunks
- **Tokens/chunk:** ~512 tokens
- **Overlap:** 128 tokens (25%)
- **Durée chunking:** <5 secondes
- **Durée AI totale:** 5-15 minutes

### Organisation AI
Structure markdown générée:
```markdown
# TEST FUSION GLOBALE - Synthèse Complète

## Partie 1/150

# Titre Projet 1
## 📝 Extrait original
...
## 📊 Vue d'ensemble
...
## ⭐ Idées principales
...

## Partie 2/150
...
```

---

## Troubleshooting

### Erreur: Service 5009 DOWN
```bash
# Vérifier port
netstat -an | findstr :5009

# Démarrer service
START_CHUNKING_SERVICE.bat

# Vérifier logs
type deuxieme_cerveau\logs\chunking_error.log
```

### Erreur: Timeout AI
```python
# Augmenter timeout dans TEST_CHUNKING_LARGE_FILE.py
timeout=600  # 10 min → 1200 (20 min)
```

### Erreur: tiktoken not found
```bash
pip install tiktoken==0.5.2
```

### Erreur: Gemini API
```python
# Vérifier clé API dans ai_service.py
GEMINI_API_KEY = "AIzaSyAUDVRdWDVxamiqtCsqEvdMUaVuIs81il8"
```

---

## Commandes Manuelles

### Test détection seule
```bash
curl -X POST http://localhost:5009/detect ^
  -H "Content-Type: application/json" ^
  -d "{\"content\": \"test\", \"line_threshold\": 200}"
```

### Test chunking seul
```bash
curl -X POST http://localhost:5009/chunk ^
  -H "Content-Type: application/json" ^
  -d "{\"content\": \"test\", \"method\": \"smart\"}"
```

### Test health
```bash
curl http://localhost:5009/health
curl http://localhost:5009/status
```

---

## Métriques de Succès

✅ **Détection:** Fichier correctement identifié comme nécessitant chunking
✅ **Chunking:** Chunks créés avec overlap préservé
✅ **Tokens:** Comptage précis avec tiktoken
✅ **AI:** Organisation complète sans erreur
✅ **Performance:** <30s par chunk AI
✅ **Intégration:** Auto-détection Flask fonctionne
✅ **Fallback:** Méthode normale si service down

---

## Prochaines Étapes

Après validation du test:

1. **Production:** Déployer avec Gunicorn
   ```bash
   gunicorn -c deuxieme_cerveau/gunicorn_config.py deuxieme_cerveau.chunking_service:app
   ```

2. **Monitoring:** Ajouter logs détaillés
3. **Optimisation:** Cache Redis pour chunks
4. **UI:** Indicateur chunking dans frontend
5. **Documentation:** Mise à jour docs techniques

---

**Durée test complète:** 15-20 minutes  
**Prérequis:** Flask + Chunking Service + Gemini API  
**Objectif:** Valider chunking intelligent sur fichier réel 11k lignes
