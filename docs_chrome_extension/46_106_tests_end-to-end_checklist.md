### 10.6 Tests End-to-End Checklist
☐ Test 1: Installation extension première fois
☐ Page options s'ouvre automatiquement
☐ URL backend configurable
☐ Sauvegarde réussit
☐ Test 2: Authentification
☐ Popup OAuth Google s'ouvre
☐ Consentement utilisateur
☐ Token reçu et stocké
☐ Notification succès
☐ Test 3: Appel API
☐ Requête envoyée avec token
☐ Réponse 200 reçue
☐ Données parsées correctement
☐ UI mise à jour
☐ Test 4: Token expiré
☐ Refresh automatique déclenché
☐ Nouveau token obtenu
☐ Requête réessayée avec succès
☐ Test 5: Refresh token expiré
☐ Notification "re-login requis"
☐ Page options ouverte
☐ Bouton Login visible
☐ Test 6: Backend down
☐ Retry automatique (3 tentatives)
☐ Erreur affichée utilisateur
☐ Pas de crash extension
☐ Test 7: Changement URL backend
☐ Nouvelle URL sauvegardée
☐ Extension rechargée
☐ Connexions utilisent nouvelle URL
☐ Test 8: Installation machine 2
☐ Extension installée via Web Store
☐ backendUrl synchronisé (si sync)
☐ Login OAuth fonctionne
☐ Appels API réussissent
☐ Test 9: Offline/Online
☐ Mode offline: erreurs gérées
☐ Retour online: auto-reconnexion
☐ Pas de données perdues

---
