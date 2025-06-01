"""
Client API per LM Studio
"""

import requests
import re
from typing import List, Dict, Optional
from config import Config

class LMStudioAPIClient:
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
    
    def clean_ai_name(self, name: str) -> str:
        """
        Pulisce il nome dell'AI da caratteri indesiderati
        
        Args:
            name: Nome da pulire
            
        Returns:
            Nome pulito
        """
        # Rimuovi asterischi, underscore e altri caratteri di formattazione
        cleaned = re.sub(r'[*_`~]', '', name)
        # Rimuovi spazi extra
        cleaned = ' '.join(cleaned.split())
        # Prendi solo la prima parola se ce ne sono multiple
        cleaned = cleaned.split()[0] if cleaned.split() else cleaned
        return cleaned.strip()
    
    def clean_text_formatting(self, text: str) -> str:
        """
        Rimuove la formattazione markdown e caratteri speciali
        
        Args:
            text: Testo da pulire
            
        Returns:
            Testo senza formattazione
        """
        # Rimuovi formattazione markdown
        text = re.sub(r'[*_`~#\-]', '', text)
        return text.strip()