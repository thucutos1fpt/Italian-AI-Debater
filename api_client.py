"""
Client API per LM Studio
"""

import requests
import re
from typing import List, Dict, Optional
from config import Config

class BaseAPIClient:
    """Interfaccia base per i client API"""
    def call_api(self, messages: List[Dict], temperature: float = None, max_tokens: int = None) -> Optional[str]:
        raise NotImplementedError
    def test_connection(self) -> bool:
        raise NotImplementedError
    def clean_ai_name(self, name: str) -> str:
        cleaned = re.sub(r'[*_`~]', '', name)
        cleaned = ' '.join(cleaned.split())
        cleaned = cleaned.split()[0] if cleaned.split() else cleaned
        return cleaned.strip()
    def clean_text_formatting(self, text: str) -> str:
        text = re.sub(r'[*_`~#\-]', '', text)
        return text.strip()

class LMStudioAPIClient(BaseAPIClient):
    """Client per interagire con l'API di LM Studio"""
    
    def __init__(self, api_url: str = None):
        """
        Inizializza il client API
        
        Args:
            api_url: URL dell'endpoint API (usa config se None)
        """
        self.api_url = api_url or Config.API_URL
        self.headers = Config.API_HEADERS.copy()
    
    def call_api(self, messages: List[Dict], 
                 temperature: float = None,
                 max_tokens: int = None) -> Optional[str]:
        """
        Effettua una chiamata all'API di LM Studio
        
        Args:
            messages: Lista di messaggi della conversazione
            temperature: Creatività della risposta (usa config se None)
            max_tokens: Numero massimo di token (usa config se None)
            
        Returns:
            La risposta dell'AI o None in caso di errore
        """
        if temperature is None:
            temperature = Config.DEFAULT_TEMPERATURE
        if max_tokens is None:
            max_tokens = Config.MAX_TOKENS
        
        data = {
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": False
        }
        
        try:
            response = requests.post(
                self.api_url,
                headers=self.headers,
                json=data
            )
            response.raise_for_status()
            
            result = response.json()
            content = result['choices'][0]['message']['content'].strip()
            
            # Rimuovi eventuali ripetizioni accidentali
            return self._clean_response(content)
            
        except requests.exceptions.ConnectionError:
            print(f"{Config.COLORS['error']}⚠️  Errore: Impossibile connettersi all'API di LM Studio{Config.COLORS['reset']}")
            return None
        except Exception as e:
            print(f"{Config.COLORS['error']}⚠️  Errore inaspettato: {e}{Config.COLORS['reset']}")
            return None
    
    def _clean_response(self, content: str) -> str:
        """
        Pulisce la risposta dell'API
        
        Args:
            content: Contenuto da pulire
            
        Returns:
            Contenuto pulito
        """
        lines = content.split('\n')
        cleaned_lines = []
        for line in lines:
            if not cleaned_lines or line.strip() != cleaned_lines[-1].strip():
                cleaned_lines.append(line)
        
        return '\n'.join(cleaned_lines)
    
    def test_connection(self) -> bool:
        """
        Testa la connessione all'API
        
        Returns:
            True se la connessione funziona, False altrimenti
        """
        test_response = self.call_api([
            {"role": "system", "content": "Rispondi solo OK"},
            {"role": "user", "content": "Test"}
        ])
        
        return test_response is not None

