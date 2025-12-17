import os
import google.generativeai as genai
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# ======================================================================
# CONFIGURATION
# ======================================================================
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)

MODEL_NAME = "gemini-2.5-pro"

GOOGLE_PLAY_APP_ID = "ai.mistral.chat"
APPLE_APP_ID = "6740410176"
