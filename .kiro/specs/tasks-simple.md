# Extension Chrome - Plan SIMPLE (Usage Perso)

> Version ultra-simplifiée pour démarrer rapidement

## 🚀 Démarrage Rapide (5 étapes)

### 1. Backend
- [ ] **Déployer Backend** - Lance `DEPLOY.bat` (déjà créé)

### 2. Extension
- [ ] **Créer Extension** - Crée dossier `extension/` avec manifest.json
- [ ] **Configurer URL Backend** - Mets l'URL GAE dans l'extension
- [ ] **Charger Extension** - Chrome → Extensions → Mode dev → Charger

### 3. Test
- [ ] **Tester** - Vérifie que ça marche

---

## 📁 Structure Minimale

```
projet/
├── backend/              ✅ DÉJÀ CRÉÉ
│   ├── index.js
│   ├── app.yaml
│   └── package.json
│
├── extension/            ⚠️ À CRÉER
│   ├── manifest.json
│   ├── popup.html
│   └── popup.js
│
└── DEPLOY.bat           ✅ DÉJÀ CRÉÉ
```

---

## 🎯 Actions Concrètes

### Étape 1 : Déployer Backend (2 min)

```bash
DEPLOY.bat
```

Récupère l'URL affichée : `https://PROJECT_ID.REGION.r.appspot.com`

### Étape 2 : Créer Extension (5 min)

Crée `extension/manifest.json` :
```json
{
  "manifest_version": 3,
  "name": "Mon Extension",
  "version": "1.0",
  "permissions": ["storage"],
  "host_permissions": ["https://*.appspot.com/*"],
  "action": {
    "default_popup": "popup.html"
  }
}
```

Crée `extension/popup.html` :
```html
<!DOCTYPE html>
<html>
<body>
  <button id="test">Test Backend</button>
  <div id="result"></div>
  <script src="popup.js"></script>
</body>
</html>
```

Crée `extension/popup.js` :
```javascript
const BACKEND_URL = 'https://TON-URL.appspot.com';

document.getElementById('test').onclick = async () => {
  const res = await fetch(`${BACKEND_URL}/api/health`);
  const data = await res.json();
  document.getElementById('result').textContent = JSON.stringify(data);
};
```

### Étape 3 : Charger Extension (1 min)

1. Chrome → `chrome://extensions/`
2. Active "Mode développeur"
3. Clique "Charger l'extension non empaquetée"
4. Sélectionne dossier `extension/`

### Étape 4 : Tester (30 sec)

1. Clique sur l'icône de l'extension
2. Clique "Test Backend"
3. Tu dois voir : `{"status":"ok",...}`

---

## ⚠️ Si Problème

**Backend ne répond pas ?**
```bash
cd backend
gcloud app logs tail
```

**Extension ne charge pas ?**
- Vérifie `manifest.json` (pas d'erreur de syntaxe)
- Vérifie l'URL backend dans `popup.js`

**CORS error ?**
- Déjà configuré dans `backend/index.js`

---

## 🔄 Mettre à Jour

**Backend :**
```bash
cd backend
# Modifie index.js
gcloud app deploy
```

**Extension :**
1. Modifie les fichiers
2. Chrome → Extensions → Recharger l'extension

---

**C'est tout ! Pas besoin des 68 autres tâches pour usage perso.**
