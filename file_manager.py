"""
Gestione del salvataggio e caricamento delle conversazioni
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional
from config import Config

class FileManager:
    """Gestisce il salvataggio e caricamento delle conversazioni"""
    
    def __init__(self):
        """Inizializza il manager dei file"""
        self.save_directory = Config.get_save_path()
        self.file_prefix = Config.FILE_PREFIX
        self.file_extension = Config.FILE_EXTENSION
        self.encoding = Config.ENCODING
    
    def save_conversation(self, conversation_data: Dict) -> Optional[str]:
        """
        Salva una conversazione su file
        
        Args:
            conversation_data: Dati della conversazione da salvare
            
        Returns:
            Nome del file salvato o None in caso di errore
        """
        try:
            timestamp = datetime.now()
            filename = f"{self.file_prefix}{timestamp.strftime('%Y%m%d_%H%M%S')}{self.file_extension}"
            filepath = os.path.join(self.save_directory, filename)
            
            with open(filepath, 'w', encoding=self.encoding) as f:
                json.dump(conversation_data, f, ensure_ascii=False, indent=2)
            
            return filename
            
        except Exception as e:
            print(f"❌ Errore nel salvataggio: {e}")
            return None
    
    def load_conversation(self, filename: str) -> Optional[Dict]:
        """
        Carica una conversazione da file
        
        Args:
            filename: Nome del file da caricare
            
        Returns:
            Dati della conversazione o None in caso di errore
        """
        try:
            filepath = os.path.join(self.save_directory, filename)
            
            with open(filepath, 'r', encoding=self.encoding) as f:
                return json.load(f)
                
        except Exception as e:
            print(f"❌ Errore nel caricamento: {e}")
            return None
    
    def list_saved_conversations(self) -> List[str]:
        """
        Lista tutte le conversazioni salvate
        
        Returns:
            Lista dei nomi dei file delle conversazioni
        """
        try:
            files = []
            for filename in os.listdir(self.save_directory):
                if filename.startswith(self.file_prefix) and filename.endswith(self.file_extension):
                    files.append(filename)
            return sorted(files, reverse=True)  # Più recenti prima
            
        except Exception:
            return []
    
    def get_file_info(self, filename: str) -> Dict:
        """
        Ottiene informazioni su un file di conversazione
        
        Args:
            filename: Nome del file
            
        Returns:
            Dizionario con informazioni sul file
        """
        try:
            filepath = os.path.join(self.save_directory, filename)
            stat = os.stat(filepath)
            
            return {
                'filename': filename,
                'size': stat.st_size,
                'created': datetime.fromtimestamp(stat.st_ctime),
                'modified': datetime.fromtimestamp(stat.st_mtime)
            }
            
        except Exception:
            return {}
    
    def create_conversation_data(self, topic: str, ai1_info: Dict, ai2_info: Dict, 
                               conversation_history: List[Dict]) -> Dict:
        """
        Crea la struttura dati per salvare una conversazione
        
        Args:
            topic: Topic della conversazione
            ai1_info: Informazioni della prima AI
            ai2_info: Informazioni della seconda AI
            conversation_history: Storia della conversazione
            
        Returns:
            Struttura dati completa per il salvataggio
        """
        timestamp = datetime.now()
        
        return {
            "metadata": {
                "timestamp": timestamp.isoformat(),
                "version": Config.VERSION,
                "topic": topic,
                "participants": {
                    "ai1": {
                        "name": ai1_info.get('nome', ''),
                        "personality": ai1_info.get('personalita', ''),
                        "style": ai1_info.get('stile', '')
                    },
                    "ai2": {
                        "name": ai2_info.get('nome', ''),
                        "personality": ai2_info.get('personalita', ''),
                        "style": ai2_info.get('stile', '')
                    }
                },
                "total_turns": len(conversation_history),
                "total_characters": sum(len(entry.get('message', '')) for entry in conversation_history)
            },
            "conversation": conversation_history
        }
    
    def get_conversation_stats(self, conversation_data: Dict) -> Dict:
        """
        Calcola statistiche da una conversazione
        
        Args:
            conversation_data: Dati della conversazione
            
        Returns:
            Dizionario con le statistiche
        """
        metadata = conversation_data.get('metadata', {})
        conversation = conversation_data.get('conversation', [])
        
        # Conteggi per AI
        ai1_name = metadata.get('participants', {}).get('ai1', {}).get('name', 'AI1')
        ai2_name = metadata.get('participants', {}).get('ai2', {}).get('name', 'AI2')
        
        ai1_messages = [entry for entry in conversation if entry.get('speaker') == ai1_name]
        ai2_messages = [entry for entry in conversation if entry.get('speaker') == ai2_name]
        total_characters = metadata.get('total_characters', 0)
        # Stima durata in secondi (20 caratteri/sec)
        estimated_duration_sec = int(total_characters / 20) if total_characters else 0
        
        return {
            'Turni completati': len(conversation),
            'Messaggi AI1': len(ai1_messages),
            'Messaggi AI2': len(ai2_messages),
            'Caratteri totali': total_characters,
            'Durata stimata (secondi)': estimated_duration_sec
        }