import re

# Funktion för att analysera protokollet baserat på sektioner och nyckelord
def analyze_meeting_minutes_basic(text):
    # Fördefinierade sektioner och mönster
    required_sections = {
        "Datum och plats": [r"(Datum och plats:.*?)(?=\n[A-Z]|$)", "När och var mötet ägde rum."],
        "Mötesdeltagare": [r"(Mötesdeltagare:.*?)(?=\n[A-Z]|$)", "Lista över deltagare."],
        "Dagordning": [r"(Dagordning:.*?)(?=\n[A-Z]|$)", "Dagordningen för mötet."],
        "Verksamhetsberättelse": [r"(Verksamhetsberättelse:.*?)(?=\n[A-Z]|$)", "Redogörelse för verksamhetsåret."],
        "Ekonomisk rapport": [r"(Ekonomisk rapport:.*?)(?=\n[A-Z]|$)", "Ekonomisk rapportering."],
        "Ansvarsfrihet": [r"(Ansvarsfrihet:.*?)(?=\n[A-Z]|$)", "Ansvarsfrihet för styrelsen."],
        "Val av styrelse": [r"(Val av styrelse:.*?)(?=\n[A-Z]|$)", "Val av ny styrelse."],
        "Övriga frågor": [r"(Övriga frågor:.*?)(?=\n[A-Z]|$)", "Övriga frågor som diskuterades."],
    }

    # Problematiska nyckelord eller fraser
    problematic_keywords = [
        "misskötsel", "ansvarig för allt dåligt", "spendera alla pengar", "olämpligt beteende"
    ]

    # Resultatbehållare
    results = {}

    for section, (pattern, explanation) in required_sections.items():
        match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
        if match:
            section_content = match.group(1).strip()  # Extrahera sektionens innehåll
            results[section] = {"status": "✅ Hittad", "content": section_content}

            # Kontrollera för problematiskt innehåll
            flagged_phrases = [kw for kw in problematic_keywords if kw in section_content.lower()]
            if flagged_phrases:
                results[section]["status"] = "⚠️ Problematiskt innehåll hittat"
                results[section]["issues"] = flagged_phrases
            else:
                results[section]["issues"] = None
        else:
            results[section] = {"status": f"❌ Saknas ({explanation})", "content": None, "issues": None}

    return results