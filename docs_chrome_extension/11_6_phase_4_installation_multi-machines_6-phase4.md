6. PHASE 4 : INSTALLATION MULTI-MACHINES {#6-phase4}
6.1 Méthode A : Publication Chrome Web Store (PRODUCTION)
Avantages:
✅ Installation automatique sur tous appareils (sync)
✅ Mises à jour automatiques
✅ ID extension fixe
✅ Distribution scalable
Procédure Complète:
Étape 4.1.1 : Préparation du Package
bash# Créer archive ZIP
cd extension/
zip -r ../extension-v1.0.0.zip . -x "*.git*" -x "node_modules/*"
Fichiers Obligatoires:

manifest.json ✅
Icônes: 16x16, 48x48, 128x128 ✅
Screenshots (1280x800 ou 640x400) ✅
Description détaillée ✅
Politique de confidentialité URL ✅

Étape 4.1.2 : Inscription Chrome Web Store

Accéder: https://chrome.google.com/webstore/devconsole
Payer frais inscription: $5 (unique)
Créer nouveau produit

Étape 4.1.3 : Compléter Informations
yamlNom: Extension Multi-Backend
Description courte: Connecte Chrome à votre backend personnel sécurisé
Description détaillée: |
  Cette extension permet de connecter votre navigateur à un backend
  personnel hébergé en cloud. Fonctionnalités:
  - Configuration URL backend dynamique
  - Authentification OAuth sécurisée
  - Synchronisation multi-appareils
  - Conforme Manifest V3

Catégorie: Développeur/Productivité
Langue: Français
Icône: icon128.png

Screenshots: (4 minimum)
  - Configuration page
  - Authentication flow
  - Popup interface
  - Settings panel

Politique confidentialité: https://your-domain.com/privacy
```

**Étape 4.1.4 : Upload et Soumission**
```