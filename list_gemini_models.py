#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Liste les modèles Gemini disponibles"""

from google import genai

api_key = 'AIzaSyAUDVRdWDVxamiqtCsqEvdMUaVuIs81il8'
client = genai.Client(api_key=api_key)

print("Modèles Gemini disponibles:\n")

try:
    for model in client.models.list():
        print(f"Nom: {model.name}")
        if hasattr(model, 'display_name'):
            print(f"  Display: {model.display_name}")
        if hasattr(model, 'description') and model.description:
            print(f"  Description: {model.description[:100]}")
        print()
except Exception as e:
    print(f"Erreur: {e}")
