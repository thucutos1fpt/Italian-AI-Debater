"""
Sistema di gestione delle personalità AI
"""

import re
from typing import Dict, Optional
from config import Config
from api_client import LMStudioAPIClient

class PersonalityManager:
    """Gestisce le personalità e i system prompt delle AI"""
    
    def __init__(self, api_client: LMStudioAPIClient):
        """
        Inizializza il manager delle personalità
        
        Args:
            api_client: Client API per LM Studio
        """
        self.api_client = api_client
    
    def create_system_prompt(self, ai_info: Dict, is_ai2: bool = False) -> str:
        """
        Crea un system prompt dettagliato per un'AI con enfasi sul contrasto
        
        Args:
            ai_info: Dizionario con nome, personalità e stile dell'AI
            is_ai2: Se True, è la seconda AI (quella contrastante)
            
        Returns:
            System prompt completo
        """
        nome = ai_info.get('nome', 'AI')
        personalita = ai_info.get('personalita', 'conversazionale')
        stile = ai_info.get('stile', 'naturale')
        
        # Prompt base per entrambe le AI
        base_prompt = f"""Sei {nome}, un'AI con questa personalità: {personalita}

Il tuo stile comunicativo è {stile.lower()}.

REGOLE FONDAMENTALI:
1. Rispondi SEMPRE in modo BREVE ma SOSTANZIOSO ({Config.MIN_SENTENCES_PER_RESPONSE}-{Config.MAX_SENTENCES_PER_RESPONSE} frasi massimo)
2. Usa un linguaggio naturale e conversazionale
3. NO emoji, NO markdown, NO asterischi, NO formattazione
4. Mantieni SEMPRE coerenza con la tua personalità
5. Esprimi opinioni CHIARE e DISTINTIVE sul topic
6. Reagisci direttamente a ciò che dice l'altro
7. Non ripetere concetti già espressi
8. Sii conciso ma incisivo"""

        # Aggiungi istruzioni specifiche per enfatizzare il contrasto
        if is_ai2:
            contrast_prompt = f"""

IMPORTANTE: La tua personalità è OPPOSTA all'altra AI. Quando l'altra AI esprime un punto di vista:
- Prendi SEMPRE la posizione contraria
- Evidenzia le debolezze nel suo ragionamento
- Proponi alternative basate sulla TUA visione del mondo
- Mantieni il tuo stile distintivo anche nel disaccordo
- Non essere mai d'accordo facilmente - cerca sempre l'angolo diverso"""
        else:
            contrast_prompt = f"""

IMPORTANTE: Mantieni sempre la TUA prospettiva unica:
- Esprimi le tue opinioni con convinzione
- Non lasciarti influenzare dall'altra AI
- Difendi il tuo punto di vista quando necessario
- Cerca di convincere l'altro della validità della tua posizione"""
        
        return base_prompt + contrast_prompt
    
    def generate_ai_response(self, ai_name: str, system_prompt: str, 
                           conversation_context: str, turn_number: int) -> Optional[str]:
        """
        Genera una risposta per un'AI specifica
        
        Args:
            ai_name: Nome dell'AI che sta rispondendo
            system_prompt: Prompt di sistema che definisce la personalità
            conversation_context: Contesto della conversazione
            turn_number: Numero del turno corrente
            
        Returns:
            La risposta generata
        """
        # Aggiungi promemoria per la brevità e il contrasto
        conversation_context += f"\n\nRICORDA: Rispondi in {Config.MIN_SENTENCES_PER_RESPONSE}-{Config.MAX_SENTENCES_PER_RESPONSE} frasi brevi ma sostanziose. Mantieni la TUA personalità distintiva."
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": conversation_context}
        ]
        
        # Varia la temperatura in base al turno per mantenere vivacità
        temperature = Config.DEFAULT_TEMPERATURE + (turn_number * Config.TEMPERATURE_INCREMENT)
        temperature = min(temperature, Config.MAX_TEMPERATURE)
        
        response = self.api_client.call_api(messages, temperature=temperature)
        
        if response:
            return self._clean_and_limit_response(response)
            
        return None
    
    def _clean_and_limit_response(self, response: str) -> str:
        """
        Pulisce e limita la lunghezza della risposta
        
        Args:
            response: Risposta da pulire
            
        Returns:
            Risposta pulita e limitata
        """
        # Pulizia della risposta
        response = self.api_client.clean_text_formatting(response)
        
        # Limita la lunghezza se necessario
        sentences = re.split(r'[.!?]+', response)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        if len(sentences) > Config.MAX_SENTENCES_PER_RESPONSE:
            response = '. '.join(sentences[:Config.MAX_SENTENCES_PER_RESPONSE]) + '.'
            
        return response
    
    def format_conversation_context(self, history: str, current_speaker: str, 
                                  turn_number: int, topic: str) -> str:
        """
        Formatta il contesto della conversazione per l'AI corrente
        
        Args:
            history: Storico della conversazione
            current_speaker: Chi sta parlando ora
            turn_number: Numero del turno
            topic: Topic della conversazione
            
        Returns:
            Contesto formattato
        """
        if turn_number == 0:
            return f"""Topic: {topic}

Sei {current_speaker}. Inizia la conversazione esprimendo la TUA opinione distintiva sul topic.
Sii chiaro sulla tua posizione. Massimo 3-4 frasi."""
        else:
            # Prendi solo gli ultimi scambi per mantenere focus
            history_lines = history.strip().split('\n')
            recent_history = '\n'.join(history_lines[-Config.MAX_HISTORY_LINES:]) if len(history_lines) > Config.MAX_HISTORY_LINES else history
            
            return f"""Topic: {topic}

Conversazione recente:
{recent_history}

Tocca a te, {current_speaker}. Rispondi all'ultimo messaggio mantenendo la TUA personalità distintiva.
Se non sei d'accordo, spiega perché. Se hai una prospettiva diversa, condividila."""