import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import re
from risk_analysis import risk_analysis_app


# Funktion för att beräkna relationer och avvikelser
def calculate_relation_changes(data):
    # Skapa nya kolumner för relationerna
    data['Activities per Member'] = data['activities'] / data['total_members']
    data['Grants per Activity'] = data['approved_grants'] / data['activities']
    data['Grants per Member'] = data['approved_grants'] / data['total_members']

    # Sortera och beräkna förändringar över år per förening
    data = data.sort_values(by=['id', 'year'])
    data['Activities per Member Change (%)'] = data.groupby('id')['Activities per Member'].pct_change() * 100
    data['Grants per Activity Change (%)'] = data.groupby('id')['Grants per Activity'].pct_change() * 100
    data['Grants per Member Change (%)'] = data.groupby('id')['Grants per Member'].pct_change() * 100

    return data

# Funktion för riskanalys baserat på historiska data
def train_risk_model(historical_data):
    # Förbered data
    X = historical_data[['activities', 'total_members', 'approved_grants']]
    y = historical_data['flagged']  # 1 om föreningen är flaggad, annars 0

    # Dela upp i tränings- och testdata
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Träna en Random Forest-modell
    model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train)

    # Utvärdera modellen
    y_pred = model.predict(X_test)
    st.subheader("Riskanalysmodellens prestanda")
    st.text(classification_report(y_test, y_pred))

    return model

# Funktion för att förutsäga risker i nya data
def predict_risks(model, new_data):
    X_new = new_data[['activities', 'total_members', 'approved_grants']]
    new_data['Risk Prediction'] = model.predict(X_new)
    new_data['Risk Level'] = new_data['Risk Prediction'].apply(lambda x: 'Hög' if x == 1 else 'Låg')
    return new_data

# Funktion för protokollanalys baserat på nyckelord
def analyze_meeting_minutes_simple(text):
    # Fördefinierade nyckelord för varje avsnitt
    required_sections = {
        "Datum och plats": [r"(datum|plats|tid)", "När och var mötet ägde rum."],
        "Mötesdeltagare": [r"(närvarande|deltagare|närvarolista)", "Lista över deltagare."],
        "Dagordning": [r"(dagordning|agenda)", "Dagordningen för mötet."],
        "Verksamhetsberättelse": [r"(verksamhetsberättelse|årsberättelse)", "Redogörelse för verksamhetsåret."],
        "Ekonomisk rapport": [r"(ekonomi|budget|ekonomisk rapport)", "Ekonomisk rapportering."],
        "Ansvarsfrihet": [r"(ansvarsfrihet|ansvarsbefrielse)", "Ansvarsfrihet för styrelsen."],
        "Val av styrelse": [r"(val av styrelse|ny styrelse)", "Val av ny styrelse."],
        "Övriga frågor": [r"(övriga frågor|övrigt)", "Övriga frågor som diskuterades."],
    }

    # Kontrollera om varje avsnitt finns
    results = {}
    for section, (pattern, explanation) in required_sections.items():
        if re.search(pattern, text, re.IGNORECASE):
            results[section] = "✅ Hittad"
        else:
            results[section] = f"❌ Saknas ({explanation})"

    return results

# Streamlit-app
def main():
    st.title("Avvikelse-, risk- och protokollanalys för föreningsdata")

    # Val av analys
    page = st.sidebar.radio("Välj analysverktyg:", ["Avvikelseanalys", "Riskanalys"]) # Removed , "Protokollanalys"

    if page == "Avvikelseanalys":
        # Ladda upp fil
        uploaded_file = st.file_uploader("Ladda upp en CSV-fil med föreningsdata", type=["csv"])

        if uploaded_file:
            # Läs in data
            data = pd.read_csv(uploaded_file)
            data['year'] = data['year'].astype(int)  # Säkerställ att 'year' är en integer

            # Beräkna relationer och förändringar
            data_with_changes = calculate_relation_changes(data)

            # Visa bearbetad data
            st.subheader("Relationer och förändringar över tid")
            st.dataframe(data_with_changes)

            # Visualisera avvikelser
            st.subheader("Visualisering av avvikelser")
            metric = st.selectbox("Välj relation att visualisera:", [
                "Activities per Member Change (%)",
                "Grants per Activity Change (%)",
                "Grants per Member Change (%)"
            ])

            # Fokusera endast på avvikelser över en viss tröskel
            threshold = st.slider("Ange tröskelvärde för avvikelse (%):", 0, 100, 20)
            filtered_data = data_with_changes[data_with_changes[metric].abs() > threshold]

            if not filtered_data.empty:
                fig = px.bar(
                    filtered_data, x='year', y=metric, color='id',
                    title=f"Föreningar med avvikelse större än {threshold}% för {metric}",
                    labels={"id": "Förenings-ID", metric: "Förändring (%)"}
                )
                st.plotly_chart(fig)
            else:
                st.info("Inga avvikelser hittades över angivet tröskelvärde.")
        else:
            st.warning("Ladda upp en CSV-fil för att börja analysen.")

    elif page == "Riskanalys":
        risk_analysis_app()

    elif page == "Protokollanalys":
        uploaded_file = st.file_uploader("Ladda upp ett protokoll (.txt)", type=["txt"])

        if uploaded_file:
            text = uploaded_file.read().decode("utf-8")
            results = analyze_meeting_minutes_simple(text)

            # Visa analysresultat
            st.subheader("Resultat av protokollanalys")
            for section, status in results.items():
                st.write(f"**{section}**: {status}")

            # Sammanfattande meddelande
            if "❌" in "".join(results.values()):
                st.error("Protokollet är inte komplett enligt den formella mallen.")
            else:
                st.success("Protokollet är komplett och följer den formella mallen.")
        else:
            st.warning("Ladda upp en textfil för att köra analysen.")

if __name__ == "__main__":
    main()