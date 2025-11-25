# Quick Test Browserbase MCP avec Ngrok

## Setup Rapide (3 étapes)

### 1. Démarrer les services
```bash
START_ALL_SERVICES.bat
```
Attend 10 secondes que tout démarre.

### 2. Démarrer ngrok
```bash
START_NGROK_FLASK.bat
```
Copie l'URL HTTPS affichée (ex: `https://abc123.ngrok.io`)

### 3. Tester avec Kiro

Dans Kiro, utilise ce prompt:

```
Utilise Browserbase MCP pour naviguer vers [TON_URL_NGROK] et:
1. Prendre un screenshot de la page
2. Observer les boutons disponibles
3. Cliquer sur "Fusion IA"
4. Me décrire ce que tu vois
```

---

## Commandes MCP Browserbase Disponibles

### Navigation
```
browserbase_stagehand_navigate
- url: "https://abc123.ngrok.io"
```

### Screenshot
```
browserbase_screenshot
```

### Observer éléments
```
browserbase_stagehand_observe
- instruction: "Find all buttons on the page"
```

### Interagir
```
browserbase_stagehand_act
- action: "Click on 'Fusion IA' button"
```

### Extraire données
```
browserbase_stagehand_extract
- instruction: "Extract all category names"
```

---

## Test Automatique Python

```bash
python TEST_BROWSERBASE_NGROK.py
```

Ce script:
1. Vérifie Flask local
2. Démarre ngrok automatiquement
3. Teste l'accès via tunnel
4. Génère le prompt pour Kiro
5. Attend que tu testes
6. Arrête ngrok proprement

---

## Troubleshooting

### Ngrok ne démarre pas
```bash
# Vérifier ngrok installé
ngrok.exe version

# Tester manuellement
ngrok.exe http 5008
```

### Flask non accessible
```bash
# Vérifier port 5008
netstat -an | findstr :5008

# Redémarrer Flask
STOP_ALL_SERVICES.bat
START_ALL_SERVICES.bat
```

### Browserbase MCP erreur
Vérifier dans `.kiro/settings/mcp.json`:
- `BROWSERBASE_API_KEY` valide
- `BROWSERBASE_PROJECT_ID` correct
- `disabled: false`

---

## Configuration Browserbase

Actuellement configuré:
- **API Key**: `bb_live_-Q2jqMd3m0I3A3yV7BrCKvl1xAs`
- **Project ID**: `bee5922c-e094-40c2-8279-fe176da275dc`
- **Model**: `gemini-2.0-flash-lite`

---

## Exemples de Tests

### Test 1: Navigation simple
```
Navigate to [NGROK_URL] using browserbase and take a screenshot
```

### Test 2: Interaction
```
Using browserbase:
1. Go to [NGROK_URL]
2. Click on "Fusion IA" button
3. Take a screenshot of the result
```

### Test 3: Extraction données
```
Using browserbase, navigate to [NGROK_URL] and extract:
- All category names
- Number of notes per category
- Available actions/buttons
```

### Test 4: Workflow complet
```
Using browserbase on [NGROK_URL]:
1. Navigate to main page
2. Observe available categories
3. Click on first category
4. Extract the notes content
5. Summarize what you found
```

---

## Notes Importantes

⚠️ **Ngrok gratuit**: URL change à chaque redémarrage
⚠️ **Timeout**: Browserbase sessions expirent après 5 min d'inactivité
⚠️ **Rate limits**: API Browserbase limitée selon plan

✅ **Auto-approve**: Toutes les commandes Browserbase sont pré-approuvées dans MCP config
✅ **Multi-session**: Support de sessions multiples simultanées
✅ **Gemini intégré**: Utilise Gemini pour comprendre les instructions

---

## Workflow Recommandé

1. **Démarrer services** → `START_ALL_SERVICES.bat`
2. **Démarrer ngrok** → `START_NGROK_FLASK.bat`
3. **Copier URL** → Depuis terminal ngrok
4. **Tester dans Kiro** → Utiliser prompts ci-dessus
5. **Observer résultats** → Screenshots + extractions
6. **Arrêter** → Ctrl+C dans ngrok, puis `STOP_ALL_SERVICES.bat`

---

**Durée test**: ~5 minutes  
**Prérequis**: Flask + ngrok + Browserbase MCP configuré  
**Objectif**: Valider accès externe à l'app via Browserbase
