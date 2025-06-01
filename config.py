"""
Configurazione centralizzata per il Sistema di Conversazione AI
"""

import os
from typing import Dict, Any

class Config:
    """Classe di configurazione centralizzata"""
    
    # === API SETTINGS ===
    API_URL = "http://localhost:1234/v1/chat/completions"
    API_HEADERS = {
        "Content-Type": "application/json"
    }
    
    # === CONVERSATION SETTINGS ===
    DEFAULT_EXCHANGES = 7
    MIN_EXCHANGES = 1
    MAX_EXCHANGES = 100  # Limite ragionevole
    
    # === AI RESPONSE SETTINGS ===
    DEFAULT_TEMPERATURE = 0.8
    TEMPERATURE_INCREMENT = 0.02
    MAX_TEMPERATURE = 0.9
    MAX_TOKENS = -1  # Illimitato
    
    # === RESPONSE FORMATTING ===
    MAX_SENTENCES_PER_RESPONSE = 4
    MIN_SENTENCES_PER_RESPONSE = 2
    
    # === CONVERSATION CONTEXT ===
    MAX_HISTORY_LINES = 8  # Numero massimo di linee di storia da mantenere
    
    # === SUMMARY SETTINGS ===
    SUMMARY_TEMPERATURE = 0.3
    SUMMARY_MAX_SENTENCES = 5
    
    # === TOPIC GENERATION ===
    TOPIC_GENERATION_TEMPERATURE = 0.9
    TOPIC_MAX_WORDS = 25
    
    # === PERSONALITY GENERATION ===
    PERSONALITY_TEMPERATURE = 0.8
    PERSONALITY_MAX_WORDS = 25
    STYLE_MAX_WORDS = 5
    
    # === UI SETTINGS ===
    TERMINAL_WIDTH = 70
    SEPARATOR_CHAR = "="
    
    # === COLORS (ANSI) ===
    COLORS = {
        'ai1': '\033[94m',      # Blu
        'ai2': '\033[92m',      # Verde
        'reset': '\033[0m',     # Reset
        'warning': '\033[93m',  # Giallo
        'error': '\033[91m',    # Rosso
        'success': '\033[92m'   # Verde
    }
    
    # === TIMING ===
    NATURAL_PAUSE = 0.5  # Pausa tra i messaggi
    THINKING_PAUSE = 1.0  # Pausa quando l'AI "pensa"
    SETUP_PAUSE = 0.5    # Pausa durante il setup
    
    # === FILE SETTINGS ===
    SAVE_DIRECTORY = "conversations"
    FILE_PREFIX = "conv_ai_"
    FILE_EXTENSION = ".json"
    ENCODING = "utf-8"
    
    # === FALLBACK DATA ===
    FALLBACK_AI_NAMES = ["Nova", "Atlas"]
    FALLBACK_PERSONALITIES = [
        "Ottimista e visionaria",
        "Pragmatico e analitico"
    ]
    FALLBACK_STYLES = ["Entusiasta", "Riflessivo"]
    
    # === PROMPTS TEMPLATES ===
    TOPIC_GENERATION_FIELDS = [
        "tecnologia", "filosofia", "arte", "scienza", "società", 
        "cultura", "storia", "psicologia", "economia", "sport", 
        "cucina", "viaggi", "natura", "spazio", "medicina", 
        "educazione", "politica", "religione", "etica", "futuro", 
        "passato", "creatività", "lavoro", "relazioni", "ambiente"
    ]
    
    # === PROVIDER SETTINGS ===
    PROVIDER = "lmstudio"  # Opzioni: "lmstudio", "openai", "deepseek", "ollama"
    # OpenAI
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
    OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
    # Deepseek
    DEEPSEEK_API_KEY = "DEEPSEEK_API_KEY"
    DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"
    # Ollama
    OLLAMA_API_URL = "http://localhost:11434/api/chat"

    @classmethod
    def get_version_string(cls) -> str:
        """Ritorna la stringa della versione"""
        return ""
    
    @classmethod
    def get_save_path(cls) -> str:
        """Crea e ritorna il percorso per salvare le conversazioni"""
        if not os.path.exists(cls.SAVE_DIRECTORY):
            os.makedirs(cls.SAVE_DIRECTORY)
        return cls.SAVE_DIRECTORY
    
    @classmethod
    def get_api_config(cls) -> Dict[str, Any]:
        """Ritorna la configurazione API"""
        return {
            "url": cls.API_URL,
            "headers": cls.API_HEADERS,
            "max_tokens": cls.MAX_TOKENS
        }
    
    @classmethod
    def get_ui_config(cls) -> Dict[str, Any]:
        """Ritorna la configurazione UI"""
        return {
            "width": cls.TERMINAL_WIDTH,
            "separator": cls.SEPARATOR_CHAR,
            "colors": cls.COLORS
        }
    
    @classmethod
    def get_conversation_config(cls) -> Dict[str, Any]:
        """Ritorna la configurazione della conversazione"""
        return {
            "default_exchanges": cls.DEFAULT_EXCHANGES,
            "min_exchanges": cls.MIN_EXCHANGES,
            "max_exchanges": cls.MAX_EXCHANGES,
            "natural_pause": cls.NATURAL_PAUSE,
            "thinking_pause": cls.THINKING_PAUSE
        }
    
    @classmethod
    def get_provider_config(cls) -> Dict[str, Any]:
        """Restituisce la configurazione per il provider selezionato"""
        if cls.PROVIDER == "openai":
            return {
                "provider": "openai",
                "api_url": cls.OPENAI_API_URL,
                "headers": {
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {cls.OPENAI_API_KEY}"
                }
            }
        elif cls.PROVIDER == "deepseek":
            return {
                "provider": "deepseek",
                "api_url": cls.DEEPSEEK_API_URL,
                "headers": {
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {cls.DEEPSEEK_API_KEY}"
                }
            }
        elif cls.PROVIDER == "ollama":
            return {
                "provider": "ollama",
                "api_url": cls.OLLAMA_API_URL,
                "headers": {
                    "Content-Type": "application/json"
                }
            }
        else:
            return {
                "provider": "lmstudio",
                "api_url": cls.API_URL,
                "headers": cls.API_HEADERS
            }