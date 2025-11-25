### 10.2 Extension Checklist
☐ manifest.json Manifest V3
☐ manifest_version: 3
☐ permissions: ["storage", "identity"]
☐ host_permissions: domaines backend listés
☐ background.service_worker: "background.js"
☐ options_ui.page: "options.html"
☐ content_security_policy.extension_pages configurée
☐ connect-src inclut tous domaines backend
☐ OAuth client_id configuré (si Google)
☐ Icônes: 16x16, 48x48, 128x128 présentes
☐ background.js implémenté avec:
☐ getBackendUrl() depuis storage
☐ getAuthToken() avec refresh automatique
☐ callBackend() avec retry logic
☐ chrome.runtime.onMessage listener
☐ options.html créé avec champs:
☐ Input URL backend
☐ Bouton Save
☐ Bouton Test Connection
☐ Bouton Login OAuth
☐ options.js implémenté avec:
☐ Chargement URL depuis storage.sync
☐ Sauvegarde URL dans storage.sync
☐ Test connexion backend
☐ Authentification OAuth complète
☐ Pas de secrets hardcodés dans code
☐ Tous console.log() utiles pour debug
