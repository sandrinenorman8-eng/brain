# Plan d'Intégration Documind RAG

## Analyse Technique

### Documind (Source)
- **Stack**: React 19 + TypeScript + Vite
- **AI**: Google Gemini (Flash 2.5 + Pro 3)
- **Features**: 
  - Upload PDF/TXT/MD
  - RAG multi-phase (6 phases orchestration)
  - Segmentation intelligente (tri-layer)
  - Workflow stages (Analyse → Smart → Insanity)
  - Artifacts + History
  - Streaming responses

### Deuxième Cerveau (Target)
- **Stack**: Flask + Vanilla JS
- **AI Actuel**: Kimi AI (fusion_intelligente)
- **Features**: Notes hiérarchiques, fusion catégories

## Stratégies d'Intégration

### Option 1: Backend Python Pur (RECOMMANDÉ)
**Avantages**: Cohérence stack, pas de Node.js
**Implémentation**:
```python
# services/documind_service.py
import google.generativeai as genai
from typing import List, Dict
import json

class DocumindService:
    def __init__(self):
        genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
        self.flash_model = genai.GenerativeModel('gemini-2.5-flash')
        self.pro_model = genai.GenerativeModel('gemini-3-pro-preview')
    
    def segment_content(self, text: str, chunk_size: int = 4000) -> str:
        """Tri-layer segmentation"""
        # Layer 1: Metadata scan
        # Layer 2: Recursive split
        # Layer 3: Context injection
        pass
    
    def orchestrate_analysis(self, content: str, callbacks: dict):
        """6-phase orchestration"""
        phases = [
            self._phase_1_decomposition,
            self._phase_2_scouting,
            self._phase_3_extraction,
            self._phase_4_synthesis,
            self._phase_5_verification,
            self._phase_6_final
        ]
        for phase in phases:
            yield from phase(content, callbacks)
```

### Option 2: Microservice Node.js
**Avantages**: Réutilise code Documind
**Implémentation**:
```javascript
// documind_service/server.js
import express from 'express';
import { GeminiService } from './geminiService.js';

const app = express();
app.post('/analyze', async (req, res) => {
    const service = new GeminiService();
    // SSE streaming
});
```

### Option 3: Hybrid (OPTIMAL)
**Backend Python + Gemini SDK Python**
- Garde architecture Flask
- Utilise `google-generativeai` Python
- Adapte logique TypeScript en Python

## Plan d'Implémentation

### Phase 1: Setup Backend (2h)
```bash
pip install google-generativeai
```

**Fichiers à créer**:
- `deuxieme_cerveau/services/documind_service.py`
- `deuxieme_cerveau/blueprints/documind_routes.py`
- `deuxieme_cerveau/utils/segmentation.py`

### Phase 2: Routes API (1h)
```python
# blueprints/documind_routes.py
@documind_bp.route('/analyze', methods=['POST'])
def analyze_fusion():
    """Remplace /ai/organize"""
    fusion_file = request.json['fusion_file']
    content = read_fusion_file(fusion_file)
    
    def stream():
        for chunk in documind_service.orchestrate(content):
            yield f"data: {json.dumps(chunk)}\n\n"
    
    return Response(stream(), mimetype='text/event-stream')
```

### Phase 3: Frontend Adaptation (2h)
**Remplacer**: `fusion_intelligente.html`
**Par**: Interface streaming moderne

```javascript
// static/documind.js
async function analyzeFusion(fusionPath) {
    const eventSource = new EventSource(`/documind/analyze?file=${fusionPath}`);
    
    eventSource.onmessage = (event) => {
        const data = JSON.parse(event.data);
        updateUI(data.phase, data.content, data.artifacts);
    };
}
```

### Phase 4: Migration Prompts (1h)
**Adapter**: `constants.ts` → `prompts.py`

```python
# config/prompts.py
PROMPT_STAGE_1_ANALYSE = """
IMPORTANT:
Les notes sont déjà séparées par date.
Chaque bloc de notes (chaque date) = UNE idée / UN projet.
Ne JAMAIS mélanger deux blocs.

Structure Markdown à produire:
# Titre principal
## 📝 Extrait original
## 📊 Vue d'ensemble
## ⭐ Idées principales
## 🔸 Idées secondaires
## 📌 Détails
## 🎯 Actions
## 🔚 Conclusion
"""
```

### Phase 5: Testing (1h)
```python
# tests/test_documind_service.py
def test_segmentation():
    service = DocumindService()
    content = "..." * 10000
    segments = service.segment_content(content)
    assert len(segments) > 0

def test_orchestration():
    service = DocumindService()
    results = list(service.orchestrate_analysis(sample_notes))
    assert len(results) == 6  # 6 phases
```

## Structure Finale

```
deuxieme_cerveau/
├── services/
│   ├── documind_service.py      # Core RAG logic
│   └── ai_service.py             # Legacy (à supprimer)
├── blueprints/
│   ├── documind_routes.py        # New routes
│   └── ai_routes.py              # Legacy (à supprimer)
├── utils/
│   └── segmentation.py           # Tri-layer logic
├── config/
│   └── prompts.py                # Gemini prompts
├── static/
│   ├── documind.js               # Frontend logic
│   └── documind.css              # Styles
└── templates/
    └── documind.html             # Interface
```

## Configuration

```env
# .env
GEMINI_API_KEY=your_key_here
GEMINI_FLASH_MODEL=gemini-2.5-flash
GEMINI_PRO_MODEL=gemini-3-pro-preview
```

## Avantages vs Kimi AI

| Feature | Kimi AI | Documind/Gemini |
|---------|---------|-----------------|
| **Orchestration** | Simple | 6-phase pipeline |
| **Segmentation** | Basic | Tri-layer intelligent |
| **Streaming** | Non | Oui (SSE) |
| **Artifacts** | Non | Oui (multi-files) |
| **Workflow** | 1 stage | 3 stages (Analyse/Smart/Insanity) |
| **Context** | Limité | Topology-aware |
| **Cost** | ? | Gemini Flash = cheap |

## Migration Path

1. **Garder Kimi** temporairement
2. **Ajouter Documind** en parallèle (`/documind/*`)
3. **Tester** sur vraies notes
4. **Basculer** bouton "Fusion IA"
5. **Supprimer** ancien système

## Commandes

```bash
# Installation
pip install google-generativeai

# Test service
python -m pytest tests/test_documind_service.py

# Lancer avec nouveau système
python app.py
```

## Timeline

- **Phase 1-2**: 3h (Backend + Routes)
- **Phase 3**: 2h (Frontend)
- **Phase 4-5**: 2h (Prompts + Tests)
- **Total**: ~7h développement
- **Testing**: 2h
- **Documentation**: 1h

**Total estimé**: 10h pour intégration complète
