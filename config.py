from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    MODEL_FILE = 'best_addiction_model.pkl'
    PAGE_CONFIG = {
        "page_title": "Social Media Addiction Predictor",
        "page_icon": "📱",
        "layout": "wide",
        "initial_sidebar_state": "expanded"
    }