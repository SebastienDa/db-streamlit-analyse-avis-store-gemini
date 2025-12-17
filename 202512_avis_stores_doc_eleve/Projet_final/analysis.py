import streamlit as st
import google.generativeai as genai
import json
from pydantic import BaseModel, Field
from typing import List
import config

# ======================================================================
# DATA MODELS
# ======================================================================

class Theme(BaseModel):
    title: str = Field(description="Titre court et percutant de la thématique")
    volume: str = Field(description="Estimation du volume, ex: '~40 avis'")
    sentiment: str = Field(description="Analyse du sentiment en une phrase")
    sentiment_type: str = Field(description="Type de sentiment: 'pos', 'neg', ou 'neu'")
    verbatim: str = Field(description="Citation représentative d'un utilisateur")

class Recommendation(BaseModel):
    action: str = Field(description="Action concrète à entreprendre")
    why: str = Field(description="Justification de l'action")
    proof: str = Field(description="Avis complet justifiant la recommandation")

class AnalysisResponse(BaseModel):
    edito: str = Field(description="Résumé éditorial de la semaine en 3 lignes")
    themes: List[Theme] = Field(description="Liste de 8 thématiques majeures")
    recos: List[Recommendation] = Field(description="Liste de 5 recommandations actionnables")

# ======================================================================
# AI FUNCTION
# ======================================================================

def generate_ai_analysis_json(df, start_date, end_date, kpis):
    text_blob = ""
    for _, row in df.iterrows():
        text_blob += f"[{row['rating']}★] - {row['store']} - {row['review_text']}\n"

    prompt = f"""
    Tu es Lead Product Analyst. Analyse ces avis utilisateurs ({start_date}-{end_date}).
    KPIs: {kpis['avg']}/5 sur {kpis['total']} avis.
    
    Identifie STRICTEMENT 8 thématiques majeures et 5 recommandations actionnables.
    
    AVIS À ANALYSER :
    {text_blob[:60000]}
    """
    
    try:
        model = genai.GenerativeModel(config.MODEL_NAME)
        
        # Configuration pour la sortie structurée (JSON via Pydantic)
        generation_config = {
            "response_mime_type": "application/json",
            "response_schema": AnalysisResponse
        }
        
        response = model.generate_content(
            prompt, 
            generation_config=generation_config
        )
        
        # Parsing direct du JSON retourné
        print(response.text)
        return json.loads(response.text)
        
    except Exception as e:
        st.error(f"Erreur IA: {e}")
        return None
