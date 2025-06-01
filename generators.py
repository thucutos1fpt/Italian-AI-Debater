"""
Generatori per topic, personalità e riassunti
"""

import re
from typing import Optional, Tuple, Dict
from config import Config
from api_client import LMStudioAPIClient

class AIGenerators:
    """Classe per generare contenuti tramite AI"""
    
    def __init__(self, api_client: LMStudioAPIClient):
        """
        Inizializza i generatori
        
        Args:
            api_client: Client API per LM Studio
        """
        self.api_client = api_client
    
    def generate_topic(self) -> Optional[str]:
        """
        Genera un topic casuale per la conversazione, con maggiore varietà, creatività e originalità
        
        Returns:
            Topic generato o None in caso di errore
        """
        fields_list = ", ".join(Config.TOPIC_GENERATION_FIELDS)
        
        messages = [
            {
                "role": "system",
                "content": (
                    "Sei un generatore di argomenti di conversazione ESTREMAMENTE creativo, sorprendente e originale. "
                    "La tua missione è proporre argomenti che siano insoliti, interdisciplinari, provocatori, universali o anche astratti, "
                    "spaziando tra scienza, arte, filosofia, futuro, misteri, paradossi, cultura pop, etica, tecnologia, natura, psicologia, storia, società, e altro. "
                    "Evita argomenti banali, già sentiti o troppo specifici. "
                    "Cerca sempre la massima varietà e novità."
                )
            },
            {
                "role": "user",
                "content": f"""Genera UN SOLO argomento di conversazione che sia:
- Originale, sorprendente o fuori dagli schemi
- Adatto a stimolare opinioni diverse e dibattito
- Possibilmente interdisciplinare o universale
- Da QUALSIASI campo: {fields_list}, ma anche combinando più campi

Rispondi SOLO con l'argomento, niente altro. Mantienilo sotto le {Config.TOPIC_MAX_WORDS} parole.

Esempi di varietà:
- Se la memoria potesse essere trasferita tra esseri umani, cosa cambierebbe nella società?
- L'esistenza di universi paralleli può influenzare le nostre scelte morali?
- L'arte generata da intelligenze artificiali può essere davvero considerata "creativa"?
- Il tempo è una costruzione della mente o una realtà oggettiva?
- Le emozioni degli animali sono paragonabili a quelle umane?
- Cosa accadrebbe se la privacy non esistesse più in nessuna forma?
- Il linguaggio plasma la realtà o la realtà plasma il linguaggio?
- L'immortalità sarebbe un dono o una condanna?"""
            }
        ]
        
        topic = self.api_client.call_api(
            messages,
            temperature=1.2  # temperatura più alta per massima creatività
        )
        
        if topic:
            # Rimuovi eventuali punti finali o formattazioni extra
            topic = topic.strip().rstrip('.')
            return topic
        return None
    
    def generate_ai_profiles(self, topic: str) -> Optional[Tuple[Dict, Dict]]:
        """
        Genera nomi e personalità per entrambe le AI con personalità contrastanti, in modo più creativo e vario ma mantenendo la struttura e il parsing attuale.
        
        Args:
            topic: Topic della conversazione
            
        Returns:
            Tupla con i profili delle due AI o None in caso di errore
        """
        messages = [
            {
                "role": "system",
                "content": (
                    "Sei un creatore di personalità AI molto creativo e fantasioso. "
                    "Genera sempre due AI con nomi evocativi, anche inventati, e personalità radicalmente opposte. "
                    "Le personalità devono essere originali, memorabili, ispirate anche a concetti astratti, mitologici, filosofici, artistici, scientifici, letterari, ecc. "
                    "Evita nomi e descrizioni banali o troppo simili. "
                    "La seconda AI deve essere sempre l'opposto della prima in ogni aspetto. "
                    "Rispetta SEMPRE il formato richiesto."
                )
            },
            {
                "role": "user",
                "content": f"""Crea due personalità AI COMPLETAMENTE OPPOSTE per discutere di: {topic}

Per ogni AI genera:
1. Un nome evocativo, originale, anche inventato (no nomi comuni, no asterischi)
2. Una personalità distintiva e sorprendente (max {Config.PERSONALITY_MAX_WORDS} parole) che rappresenti un estremo
3. Uno stile comunicativo unico (max {Config.STYLE_MAX_WORDS} parole)

Le due AI devono essere in TOTALE CONTRASTO tra loro su:
- Visione del mondo (es: razionale vs mistica, ottimista vs nichilista, umano-centrica vs aliena, ecc)
- Approccio (logico vs intuitivo, pragmatico vs visionario, ecc)
- Stile comunicativo (diretto vs enigmatico, poetico vs tecnico, ecc)
- Valori, emozioni, atteggiamento, metodo, ecc

Rispetta questo formato:
NOME1: [nome evocativo]
PERSONALITA1: [descrizione che enfatizza un estremo]
STILE1: [stile comunicativo]
NOME2: [nome evocativo opposto]
PERSONALITA2: [descrizione che enfatizza l'estremo opposto]
STILE2: [stile comunicativo opposto]"""
            }
        ]
        response = self.api_client.call_api(
            messages,
            temperature=0.9  # temperatura alta per creatività e contrasto
        )
        if not response:
            return None
        return self._parse_ai_profiles(response)
    
    def _parse_ai_profiles(self, response: str) -> Optional[Tuple[Dict, Dict]]:
        """
        Parsing della risposta dei profili AI
        
        Args:
            response: Risposta dell'API da parsare
            
        Returns:
            Tupla con i profili parsati o None in caso di errore
        """
        try:
            lines = response.strip().split('\n')
            ai1_info = {}
            ai2_info = {}
            
            for line in lines:
                line = line.strip()
                if ':' in line:
                    key, value = line.split(':', 1)
                    key = key.strip().upper()
                    value = value.strip()
                    
                    if 'NOME1' in key:
                        ai1_info['nome'] = self.api_client.clean_ai_name(value)
                    elif 'PERSONALITA1' in key:
                        ai1_info['personalita'] = value
                    elif 'STILE1' in key:
                        ai1_info['stile'] = value
                    elif 'NOME2' in key:
                        ai2_info['nome'] = self.api_client.clean_ai_name(value)
                    elif 'PERSONALITA2' in key:
                        ai2_info['personalita'] = value
                    elif 'STILE2' in key:
                        ai2_info['stile'] = value
            
            # Validazione e fallback
            if ai1_info.get('nome') and ai2_info.get('nome'):
                return (ai1_info, ai2_info)
            else:
                return self._get_fallback_profiles()
                
        except Exception as e:
            print(f"{Config.COLORS['warning']}⚠️  Errore nel parsing dei profili: {e}{Config.COLORS['reset']}")
            return self._get_fallback_profiles()
    
    def _get_fallback_profiles(self) -> Tuple[Dict, Dict]:
        """
        Ritorna profili di fallback predefiniti
        
        Returns:
            Tupla con profili di fallback
        """
        return (
            {
                'nome': Config.FALLBACK_AI_NAMES[0], 
                'personalita': Config.FALLBACK_PERSONALITIES[0], 
                'stile': Config.FALLBACK_STYLES[0]
            },
            {
                'nome': Config.FALLBACK_AI_NAMES[1], 
                'personalita': Config.FALLBACK_PERSONALITIES[1], 
                'stile': Config.FALLBACK_STYLES[1]
            }
        )
    
    def generate_conversation_summary(self, conversation_history: list, topic: str) -> Optional[str]:
        """
        Genera un riassunto della conversazione
        
        Args:
            conversation_history: Storia della conversazione
            topic: Topic della conversazione
            
        Returns:
            Riassunto generato o None in caso di errore
        """
        if not conversation_history:
            return None
        
        # Costruisci il testo completo della conversazione
        conversation_text = ""
        for entry in conversation_history:
            conversation_text += f"{entry['speaker']}: {entry['message']}\n"
        
        messages = [
            {
                "role": "system",
                "content": "Sei un analista esperto che crea riassunti concisi di conversazioni. Scrivi sempre in modo chiaro e diretto, senza formattazione markdown o caratteri speciali."
            },
            {
                "role": "user",
                "content": f"""Riassumi brevemente questa conversazione tra due AI sul topic: {topic}

CONVERSAZIONE:
{conversation_text}

Crea un riassunto di massimo {Config.SUMMARY_MAX_SENTENCES} frasi che evidenzi:
1. I punti di vista principali di entrambe le AI
2. I contrasti emersi nella discussione
3. Gli argomenti chiave trattati

IMPORTANTE: 
- NON usare markdown, asterischi, trattini o formattazione
- Scrivi in modo naturale e scorrevole
- Mantieni un tono neutrale e obiettivo
- NON menzionare che sono AI, trattale come partecipanti normali"""
            }
        ]
        
        summary = self.api_client.call_api(
            messages, 
            temperature=Config.SUMMARY_TEMPERATURE
        )
        
        if summary:
            # Pulizia extra per rimuovere qualsiasi formattazione residua
            summary = self.api_client.clean_text_formatting(summary)
            return summary
        
        return None
    
    def generate_debate_winner(self, conversation_history: list, topic: str, ai1_name: str, ai2_name: str) -> Optional[dict]:
        """
        Determina il vincitore del dibattito tramite AI, obbligando la scelta di uno dei due nomi e fornendo una breve motivazione.
        
        Args:
            conversation_history: Storia della conversazione
            topic: Topic della conversazione
            ai1_name: Nome della prima AI
            ai2_name: Nome della seconda AI
            
        Returns:
            Dict con 'winner' (nome) e 'reason' (motivazione) oppure None
        """
        if not conversation_history:
            return None
        
        conversation_text = ""
        for entry in conversation_history:
            conversation_text += f"{entry['speaker']}: {entry['message']}\n"
        
        messages = [
            {
                "role": "system",
                "content": (
                    "Sei un giudice imparziale di dibattiti. Dopo un'attenta e lunga riflessione, devi stabilire chi ha vinto il dibattito tra due partecipanti. "
                    "Non puoi mai rispondere che è un pareggio, che non puoi decidere o che entrambi hanno vinto. Devi scegliere obbligatoriamente solo uno dei due nomi forniti. "
                    "Motiva brevemente la scelta, ma alla fine scrivi solo il nome del vincitore su una riga separata, senza alcuna formattazione, markdown, asterischi, trattini o simboli. "
                    "Non aggiungere altro dopo il nome."
                )
            },
            {
                "role": "user",
                "content": (
                    f"Topic: {topic}\n\nCONVERSAZIONE:\n{conversation_text}\n\nI partecipanti sono: {ai1_name} e {ai2_name}. "
                    f"Dopo una lunga riflessione, chi ha vinto il dibattito? Scrivi una breve motivazione, poi solo il nome del vincitore alla fine, senza formattazione."
                )
            }
        ]
        
        result = self.api_client.call_api(messages, temperature=0.2)
        
        if result:
            lines = [l.strip() for l in result.strip().split('\n') if l.strip()]
            if len(lines) < 2:
                return None
            winner = lines[-1]
            reason = ' '.join(lines[:-1])
            if winner in [ai1_name, ai2_name]:
                return {'winner': winner, 'reason': reason}
        
        return None