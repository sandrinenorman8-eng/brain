# Télécharger fichier .pem depuis Dashboard
# Convertir en clé publique:
openssl rsa -in key.pem -pubout -outform DER | base64 -w 0
```

### 6.2 Méthode B : Installation Manuelle (DÉVELOPPEMENT/TEST)

**Étape 4.2.1 : Empaqueter Extension**

**Option 1: Load Unpacked (recommandé développement)**
```