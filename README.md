# Sistema di Conversazione AI

Un sistema generativo di dibattito tra due intelligenze artificiali, completamente personalizzabile, scritto in Python.

## Caratteristiche
- Generazione automatica di topic originali e creativi
- Creazione di personalità AI contrapposte e uniche
- Gestione di conversazioni strutturate tra due AI
- Riassunto automatico della conversazione e determinazione del vincitore
- Salvataggio e caricamento delle conversazioni
- Interfaccia utente testuale chiara e colorata
- Supporto a diversi provider di modelli AI (LM Studio, OpenAI, Deepseek, Ollama)

## Requisiti
- Python 3.10+
- [requests](https://pypi.org/project/requests/) (`pip install requests`)
- Un provider AI compatibile (es. LM Studio, OpenAI, Deepseek, Ollama)

## Installazione
1. **Clona il repository:**
   ```powershell
   git clone https://github.com/IDanK0/Italian-AI-Debater
   cd Italian-AI-Debater
   ```
2. **Installa le dipendenze:**
   ```powershell
   pip install requests
   ```
3. **Configura il provider AI:**
   - Modifica `config.py` per selezionare il provider desiderato e inserire eventuali chiavi API.
   - Esempio per OpenAI:
     ```python
     PROVIDER = "openai"
     OPENAI_API_KEY = "la-tua-chiave"
     ```

## Utilizzo
1. **Avvia il programma:**
   ```powershell
   python main.py
   ```
2. **Segui le istruzioni a schermo:**
   - Scegli/genera un topic
   - Genera le personalità AI
   - Avvia la conversazione
   - Visualizza riassunto, vincitore e statistiche
   - Salva la conversazione se desiderato

## Struttura del Progetto
- `main.py` — Avvio e gestione principale
- `config.py` — Configurazione centralizzata
- `conversation_manager.py` — Logica della conversazione
- `generators.py` — Generazione topic, personalità, riassunti
- `personalities.py` — Gestione personalità e prompt
- `ui_manager.py` — Interfaccia utente e output
- `file_manager.py` — Salvataggio/caricamento conversazioni
- `api_client.py` — Client per provider AI
- `conversations/` — Cartella con le conversazioni salvate

## Esempio di Output
```
🤖 SISTEMA DI CONVERSAZIONE AI COMPLETAMENTE GENERATIVO 🤖
============================================================
⚙️  CONFIGURAZIONE CONVERSAZIONE
...
🎯 Topic: L'esistenza di universi paralleli può influenzare le nostre scelte morali?
👤 Nova: Ottimista e visionaria
👤 Atlas: Pragmatico e analitico
💬 Scambi previsti: 7
...
🏆 Vincitore del dibattito: Nova
Motivazione: Ha argomentato con maggiore coerenza e originalità.
```

## Note
- Il sistema è pensato per uso didattico, creativo e di sperimentazione.
- Puoi personalizzare facilmente i prompt e le regole modificando i file Python.
- Per problemi o suggerimenti, apri una issue su GitHub.

## Licenza
Questo progetto è distribuito sotto licenza Apache 2.0. Vedi il file `LICENSE` per i dettagli.
