# Test MCP Tools - Quick Reference

## MCP Servers Configurés

### 1. Browserbase
**Status:** ✅ Configuré
**API Key:** `bb_live_-Q2jqMd3m0I3A3yV7BrCKvl1xAs`
**Project ID:** `bee5922c-e094-40c2-8279-fe176da275dc`

**Commandes disponibles:**
- `browserbase_stagehand_navigate` - Naviguer vers URL
- `browserbase_stagehand_act` - Interagir (clic, remplir)
- `browserbase_stagehand_extract` - Extraire données
- `browserbase_stagehand_observe` - Observer éléments
- `browserbase_screenshot` - Screenshot
- `browserbase_session_create` - Créer session
- `multi_browserbase_stagehand_*` - Sessions multiples

**Test rapide:**
```
Navigate to https://example.com using browserbase and take a screenshot
```

---

### 2. Tavily (Search)
**Status:** ✅ Configuré
**API Key:** `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`

**Commandes disponibles:**
- `tavily-search` - Recherche web
- `tavily-crawl` - Crawler site
- `tavily-extract` - Extraire contenu
- `tavily-map` - Mapper site

**Test rapide:**
```
Use Tavily to search for "Flask chunking best practices"
```

---

### 3. Playwright
**Status:** ✅ Configuré

**Commandes disponibles:**
- `Playwright_navigate` - Navigation
- `Playwright_screenshot` - Screenshot
- `Playwright_click` - Clic
- `Playwright_fill` - Remplir formulaire
- `Playwright_evaluate` - Exécuter JS

**Test rapide:**
```
Use Playwright to navigate to http://localhost:5008 and take a screenshot
```

---

### 4. Puppeteer
**Status:** ✅ Configuré

**Commandes disponibles:**
- `puppeteer_navigate`
- `puppeteer_screenshot`
- `puppeteer_click`
- `puppeteer_evaluate`

**Test rapide:**
```
Use Puppeteer to navigate to http://localhost:5008 and get the page title
```

---

### 5. Apify
**Status:** ✅ Configuré
**Token:** `REDACTED`

**Commandes disponibles:**
- `search-actors` - Chercher actors
- `fetch-actor-details` - Détails actor
- `call-actor` - Exécuter actor
- `apify/rag-web-browser` - RAG browser

**Test rapide:**
```
Use Apify to search for web scraping actors
```

---

### 6. n8n
**Status:** ✅ Configuré

**Commandes disponibles:**
- `n8n_trigger_webhook_workflow`
- `n8n_get_execution`
- `n8n_list_executions`
- `n8n_health_check`

**Test rapide:**
```
Check n8n health status
```

---

### 7. Chrome DevTools
**Status:** ✅ Configuré
**CDP URL:** `ws://localhost:9222/devtools/browser/5cbc8462-363b-42bf-952e-95902ff058ac`

**Commandes disponibles:**
- `mcp_chrome_devtools_take_snapshot`
- `mcp_chrome_devtools_click`
- `mcp_chrome_devtools_evaluate_script`
- `navigate_page`
- `take_screenshot`

**Test rapide:**
```
Use Chrome DevTools to take a snapshot of the current page
```

---

### 8. Filesystem
**Status:** ✅ Configuré
**Path:** `G:\memobrik`

**Commandes disponibles:**
- `list_directory`
- `read_file`
- `write_file`
- `create_directory`
- `search_files`

**Test rapide:**
```
List files in G:\memobrik\deuxieme_cerveau
```

---

### 9. Accessibility (Axe)
**Status:** ✅ Configuré

**Commandes disponibles:**
- `scan-url` - Scanner URL
- `scan-html` - Scanner HTML
- `analyze` - Analyser accessibilité

**Test rapide:**
```
Scan http://localhost:5008 for accessibility issues
```

---

### 10. Fetch
**Status:** ⚠️ Erreur (uvx non trouvé)

**Fix:**
```bash
# Installer uv
pip install uv

# Ou désactiver dans .kiro/settings/mcp.json
"fetch": { "disabled": true }
```

---

## Tests Recommandés

### Test 1: Browserbase + Ngrok
```
1. Start ngrok: START_NGROK_FLASK.bat
2. Copy ngrok URL
3. Prompt: "Navigate to [NGROK_URL] using browserbase and take a screenshot"
```

### Test 2: Playwright Local
```
Use Playwright to:
1. Navigate to http://localhost:5008
2. Click on "Fusion IA" button
3. Take a screenshot
4. Extract the page title
```

### Test 3: Tavily Search
```
Use Tavily to search for "smart text chunking for LLMs" and summarize the top 3 results
```

### Test 4: Filesystem + Analysis
```
1. List all Python files in G:\memobrik\deuxieme_cerveau
2. Read chunking_service.py
3. Analyze the code structure
```

### Test 5: Multi-tool Workflow
```
Use Playwright to navigate to http://localhost:5008, then use Accessibility scanner to check for issues, then summarize findings
```

---

## Troubleshooting

### MCP Server Not Responding
```bash
# Vérifier logs dans Kiro
# Ou redémarrer serveur depuis MCP panel
```

### uvx Error (Fetch server)
```json
// Dans .kiro/settings/mcp.json
"fetch": {
  "disabled": true  // Désactiver temporairement
}
```

### Browserbase Timeout
```
Browserbase sessions expirent après 5 min d'inactivité
Créer nouvelle session si timeout
```

---

## Quick Test Commands

```bash
# Test tous les services locaux
curl http://localhost:5008/categories  # Flask
curl http://localhost:5009/health      # Chunking
curl http://localhost:3008/status      # Search (si actif)

# Test ngrok
ngrok http 5008

# Test MCP dans Kiro
"List all available MCP tools"
"Test browserbase connection"
"Use Playwright to screenshot localhost:5008"
```
