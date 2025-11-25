# 📂 INDEX FICHIERS DE DONNÉES

## 🗂️ STRUCTURE HIÉRARCHIQUE DU DOSSIER data/

### Vue d'ensemble
```
data/
├── api/                           # Notes API
├── automatisation/                # Notes automatisation
├── buziness/                      # 🏢 BUSINESS
│   ├── association/
│   ├── idée business/
│   ├── la villa de la paix/
│   ├── lagence/
│   ├── money brick/
│   └── opportunité/
├── cinema/                        # 🎬 CINÉMA
│   └── scénario/
├── comfy/                         # Notes Comfy
├── extentions/                    # Notes extensions
├── koko/                          # Notes Koko
├── livres/                        # 📚 LIVRES
│   ├── idee philo/
│   ├── motivation/
│   ├── psychologie succès/
│   └── société de livres/
├── logiciels/                     # 💻 LOGICIELS
│   ├── agenda intelligent/
│   ├── brikmagik/
│   ├── chrono brique/
│   ├── kodi brik/
│   ├── memobrik/
│   ├── promptbrik/
│   └── scrap them all/
├── priorité/                      # ⚡ PRIORITÉ
│   └── todo/
├── prompt ai vfx/                 # Notes AI VFX
├── series/                        # 📺 SÉRIES
│   ├── GEN Z/
│   └── projet youtube/
├── succès du jour/                # Notes succès
├── test/                          # Notes test
└── web manager/                   # Notes web manager
```

---

## 📋 MAPPING CATÉGORIES → CHEMINS

### Fichier : category_mapping.json

| Catégorie | Chemin complet | Parent |
|-----------|----------------|--------|
| api | api | - |
| automatisation | automatisation | - |
| association | buziness/association | buziness |
| idée business | buziness/idée business | buziness |
| la villa de la paix | buziness/la villa de la paix | buziness |
| lagence | buziness/lagence | buziness |
| money brick | buziness/money brick | buziness |
| opportunité | buziness/opportunité | buziness |
| scénario | cinema/scénario | cinema |
| comfy | comfy | - |
| extentions | extentions | - |
| koko | koko | - |
| idee philo | livres/idee philo | livres |
| motivation | livres/motivation | livres |
| psychologie succès | livres/psychologie succès | livres |
| société de livres | livres/société de livres | livres |
| agenda intelligent | logiciels/agenda intelligent | logiciels |
| brikmagik | logiciels/brikmagik | logiciels |
| chrono brique | logiciels/chrono brique | logiciels |
| kodi brik | logiciels/kodi brik | logiciels |
| memobrik | logiciels/memobrik | logiciels |
| promptbrik | logiciels/promptbrik | logiciels |
| scrap them all | logiciels/scrap them all | logiciels |
| todo | priorité/todo | priorité |
| prompt ai vfx | prompt ai vfx | - |
| GEN Z | series/GEN Z | series |
| projet youtube | series/projet youtube | series |
| succès du jour | succès du jour | - |
| test | test | - |
| web manager | web manager | - |

---

## 📝 FORMAT DES FICHIERS DE NOTES

### Convention de nommage
```
{category}_{YYYY-MM-DD}.txt
```

**Exemples** :
- `todo_2025-11-16.txt`
- `memobrik_2025-11-15.txt`
- `scénario_2025-10-24.txt`

### Format du contenu
```
HH:MM:SS: Première note de la journée
HH:MM:SS: Deuxième note avec plus de détails
HH:MM:SS: Troisième note
```

**Exemple réel** :
```
10:30:15: Implémenter la fonction de recherche
11:45:22: Bug corrigé dans le système de catégories
14:20:00: Réunion avec l'équipe - décisions importantes
```

---

## 🎨 MÉTADONNÉES DES CATÉGORIES

### Fichier : categories.json

| Catégorie | Emoji | Couleur | Description |
|-----------|-------|---------|-------------|
| todo | ✅ | #4CAF50 | Tâches prioritaires |
| memobrik | 🧠 | #2196F3 | Projet Memobrik |
| scénario | 🎬 | #E91E63 | Scénarios de films |
| brikmagik | ✨ | #9C27B0 | Projet Brikmagik |
| promptbrik | 💬 | #FF9800 | Projet Promptbrik |
| association | 🤝 | #795548 | Notes association |
| money brick | 💰 | #4CAF50 | Projet Money Brick |
| motivation | 🔥 | #F44336 | Livres motivation |
| projet youtube | 📹 | #FF0000 | Projet YouTube |

---

## 📊 STATISTIQUES PAR CATÉGORIE

### Catégories les plus utilisées (estimation)
1. **todo** - Tâches quotidiennes
2. **memobrik** - Développement principal
3. **scénario** - Écriture créative
4. **promptbrik** - Projet IA
5. **projet youtube** - Contenu vidéo

