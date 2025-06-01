"""
Gestione dell'interfaccia utente e output
"""

import os
import time
from typing import Dict, Any, List
from config import Config

class UIManager:
    """Gestisce l'interfaccia utente e l'output"""
    
    def __init__(self):
        """Inizializza il manager UI"""
        self.colors = Config.COLORS
        self.width = Config.TERMINAL_WIDTH
        self.separator = Config.SEPARATOR_CHAR
    
    def clear_screen(self):
        """Pulisce lo schermo del terminale"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_header(self, title: str, subtitle: str = None):
        """
        Stampa un header formattato
        
        Args:
            title: Titolo principale
            subtitle: Sottotitolo opzionale
        """
        print(f"\n{self.separator * self.width}")
        print(f"{title}")
        print(f"{self.separator * self.width}")
        if subtitle:
            print(f"\n{subtitle}")
    
    def print_section(self, title: str, width: int = 50):
        """
        Stampa una sezione con separatori
        
        Args:
            title: Titolo della sezione
            width: Larghezza del separatore
        """
        print(f"\n{title}")
        print(self.separator * width)
    
    def print_colored(self, text: str, color_key: str):
        """
        Stampa testo colorato
        
        Args:
            text: Testo da stampare
            color_key: Chiave del colore dalla config
        """
        color = self.colors.get(color_key, '')
        reset = self.colors.get('reset', '')
        print(f"{color}{text}{reset}")
    
    def print_ai_message(self, ai_name: str, message: str, ai_number: int):
        """
        Stampa un messaggio dell'AI con colori
        
        Args:
            ai_name: Nome dell'AI
            message: Messaggio da stampare
            ai_number: Numero dell'AI (1 o 2) per i colori
        """
        color_key = 'ai1' if ai_number == 1 else 'ai2'
        color = self.colors.get(color_key, '')
        reset = self.colors.get('reset', '')
        print(f"{color}{ai_name}{reset}: {message}")
    
    def print_thinking(self, ai_name: str):
        """
        Mostra che l'AI sta pensando
        
        Args:
            ai_name: Nome dell'AI che sta pensando
        """
        print(f"💭 {ai_name} sta pensando...")
        time.sleep(Config.THINKING_PAUSE)
    
    def print_error(self, message: str):
        """
        Stampa un messaggio di errore
        
        Args:
            message: Messaggio di errore
        """
        self.print_colored(f"❌ {message}", 'error')
    
    def print_warning(self, message: str):
        """
        Stampa un messaggio di warning
        
        Args:
            message: Messaggio di warning
        """
        self.print_colored(f"⚠️  {message}", 'warning')
    
    def print_success(self, message: str):
        """
        Stampa un messaggio di successo
        
        Args:
            message: Messaggio di successo
        """
        self.print_colored(f"✅ {message}", 'success')
    
    def print_info(self, message: str):
        """
        Stampa un messaggio informativo
        
        Args:
            message: Messaggio informativo
        """
        print(f"ℹ️  {message}")
    
    def get_user_input(self, prompt: str, input_type: str = "string", 
                      choices: List[str] = None, default: Any = None) -> Any:
        """
        Ottiene input dall'utente con validazione
        
        Args:
            prompt: Prompt da mostrare
            input_type: Tipo di input ("string", "int", "choice", "bool")
            choices: Lista di scelte valide per input_type="choice"
            default: Valore di default
            
        Returns:
            Input dell'utente validato
        """
        while True:
            try:
                if default is not None:
                    user_input = input(f"{prompt} (default {default}): ").strip()
                    if not user_input:
                        return default
                else:
                    user_input = input(f"{prompt}: ").strip()
                
                if input_type == "string":
                    return user_input
                
                elif input_type == "int":
                    return int(user_input)
                
                elif input_type == "choice":
                    if choices and user_input in choices:
                        return user_input
                    else:
                        self.print_error(f"Scelta non valida. Opzioni: {', '.join(choices)}")
                        continue
                
                elif input_type == "bool":
                    return user_input.lower() in ['s', 'si', 'sì', 'y', 'yes', '1', 'true']
                
                else:
                    return user_input
                    
            except ValueError:
                self.print_error("Input non valido. Riprova.")
            except KeyboardInterrupt:
                print("\n")
                self.print_warning("Operazione annullata dall'utente")
                return None
    
    def show_topic_selection(self) -> str:
        """
        Mostra il menu di selezione del topic
        
        Returns:
            Scelta dell'utente ("1" o "2")
        """
        self.print_section("📝 SCEGLI IL TOPIC", 40)
        print("1. Genera automaticamente un topic")
        print("2. Inserisci un topic personalizzato")
        
        return self.get_user_input("Scegli (1 o 2)", "choice", ["1", "2"], default="1")
    
    def show_conversation_summary(self, topic: str, ai1_info: Dict, ai2_info: Dict, 
                                num_exchanges: int):
        """
        Mostra il riepilogo della conversazione prima di iniziare
        
        Args:
            topic: Topic della conversazione
            ai1_info: Informazioni della prima AI
            ai2_info: Informazioni della seconda AI
            num_exchanges: Numero di scambi previsti
        """
        self.clear_screen()
        self.print_section("📋 RIEPILOGO CONVERSAZIONE", 50)
        print(f"\n🎯 Topic: {topic}")
        print(f"\n👤 {ai1_info.get('nome', 'AI1')}: {ai1_info.get('personalita', 'N/A')}")
        print(f"👤 {ai2_info.get('nome', 'AI2')}: {ai2_info.get('personalita', 'N/A')}")
        print(f"\n💬 Scambi previsti: {num_exchanges}")
    
    def show_conversation_header(self, topic: str, ai1_info: Dict, ai2_info: Dict):
        """
        Mostra l'header della conversazione in corso
        
        Args:
            topic: Topic della conversazione
            ai1_info: Informazioni della prima AI
            ai2_info: Informazioni della seconda AI
        """
        self.print_header("🎭 CONVERSAZIONE AI IN CORSO")
        print(f"\n📌 TOPIC: {topic}")
        print(f"\n👤 PARTECIPANTI:")
        print(f"   • {ai1_info.get('nome', 'AI1')}: {ai1_info.get('personalita', 'N/A')}")
        print(f"   • {ai2_info.get('nome', 'AI2')}: {ai2_info.get('personalita', 'N/A')}")
        print(f"\n{self.separator * self.width}\n")
    
    def show_conversation_end(self, summary: str = None, stats: Dict = None, winner: str = None, winner_reason: str = None, ai1_name: str = None, ai2_name: str = None):
        """
        Mostra la conclusione della conversazione con riassunto, motivazione e vincitore colorato
        
        Args:
            summary: Riassunto della conversazione
            stats: Statistiche della conversazione
            winner: Nome del vincitore del dibattito
            winner_reason: Motivazione della scelta
            ai1_name: Nome della prima AI
            ai2_name: Nome della seconda AI
        """
        self.print_header("✨ CONVERSAZIONE CONCLUSA")

        # Riassunto
        if summary:
            self.print_section("📝 RIASSUNTO CONVERSAZIONE", 40)
            print(summary)
        else:
            self.print_warning("Impossibile generare il riassunto della conversazione.")

        # Vincitore con motivazione
        if winner and winner_reason:
            self.print_section("🏆 VINCITORE DEL DIBATTITO", 40)
            # Evidenzia entrambi i nomi nella motivazione
            evidenziato = winner_reason
            if ai1_name:
                evidenziato = evidenziato.replace(ai1_name, f"{self.colors['ai1']}{ai1_name}{self.colors['reset']}")
            if ai2_name:
                evidenziato = evidenziato.replace(ai2_name, f"{self.colors['ai2']}{ai2_name}{self.colors['reset']}")
            print(evidenziato)
        elif winner_reason:
            self.print_section("🏆 VINCITORE DEL DIBATTITO", 40)
            print(winner_reason)
        else:
            self.print_warning("Impossibile determinare il vincitore del dibattito.")

        # Statistiche
        if stats:
            self.print_section("📊 STATISTICHE", 40)
            for key, value in stats.items():
                print(f"   • {key}: {value}")
    
    def show_api_connection_test(self):
        """Mostra il test di connessione all'API"""
        self.print_info("Verifica connessione all'API di LM Studio...")
    
    def show_api_connection_error(self):
        """Mostra errore di connessione all'API"""
        self.print_error("ERRORE: Impossibile connettersi all'API di LM Studio.")
        print("\n📋 Checklist:")
        print("   ✓ LM Studio è in esecuzione?")
        print("   ✓ Un modello è caricato?")
        print("   ✓ Il server API è attivo sulla porta 1234?")
        print("\n💡 Suggerimento: Controlla le impostazioni del server in LM Studio")
    
    def show_startup_banner(self):
        """Mostra il banner di avvio"""
        self.clear_screen()
        print(f"\n🤖 SISTEMA DI CONVERSAZIONE AI COMPLETAMENTE GENERATIVO 🤖")
        print("=" * 60)
        print(Config.get_version_string())
    
    def wait_for_user(self, message: str = "Premi INVIO per continuare..."):
        """
        Aspetta che l'utente prema INVIO
        
        Args:
            message: Messaggio da mostrare
        """
        input(f"\n{message}")
    
    def natural_pause(self):
        """Pausa naturale tra i messaggi"""
        time.sleep(Config.NATURAL_PAUSE)
    
    def setup_pause(self):
        """Pausa durante il setup"""
        time.sleep(Config.SETUP_PAUSE)