"""
Manager principale per gestire le conversazioni AI
"""

import time
from typing import Dict, Optional
from config import Config
from api_client import LMStudioAPIClient
from generators import AIGenerators
from personalities import PersonalityManager
from ui_manager import UIManager
from file_manager import FileManager

class ConversationManager:
    """Manager principale per le conversazioni AI"""
    
    def __init__(self):
        """Inizializza il manager della conversazione"""
        # Componenti principali
        self.api_client = LMStudioAPIClient()
        self.generators = AIGenerators(self.api_client)
        self.personality_manager = PersonalityManager(self.api_client)
        self.ui = UIManager()
        self.file_manager = FileManager()
        
        # Stato della conversazione
        self.conversation_history = []
        self.topic = None
        self.ai1_name = None
        self.ai2_name = None
        self.ai1_info = None
        self.ai2_info = None
        self.ai1_personality = None
        self.ai2_personality = None
    
    def test_api_connection(self) -> bool:
        """
        Testa la connessione all'API
        
        Returns:
            True se la connessione funziona, False altrimenti
        """
        self.ui.show_api_connection_test()
        
        if self.api_client.test_connection():
            self.ui.print_success("Connessione stabilita con successo!")
            return True
        else:
            self.ui.show_api_connection_error()
            return False
    
    def get_topic_from_user(self) -> Optional[str]:
        """
        Permette all'utente di scegliere o inserire un topic
        
        Returns:
            Topic scelto o None in caso di errore
        """
        choice = self.ui.show_topic_selection()
        
        if choice == '2':
            topic = self.ui.get_user_input("📌 Inserisci il topic", "string")
            if topic:
                return topic
            else:
                self.ui.print_warning("Topic vuoto, generazione automatica...")
        
        self.ui.print_info("Generazione automatica del topic...")
        return self.generators.generate_topic()
    
    def setup_conversation(self) -> Optional[Dict]:
        """
        Inizializza tutti gli elementi della conversazione
        
        Returns:
            Dati di setup o None in caso di errore
        """
        # Ottieni il topic
        self.topic = self.get_topic_from_user()
        if not self.topic:
            self.ui.print_error("Errore nella generazione del topic")
            return None
        
        self.ui.print_success(f"Topic impostato: {self.topic}")
        
        # Pulisci lo schermo prima di generare le personalità
        self.ui.wait_for_user("📋 Topic confermato. Premi INVIO per generare le personalità AI...")
        self.ui.clear_screen()
        
        self.ui.print_section("🤖 GENERAZIONE PERSONALITÀ AI", 50)
        print(f"\n📌 Topic: {self.topic}\n")
        
        self.ui.print_info("Creazione delle personalità AI...")
        profiles = self.generators.generate_ai_profiles(self.topic)
        if not profiles:
            self.ui.print_error("Errore nella generazione dei profili AI")
            return None
        
        self.ai1_info, self.ai2_info = profiles
        
        # Salva i nomi puliti
        self.ai1_name = self.ai1_info.get('nome', Config.FALLBACK_AI_NAMES[0])
        self.ai2_name = self.ai2_info.get('nome', Config.FALLBACK_AI_NAMES[1])
        
        self.ui.print_success(f"Personalità create per {self.ai1_name} e {self.ai2_name}")
        
        # Genera system prompts
        self.ui.print_info(f"Configurazione di {self.ai1_name}...")
        self.ai1_personality = self.personality_manager.create_system_prompt(self.ai1_info, is_ai2=False)
        self.ui.setup_pause()
        
        self.ui.print_info(f"Configurazione di {self.ai2_name}...")
        self.ai2_personality = self.personality_manager.create_system_prompt(self.ai2_info, is_ai2=True)
        self.ui.setup_pause()
        
        self.ui.print_success("Configurazione completata!")
        
        return {
            'topic': self.topic,
            'ai1': self.ai1_info,
            'ai2': self.ai2_info
        }
    
    def run_single_turn(self, turn_number: int, conversation_text: str) -> Optional[str]:
        """
        Esegue un singolo turno di conversazione
        
        Args:
            turn_number: Numero del turno
            conversation_text: Testo della conversazione fino ad ora
            
        Returns:
            Risposta generata o None in caso di errore
        """
        # Determina chi parla
        if turn_number % 2 == 0:
            current_ai = self.ai1_name
            current_prompt = self.ai1_personality
            ai_number = 1
        else:
            current_ai = self.ai2_name
            current_prompt = self.ai2_personality
            ai_number = 2
        
        # Indicatore visivo del turno
        color_key = 'ai1' if ai_number == 1 else 'ai2'
        color = Config.COLORS.get(color_key, '')
        reset = Config.COLORS.get('reset', '')
        print(f"{color}{current_ai}{reset}: ", end="", flush=True)
        
        # Costruisci il contesto
        context = self.personality_manager.format_conversation_context(
            conversation_text, current_ai, turn_number, self.topic
        )
        
        # Genera la risposta
        response = self.personality_manager.generate_ai_response(
            current_ai, current_prompt, context, turn_number
        )
        
        if response:
            print(response)
            self.conversation_history.append({
                "speaker": current_ai,
                "message": response,
                "turn": turn_number + 1
            })
            self.ui.natural_pause()
            return response
        else:
            self.ui.print_thinking(current_ai)
            # Riprova una volta
            response = self.personality_manager.generate_ai_response(
                current_ai, current_prompt, context, turn_number
            )
            if response:
                print(response)
                self.conversation_history.append({
                    "speaker": current_ai,
                    "message": response,
                    "turn": turn_number + 1
                })
                return response
            else:
                self.ui.print_error("Errore nella generazione")
                return None
    
    def run_conversation(self, num_exchanges: int = None) -> Optional[Dict]:
        """
        Esegue una conversazione completa tra due AI
        
        Args:
            num_exchanges: Numero di scambi nella conversazione
            
        Returns:
            Dati di setup per il salvataggio
        """
        if num_exchanges is None:
            num_exchanges = Config.DEFAULT_EXCHANGES
        
        # Setup iniziale
        setup_data = self.setup_conversation()
        if not setup_data:
            self.ui.print_error("Impossibile inizializzare la conversazione")
            return None
        
        # Mostra riepilogo e attendi conferma
        self.ui.show_conversation_summary(
            self.topic, self.ai1_info, self.ai2_info, num_exchanges
        )
        self.ui.wait_for_user("✅ Tutto pronto! Premi INVIO per iniziare la conversazione...")
        
        # Pulisci lo schermo e mostra header della conversazione
        self.ui.clear_screen()
        self.ui.show_conversation_header(self.topic, self.ai1_info, self.ai2_info)
        
        # Inizia la conversazione
        conversation_text = ""
        
        for i in range(num_exchanges):
            response = self.run_single_turn(i, conversation_text)
            if response:
                conversation_text += f"{self.conversation_history[-1]['speaker']}: {response}\n"
            else:
                break

        summary = self.generators.generate_conversation_summary(
            self.conversation_history, self.topic
        )

        winner_info = self.generators.generate_debate_winner(
            self.conversation_history, self.topic, self.ai1_name, self.ai2_name
        )

        stats = self.file_manager.get_conversation_stats(
            self.file_manager.create_conversation_data(
                self.topic, self.ai1_info, self.ai2_info, self.conversation_history
            )
        )

        self.ui.show_conversation_end(
            summary, stats, 
            winner=winner_info['winner'] if winner_info else None,
            winner_reason=winner_info['reason'] if winner_info else None,
            ai1_name=self.ai1_name, ai2_name=self.ai2_name
        )

        return setup_data
    
    def save_conversation_if_requested(self, setup_data: Dict) -> bool:
        """
        Chiede all'utente se salvare la conversazione e la salva se richiesto
        
        Args:
            setup_data: Dati di setup della conversazione
            
        Returns:
            True se salvata con successo, False altrimenti
        """
        print("\n" + "=" * 60)
        save_choice = self.ui.get_user_input(
            "💾 Vuoi salvare la conversazione? (s/n)", 
            "bool"
        )
        
        if save_choice:
            conversation_data = self.file_manager.create_conversation_data(
                self.topic, self.ai1_info, self.ai2_info, self.conversation_history
            )
            
            filename = self.file_manager.save_conversation(conversation_data)
            if filename:
                self.ui.print_success(f"Conversazione salvata in: {filename}")
                file_size = len(str(conversation_data))
                self.ui.print_info(f"Dimensione file: {file_size} caratteri")
                return True
            else:
                return False
        
        return False