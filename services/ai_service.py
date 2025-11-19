# -*- coding: utf-8 -*-
"""
Service d'IA pour organiser les fusions de catégories
Utilise l'API Groq pour transformer le charabia en contenu structuré
"""

import requests
import configparser
import os
import json

class AIService:
    def __init__(self):
        self.config = self._load_config()
        self.api_key = self.config.get('DEFAULT', 'api_key')
        self.model = self.config.get('DEFAULT', 'model', fallback='moonshotai/kimi-k2-instruct-0905')
        self.api_url = "https://api.groq.com/openai/v1/chat/completions"
        
    def _load_config(self):
        """Charge la configuration depuis config.ini"""
        config = configparser.ConfigParser()
        config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.ini')
        config.read(config_path, encoding='utf-8')
        return config
    
    def organize_fusion(self, fusion_content, category_name):
        """
        Organise le contenu d'une fusion de catégorie avec l'IA
        
        Args:
            fusion_content: Contenu brut de la fusion
            category_name: Nom de la catégorie
            
        Returns:
            dict: Contenu organisé avec chapitres et bullet points
        """
        
        system_prompt = """RÔLE
Notes brutes → système de connaissances hiérarchisé

PROTOCOLE

PHASE 1: EXTRACTION
Extraire: concepts, arguments, faits, questions implicites
Identifier: chaînes causales, dépendances, liens inter-domaines
Taguer: idées centrales vs détails vs exemples

PHASE 2: PRIORISATION
Critères:
- Impact potentiel (court/moyen/long terme)
- Degré d'innovation
- Valeur intellectuelle
- Faisabilité technique
- Effet de levier

Structure 3 niveaux:
L1: Noyau stratégique (impact majeur)
L2: Éléments de soutien (impact significatif)
L3: Détails complémentaires

PHASE 3: ENRICHISSEMENT
Par note:
- Corriger: grammaire, syntaxe, ambiguïté, redondance
- Enrichir: précision, implications, extensions, exemples, angles morts
- Valider: potentiel révélé, sens préservé, zéro remplissage

PHASE 4: ASSEMBLAGE
- Groupement thématique logique
- Chapitres cohérents (max 3 niveaux)
- Gradient d'importance
- Relations logiques explicites

TEMPLATE DE SORTIE

[TITRE - Synthèse Corpus]
Énoncé objectif global

📊 VUE STRATÉGIQUE
[Cartographie: thèmes majeurs, niveaux maturité, axes prioritaires]

⭐ NIVEAU 1: IMPACT MAJEUR (5/5)

[Thème A]
Reformulation: [Version corrigée]

Enrichissement conceptuel: [Développer implications. Expliquer connexions interdisciplinaires. Explorer extensions logiques. Fournir contexte et exemples. Justifier importance stratégique.]

Évaluation:
- Brillance: [X/10] - [Analyse pourquoi innovant/prometteur]
- Faisabilité: [X/10] - [Analyse pratique: ressources, obstacles, timeline, implémentation]

Points clés:
- [Point 1: explication + précision + exemple + contexte]
- [Point 2: angle complémentaire développé]
- [Nuance critique expliquée]
- [Implication pratique détaillée]

🔸 NIVEAU 2: IMPACT SIGNIFICATIF (3-4/5)

[Thème B]
Reformulation: [Corrigé + clarifié]

Extension stratégique: [Comment amplifie/complète idées L1]
- [Élément 1: contexte et enrichissement]
- [Élément 2: développement]

📌 NIVEAU 3: COMPLÉMENTAIRE (1-2/5)

[Détails & Notes Techniques]
[Informations tertiaires organisées]

🔗 MATRICE CONNEXIONS

| Idée A | Relation | Idée B | Analyse Synergie/Tension |
|--------|----------|--------|--------------------------|
| [X] | ↔️/→ | [Y] | [Explication nature relation et implications] |

🎯 SYNTHÈSE HIÉRARCHIQUE

Top 3 Idées Essentielles
1. [Idée 1] - [Importance stratégique]
2. [Idée 2] - [Pourquoi critique/différenciant]
3. [Idée 3] - [Potentiel inexploité]

Immédiatement Actionnable
- [Action 1: contexte et rationale]
- [Action 2: chemin implémentation]

À Approfondir
- [Piste 1: raisonnement]
- [Piste 2: justification]

📈 ÉVALUATION GLOBALE

Scores Consolidés
- Brillance Globale: [X/10]
  Justification: [Analyse originalité, innovation, potentiel disruptif]
  
- Faisabilité Globale: [X/10]
  Justification: [Évaluation implications pratiques, contraintes, opportunités]
  
- Cohérence Système: [X/10]
  Justification: [Évaluation qualité articulation inter-idées]

Points de Génie Identifiés
- [Idée/angle le plus innovant - pourquoi]
- [Connexion la plus perspicace - signification]
- [Potentiel le plus prometteur]

Angles Morts Détectés
- [Écart 1: implications]
- [Écart 2: conséquences]
- [Question critique: importance]

🚀 ANALYSE FAISABILITÉ & BRILLANCE

Faisabilité Approfondie
Réalisabilité: [Simple/Moyen/Complexe]

Prérequis identifiés:
- [Ressource/compétence 1: nécessité et chemin acquisition]
- [Ressource/compétence 2: importance et disponibilité]

Obstacles critiques:
- [Obstacle 1: analyse + stratégie mitigation]
- [Obstacle 2: évaluation + approche contournement]

Estimation timeline:
- Prototypage: [X semaines/mois - justifier]
- Développement: [X mois - phases]
- Déploiement: [X mois - processus]

Brillance Approfondie
Forces dominantes:
- [Ce qui distingue - unicité]
- [Angles différenciants - avantage compétitif]

Potentiel impact:
- [Pourquoi prometteur]
- [Domaines transformables - analyse marché]

Opportunités cachées:
- [Insight non perçu - implications]
- [Application inattendue - potentiel]"""

        user_prompt = f"""Catégorie: {category_name}

Notes brutes à transformer en système de connaissances hiérarchisé:

{fusion_content}

Applique le protocole complet (EXTRACTION → PRIORISATION → ENRICHISSEMENT → ASSEMBLAGE) et génère la sortie selon le template structuré."""

        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": "moonshotai/kimi-k2-instruct-0905",
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                "temperature": 0.7,
                "max_completion_tokens": 8192,
                "top_p": 1,
                "stream": False
            }
            
            response = requests.post(
                self.api_url,
                headers=headers,
                json=payload,
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                organized_content = result['choices'][0]['message']['content']
                
                return {
                    "success": True,
                    "organized_content": organized_content,
                    "category": category_name,
                    "model": self.model
                }
            else:
                return {
                    "success": False,
                    "error": f"API Error: {response.status_code}",
                    "details": response.text
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def test_connection(self):
        """Teste la connexion à l'API"""
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": "moonshotai/kimi-k2-instruct-0905",
                "messages": [
                    {"role": "user", "content": "Test"}
                ],
                "max_completion_tokens": 10
            }
            
            response = requests.post(
                self.api_url,
                headers=headers,
                json=payload,
                timeout=10
            )
            
            return response.status_code == 200
        except:
            return False
