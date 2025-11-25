# ⚡ Commandes Rapides - Extension Chrome

## 🎯 Navigation

```bash
# Voir le menu principal
python quick_nav.py

# Quick Start (5 sections prioritaires)
python quick_nav.py quick

# Liste complète des 67 sections
python quick_nav.py list

# Lire une section spécifique
python quick_nav.py 9
python quick_nav.py 41
```

## 📊 Progression

```bash
# Voir la progression globale
python update_progress.py show

# Marquer une tâche comme complétée
python update_progress.py 4
python update_progress.py 9
```

## 🔧 Découpage de Documents

```bash
# Découper un nouveau document
python smart_doc_splitter.py "mon_document.txt" "docs_output"

# Générer tasks.md depuis les docs
python create_kiro_tasks.py docs_output tasks_nouveau.md
```

## 📁 Fichiers Importants

| Fichier | Description |
|---------|-------------|
| `tasks.md` | **FICHIER PRINCIPAL** - Ouvre-le dans Kiro |
| `docs_chrome_extension/00_INDEX.md` | Index complet des 67 sections |
| `README_CHROME_EXTENSION.md` | Documentation complète |
| `tasks.json` | Métadonnées pour automatisation |

## 🚀 Workflow Recommandé

### 1. Démarrage
```bash
# Voir les sections prioritaires
python quick_nav.py quick

# Ouvrir tasks.md dans Kiro
# Cliquer sur les liens pour naviguer
```

### 2. Lecture
```bash
# Lire section par section
python quick_nav.py 4   # Architecture
python quick_nav.py 9   # Configuration
python quick_nav.py 10  # Sécurité
```

### 3. Suivi
```bash
# Marquer comme fait
python update_progress.py 4

# Voir progression
python update_progress.py show
```

## 💡 Astuces Kiro

Dans Kiro, tu peux dire :

- "Ouvre la section 9 du document Chrome"
- "Montre-moi le Quick Start"
- "Exécute les commandes de la section 10"
- "Quelle est ma progression ?"
- "Marque la tâche 4 comme terminée"

## 📋 Sections Quick Start

| # | Section | Lignes | Priorité |
|---|---------|--------|----------|
| 4 | Architecture Globale | 28 | 🔥 CRITIQUE |
| 9 | Configuration Extension | 329 | 🔥 CRITIQUE |
| 10 | Sécurisation & Auth | 228 | 🔥 CRITIQUE |
| 41 | Checklist Finale | 18 | ⭐ Important |
| 42 | Extension Checklist | 29 | ⭐ Important |

## 🎓 Exemples d'Utilisation

### Scénario 1 : Je débute
```bash
# 1. Voir le Quick Start
python quick_nav.py quick

# 2. Lire l'architecture
python quick_nav.py 4

# 3. Ouvrir tasks.md dans Kiro
# 4. Suivre les liens un par un
```

### Scénario 2 : Je cherche une info précise
```bash
# 1. Lister toutes les sections
python quick_nav.py list

# 2. Identifier le numéro
# 3. Lire la section
python quick_nav.py 28  # Exemple: CSP
```

### Scénario 3 : Je veux suivre ma progression
```bash
# 1. Voir où j'en suis
python update_progress.py show

# 2. Marquer ce que j'ai fait
python update_progress.py 4
python update_progress.py 9

# 3. Revoir la progression
python update_progress.py show
```

## 🔍 Recherche dans les Sections

```bash
# Windows - Chercher un mot-clé dans tous les fichiers
findstr /s /i "CORS" docs_chrome_extension\*.md
findstr /s /i "OAuth" docs_chrome_extension\*.md
findstr /s /i "manifest" docs_chrome_extension\*.md

# Ou utiliser Kiro
# "Cherche 'CORS' dans les docs Chrome"
```

## 📦 Structure Complète

```
📁 Projet Extension Chrome
│
├── 📄 tasks.md                    ← COMMENCE ICI
├── 📄 tasks.json                  ← Métadonnées
├── 📄 README_CHROME_EXTENSION.md  ← Doc complète
├── 📄 QUICK_COMMANDS.md           ← Ce fichier
│
├── 📁 docs_chrome_extension/      ← 67 sections
│   ├── 00_INDEX.md
│   ├── 01_Introduction.md
│   ├── 04_2_architecture...md     ← Quick Start
│   ├── 09_phase_2_config...md     ← Quick Start
│   ├── 10_5_phase_3_secu...md     ← Quick Start
│   ├── 41_checklist_finale.md     ← Quick Start
│   ├── 42_102_extension...md      ← Quick Start
│   └── ... (62 autres)
│
└── 🐍 Scripts Python
    ├── smart_doc_splitter.py      ← Découpage
    ├── create_kiro_tasks.py       ← Génération tasks
    ├── quick_nav.py               ← Navigation CLI
    └── update_progress.py         ← Suivi progression
```

## 🎯 Objectif Final

- [ ] Comprendre l'architecture (Section 4)
- [ ] Configurer l'extension (Section 9)
- [ ] Implémenter la sécurité (Section 10)
- [ ] Déployer sur plusieurs machines (Sections 11-19)
- [ ] Gérer les edge cases (Sections 20-30)
- [ ] Valider avec les checklists (Sections 41-46)

**Progression : 0/67 sections**

---

💡 **Conseil** : Ouvre `tasks.md` dans Kiro et laisse-toi guider !