---

## 🔍 RECHERCHE DANS LES DONNÉES

### Fichiers indexés
- **Extension** : `.txt` uniquement
- **Encodage** : UTF-8 (avec fallback cp1252, latin-1)
- **Recherche** : Insensible à la casse
- **Contexte** : 100 caractères autour du match

### Commande de recherche manuelle
```bash
# Windows
findstr /S /I "mot_clé" data\*.txt

# PowerShell
Get-ChildItem -Path data -Recurse -Filter *.txt | Select-String "mot_clé"
```

---

## 💾 BACKUPS

### Dossiers de backup
```
deuxieme_cerveau/
├── backups/              # Backups automatiques (anciens)
├── fusion_categories/    # Fusions par catégorie
├── fusion_global/        # Fusions globales
└── zip/                  # Archives complètes
```

### Fichiers de fusion

#### fusion_global/
**Format** : `fusion_globale_{YYYY-MM-DD}_{HH-MM-SS}.txt`
**Contenu** : TOUTES les notes de TOUTES les catégories, triées chronologiquement

**Exemple** :
```
fusion_globale_2025-11-16_14-30-00.txt
```

#### fusion_categories/
**Format** : `fusion_categories_{cat1}_{cat2}_{YYYY-MM-DD}_{HH-MM-SS}.txt`
**Contenu** : Notes des catégories sélectionnées, triées chronologiquement

**Exemples** :
```
fusion_categories_todo_memobrik_2025-11-16_14-30-00.txt
fusion_categories_scénario_2025-10-26_07-39-52.txt
```

---

## 🛡️ PROTECTION DES DONNÉES

### Fichiers critiques à NE JAMAIS supprimer
1. **data/** - Toutes vos notes
2. **categories.json** - Définition des catégories
3. **category_mapping.json** - Mapping des chemins

### Commande de backup manuel
```bash
cd deuxieme_cerveau
python -c "
import shutil, datetime
timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
shutil.make_archive(f'../zip/backup_manuel_{timestamp}', 'zip', 'data')
print(f'Backup créé: backup_manuel_{timestamp}.zip')
"
```

---

## 📈 CROISSANCE DES DONNÉES

### Estimation de taille
- **Fichier texte moyen** : 1-5 KB
- **Notes par jour** : 5-20
- **Croissance mensuelle** : ~500 KB - 2 MB
- **Croissance annuelle** : ~6-24 MB

### Nettoyage recommandé
- **Jamais** : Ne supprimez pas les notes
- **Fusion** : Utilisez la fusion pour consolider
- **Archive** : Déplacez les anciennes fusions vers un dossier archive

---

## 🔧 MAINTENANCE

### Vérifier l'intégrité des données
```bash
cd deuxieme_cerveau
python -c "
import os, json

# Vérifier categories.json
with open('categories.json', 'r', encoding='utf-8') as f:
    cats = json.load(f)
    print(f'Catégories définies: {len(cats)}')

# Vérifier category_mapping.json
with open('category_mapping.json', 'r', encoding='utf-8') as f:
    mapping = json.load(f)
    print(f'Mappings définis: {len(mapping)}')

# Compter les fichiers
total = 0
for root, dirs, files in os.walk('data'):
    total += len([f for f in files if f.endswith('.txt')])
print(f'Fichiers de notes: {total}')
"
```

### Nettoyer les dossiers vides
```bash
cd deuxieme_cerveau
python -c "
import os, shutil
for root, dirs, files in os.walk('data', topdown=False):
    for d in dirs:
        path = os.path.join(root, d)
        if not os.listdir(path):
            os.rmdir(path)
            print(f'Supprimé: {path}')
"
```

---

## 📞 RÉCUPÉRATION D'URGENCE

### Si categories.json est perdu
```json
{
  "todo": {"emoji": "✅", "color": "#4CAF50"},
  "memobrik": {"emoji": "🧠", "color": "#2196F3"},
  "scénario": {"emoji": "🎬", "color": "#E91E63"}
}
```

### Si category_mapping.json est perdu
```json
{
  "todo": "priorité/todo",
  "memobrik": "logiciels/memobrik",
  "scénario": "cinema/scénario"
}
```

### Reconstruire le mapping depuis data/
```bash
python -c "
import os, json
mapping = {}
for root, dirs, files in os.walk('data'):
    for d in dirs:
        rel_path = os.path.relpath(os.path.join(root, d), 'data')
        category_name = d
        mapping[category_name] = rel_path.replace('\\\\', '/')
with open('category_mapping_rebuilt.json', 'w', encoding='utf-8') as f:
    json.dump(mapping, f, indent=2, ensure_ascii=False)
print('Mapping reconstruit dans category_mapping_rebuilt.json')
"
```
