# Debug Fusion IA - Chunking Service

## Statut Actuel

✅ **Chunking Service:** Port 5009 actif et fonctionnel
✅ **Flask Main:** Port 5008 actif
✅ **Tests connexion:** Tous passent

## Problème Observé

Quand tu cliques sur "Organiser" dans Fusion IA:
- Page se charge
- API test passe
- Mais ensuite ça bloque

## Vérifications à Faire

### 1. Regarder terminal Chunking Service
Quand tu cliques "Organiser", tu devrais voir:
```
127.0.0.1 - - [23/Nov/2025 07:XX:XX] "POST /organize_large HTTP/1.1" 200 -
```

Si tu ne vois RIEN → la requête n'arrive pas au service

### 2. Regarder terminal Flask Main
Tu devrais voir:
```
[INFO] Fichier détecté: XXX lignes
[INFO] Redirection vers chunking service...
```

Si tu vois:
```
[WARN] Chunking service indisponible: ...
```
→ Problème de connexion

### 3. Vérifier le fichier fusion
```bash
# Compter lignes
python -c "print(len(open('deuxieme_cerveau/fusion_global/fusion_globale_2025-11-20_10-14-43.txt').readlines()))"
```

Doit être >200 lignes pour déclencher chunking

## Solutions

### Solution 1: Forcer le chunking
Modifie le seuil dans `ai_routes.py` ligne 45:
```python
# Avant
if line_count > 200 or char_count > 50000:

# Après (plus agressif)
if line_count > 100 or char_count > 30000:
```

### Solution 2: Test direct
```bash
python TEST_DIRECT_CHUNKING.py
```

Ceci teste directement le chunking service sans passer par Flask.

### Solution 3: Logs détaillés
Ajoute dans `ai_routes.py` après ligne 42:
```python
print(f"[DEBUG] Fichier: {line_count} lignes, {char_count} chars")
print(f"[DEBUG] Chunking requis: {line_count > 200 or char_count > 50000}")
```

## Test Manuel Complet

```bash
# Terminal 1 - Flask
cd deuxieme_cerveau
python app_new.py

# Terminal 2 - Chunking
cd deuxieme_cerveau
python chunking_service.py

# Terminal 3 - Test
python TEST_DIRECT_CHUNKING.py
```

## Commande Debug Rapide

```bash
# Vérifier que les 2 services tournent
netstat -an | findstr ":5008 :5009"

# Tester chunking service
curl http://localhost:5009/health

# Tester Flask
curl http://localhost:5008/categories
```

## Prochaine Étape

Clique sur "Organiser" et copie-colle ici:
1. Ce que tu vois dans terminal Flask
2. Ce que tu vois dans terminal Chunking Service
3. Ce qui s'affiche dans le navigateur (erreur?)
