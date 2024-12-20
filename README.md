# Föreningsdataanalys

Ett projekt för analys av föreningsdata, avvikelse- och riskanalys samt protokollanalys med hjälp av maskininlärning och textanalys.

## Funktioner
- **Avvikelseanalys:** Identifierar avvikelser i föreningars aktiviteter, medlemmar och ekonomiska bidrag.
- **Riskanalys:** Upptäcker riskfyllda föreningar med hjälp av maskininlärning (Isolation Forest och Random Forest).
- **Protokollanalys:** Analyserar mötesprotokoll för att säkerställa fullständighet och identifiera problematiskt innehåll.

## Installation
1. Klona projektet:
    ```bash
    git clone <repo-url>
    cd föreningsdataanalys
    ```

2. Skapa och aktivera en virtuell miljö:
    ```bash
    python -m venv venv
    source venv/bin/activate  # Linux/Mac
    venv\Scripts\activate     # Windows
    ```

3. Installera beroenden:
    ```bash
    pip install -r requirements.txt
    ```

4. Starta applikationen:
    ```bash
    streamlit run app.py
    ```

## Projektstruktur
Föreningsdataanalys/ │ ├── app.py # Huvudapplikation för Streamlit ├── risk_analysis.py # Riskanalysmodul ├── meeting_analysis.py # Protokollanalysmodul ├── data_analysis.py # Analys av föreningsdata ├── föreningsdata.csv # Exempeldata för analys ├── protokoll_f1.txt # Exempelprotokoll 1 ├── protokoll_f2.txt # Exempelprotokoll 2 ├── requirements.txt # Lista över Python-beroenden └── README.md # Projektbeskrivning


## Användning
- Ladda upp föreningsdata i CSV-format för att utföra avvikelseanalys.
- Utför riskanalys med hjälp av maskininlärningsmodeller.
- Analysera mötesprotokoll i textformat (.txt).

## Testning
- Testa moduler genom att använda exempeldata (t.ex. `föreningsdata.csv`, `protokoll_f1.txt`).
- Se `app.py` för att utföra analyser via Streamlit-gränssnittet.

## Licens
Projektet är licensierat under MIT-licensen.