class OpenAIAPIClient(BaseAPIClient):
    def __init__(self, api_url: str = None, api_key: str = None):
        from config import Config
        cfg = Config.get_provider_config()
        self.api_url = api_url or cfg["api_url"]
        self.headers = cfg["headers"].copy()
    def call_api(self, messages: List[Dict], temperature: float = None, max_tokens: int = None) -> Optional[str]:
        from config import Config
        if temperature is None:
            temperature = Config.DEFAULT_TEMPERATURE
        if max_tokens is None:
            max_tokens = Config.MAX_TOKENS
        data = {
            "model": "gpt-3.5-turbo",
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens if max_tokens > 0 else None,
            "stream": False
        }
        try:
            response = requests.post(self.api_url, headers=self.headers, json=data)
            response.raise_for_status()
            result = response.json()
            content = result['choices'][0]['message']['content'].strip()
            return self._clean_response(content)
        except Exception as e:
            print(f"Errore OpenAI: {e}")
            return None
    def _clean_response(self, content: str) -> str:
        lines = content.split('\n')
        cleaned_lines = []
        for line in lines:
            if not cleaned_lines or line.strip() != cleaned_lines[-1].strip():
                cleaned_lines.append(line)
        return '\n'.join(cleaned_lines)
    def test_connection(self) -> bool:
        test_response = self.call_api([
            {"role": "system", "content": "Rispondi solo OK"},
            {"role": "user", "content": "Test"}
        ])
        return test_response is not None

class DeepseekAPIClient(BaseAPIClient):
    def __init__(self, api_url: str = None, api_key: str = None):
        from config import Config
        cfg = Config.get_provider_config()
        self.api_url = api_url or cfg["api_url"]
        self.headers = cfg["headers"].copy()
    def call_api(self, messages: List[Dict], temperature: float = None, max_tokens: int = None) -> Optional[str]:
        from config import Config
        if temperature is None:
            temperature = Config.DEFAULT_TEMPERATURE
        if max_tokens is None:
            max_tokens = Config.MAX_TOKENS
        data = {
            "model": "deepseek-chat",
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens if max_tokens > 0 else None,
            "stream": False
        }
        try:
            response = requests.post(self.api_url, headers=self.headers, json=data)
            response.raise_for_status()
            result = response.json()
            content = result['choices'][0]['message']['content'].strip()
            return self._clean_response(content)
        except Exception as e:
            print(f"Errore Deepseek: {e}")
            return None
    def _clean_response(self, content: str) -> str:
        lines = content.split('\n')
        cleaned_lines = []
        for line in lines:
            if not cleaned_lines or line.strip() != cleaned_lines[-1].strip():
                cleaned_lines.append(line)
        return '\n'.join(cleaned_lines)
    def test_connection(self) -> bool:
        test_response = self.call_api([
            {"role": "system", "content": "Rispondi solo OK"},
            {"role": "user", "content": "Test"}
        ])
        return test_response is not None

class OllamaAPIClient(BaseAPIClient):
    def __init__(self, api_url: str = None):
        from config import Config
        cfg = Config.get_provider_config()
        self.api_url = api_url or cfg["api_url"]
        self.headers = cfg["headers"].copy()
    def call_api(self, messages: List[Dict], temperature: float = None, max_tokens: int = None) -> Optional[str]:
        from config import Config
        if temperature is None:
            temperature = Config.DEFAULT_TEMPERATURE
        if max_tokens is None:
            max_tokens = Config.MAX_TOKENS
        data = {
            "model": "llama3",
            "messages": messages,
            "options": {"temperature": temperature},
            "stream": False
        }
        try:
            response = requests.post(self.api_url, headers=self.headers, json=data)
            response.raise_for_status()
            result = response.json()
            content = result['message']['content'].strip() if 'message' in result else result['choices'][0]['message']['content'].strip()
            return self._clean_response(content)
        except Exception as e:
            print(f"Errore Ollama: {e}")
            return None
    def _clean_response(self, content: str) -> str:
        lines = content.split('\n')
        cleaned_lines = []
        for line in lines:
            if not cleaned_lines or line.strip() != cleaned_lines[-1].strip():
                cleaned_lines.append(line)
        return '\n'.join(cleaned_lines)
    def test_connection(self) -> bool:
        test_response = self.call_api([
            {"role": "system", "content": "Rispondi solo OK"},
            {"role": "user", "content": "Test"}
        ])
        return test_response is not None

def get_api_client():
    from config import Config
    provider = Config.PROVIDER.lower()
    if provider == "openai":
        return OpenAIAPIClient()
    elif provider == "deepseek":
        return DeepseekAPIClient()
    elif provider == "ollama":
        return OllamaAPIClient()
    else:
        return LMStudioAPIClient()