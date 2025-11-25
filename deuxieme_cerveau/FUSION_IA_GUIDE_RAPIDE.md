# 🧠 GUIDE RAPIDE - FUSION INTELLIGENTE

## C'est quoi ?

Un système d'IA qui transforme vos notes en charabia en contenu organisé avec chapitres et bullet points.

## Comment l'utiliser ?

### 1. Démarrer l'application
```bash
cd deuxieme_cerveau
START.bat
```

### 2. Ouvrir l'interface
http://localhost:5008

### 3. Cliquer sur "🧠 Fusion IA"
Le bouton violet en haut à droite

### 4. Sélectionner une fusion
- Fusions globales (toutes vos notes)
- Fusions par catégorie (notes d'une catégorie)

### 5. Attendre l'organisation
L'IA analyse et structure vos notes (10-30 secondes)

### 6. Utiliser le résultat
- **Copier** : Copie dans le presse-papier
- **Télécharger** : Sauvegarde en fichier .md
- **Lire** : Visualise directement dans la page

## Exemple

### Avant (charabia)
```
10:30:15: Faire la présentation
11:45:22: Appeler Jean pour le projet
14:20:00: Réunion équipe - décisions importantes
15:30:00: Corriger le bug dans le code
```

### Après (organisé par l'IA)
```markdown
# Notes de Travail

## Chapitre 1: Tâches Administratives
- Faire la présentation
- Appeler Jean pour le projet

## Chapitre 2: Réunions
- Réunion équipe
  - Décisions importantes prises

## Chapitre 3: Développement
- Corriger le bug dans le code

## Résumé
- 4 tâches identifiées
- 1 réunion planifiée
- 1 bug à corriger
```

## Où sont sauvegardés les résultats ?

`deuxieme_cerveau/fusion_organized/`

Format : `organized_{categorie}_{date}_{heure}.md`

## Problèmes ?

### L'IA ne répond pas
1. Vérifier que Flask est démarré
2. Tester : http://localhost:5008/ai/test
3. Doit retourner : `{"success": true, "status": "connected"}`

### Erreur "API non disponible"
- Vérifier la connexion internet
- La clé API est déjà configurée dans `config.ini`

### Résultat bizarre
- Essayer avec une fusion plus petite
- Le modèle IA a des limites sur les très gros fichiers

## Configuration

Tout est déjà configuré ! La clé API Groq est dans `config.ini`

Si besoin de changer :
```ini
[DEFAULT]
api_key = VOTRE_CLE_ICI
model = kimi
```

## C'est tout !

Simple, rapide, efficace. Vos notes chaotiques deviennent organisées en un clic.

---

**Documentation complète** : `docs/FUSION_INTELLIGENTE.md`
