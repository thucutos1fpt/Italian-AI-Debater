"""
File principale per il Sistema di Conversazione AI
"""

from config import Config
from conversation_manager import ConversationManager
from ui_manager import UIManager

def main():
    """Funzione principale per eseguire il programma"""
    # Inizializza i componenti
    ui = UIManager()
    manager = ConversationManager()
    
    # Mostra banner di avvio
    ui.show_startup_banner()
    
    # Verifica la connessione all'API
    if not manager.test_api_connection():
        ui.wait_for_user("Premi INVIO per uscire...")
        return
    
    # Pulisci lo schermo per la configurazione
    ui.wait_for_user("Premi INVIO per continuare con la configurazione...")
    ui.clear_screen()
    
    ui.print_section("⚙️  CONFIGURAZIONE CONVERSAZIONE", 50)
    
    # Chiedi il numero di scambi
    num_exchanges = ui.get_user_input(
        f"📝 Numero di scambi nella conversazione",
        "int",
        default=Config.DEFAULT_EXCHANGES
    )
    
    # Validazione del numero di scambi
    if num_exchanges is None:
        ui.print_warning("Operazione annullata")
        return
    
    num_exchanges = max(Config.MIN_EXCHANGES, 
                       min(num_exchanges, Config.MAX_EXCHANGES))
    
    ui.print_success(f"Configurato per {num_exchanges} scambi")
    
    # Esegui la conversazione
    setup_data = None
    try:
        setup_data = manager.run_conversation(num_exchanges=num_exchanges)
    except KeyboardInterrupt:
        print("\n")
        ui.print_warning("Conversazione interrotta dall'utente")
    except Exception as e:
        ui.print_error(f"Errore durante la conversazione: {e}")
    
    # Salvataggio
    if setup_data:
        manager.save_conversation_if_requested(setup_data)
    
    # Messaggio di chiusura
    print(f"\n👋 Grazie per aver usato il Sistema di Conversazione AI!")
    print("=" * 60)
    ui.wait_for_user("Premi INVIO per uscire...")

if __name__ == "__main__":
    main()