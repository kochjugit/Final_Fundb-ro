import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Seiten-Konfiguration
st.set_page_config(
    page_title="Digitales Fundbüro",
    page_icon="🔍",
    layout="centered"
)

# Custom CSS für Layout-Anpassung und vergrößerte Buttons/Container
st.markdown("""
    <style>
    .main-header {
        text-align: center;
        font-size: 2.8rem;
        font-weight: bold;
        color: #2C3E50;
        margin-bottom: 2rem;
    }
    .stButton>button {
        width: 100%;
        height: 80px;
        font-size: 1.4rem !important;
        font-weight: bold !important;
        border-radius: 12px !important;
        margin-bottom: 1rem;
    }
    .card {
        padding: 1.5rem;
        border-radius: 10px;
        background-color: #F8F9FA;
        border: 1px solid #E9ECEF;
        margin-bottom: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# DATENBANK INITIALISIERUNG (Session State)
# ---------------------------------------------------------
if "fundstuecke" not in st.session_state:
    st.session_state.fundstuecke = [
        {
            "id": 1,
            "titel": "Rote Mütze",
            "kategorie": "Kleidung",
            "ort": "Mensa",
            "datum": datetime.now().date() - timedelta(days=2),
            "beschreibung": "Gestrickte Mütze mit Bommel",
            "kontakt": "mensa@fundbuero.de",
            "status": "Aktiv"
        },
        {
            "id": 2,
            "titel": "Schlüsselbund",
            "kategorie": "Schlüssel",
            "ort": "Bibliothek",
            "datum": datetime.now().date() - timedelta(days=10),
            "beschreibung": "3 Schlüssel mit blauem Anhänger",
            "kontakt": "bib@fundbuero.de",
            "status": "Aktiv"
        },
        {
            "id": 3,
            "titel": "Kopfhörer (Wireless)",
            "kategorie": "Elektronik",
            "ort": "Hörsaal 1",
            "datum": datetime.now().date() - timedelta(days=1),
            "beschreibung": "Schwarzes Ladeetui",
            "kontakt": "ha1@fundbuero.de",
            "status": "Abgeholt"
        }
    ]

if "ansicht" not in st.session_state:
    st.session_state.ansicht = "home"

# ---------------------------------------------------------
# HILFSFUNKTIONEN
# ---------------------------------------------------------
def status_aendern(item_id, neuer_status):
    for item in st.session_state.fundstuecke:
        if item["id"] == item_id:
            item["status"] = neuer_status

def item_karte_anzeigen(item):
    st.markdown(f"### {item['titel']}")
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"**Ort:** {item['ort']}")
        st.write(f"**Kategorie:** {item['kategorie']}")
        st.write(f"**Datum:** {item['datum'].strftime('%d.%m.%Y')}")
    with col2:
        st.write(f"**Beschreibung:** {item['beschreibung']}")
        st.write(f"**Kontakt:** {item['kontakt']}")
        
        # Status-Anzeige und Kennzeichnung
        if item["status"] == "Aktiv":
            st.warning("Status: Noch nicht abgeholt")
            if st.button("✅ Als abgeholt kennzeichnen", key=f"btn_abgeholt_{item['id']}"):
                status_aendern(item['id'], "Abgeholt")
                st.success("Status aktualisiert!")
                st.rerun()
        else:
            st.success("Status: Bereits abgeholt")
            if st.button("🔄 Zurück auf 'Aktiv' setzen", key=f"btn_aktiv_{item['id']}"):
                status_aendern(item['id'], "Aktiv")
                st.success("Status aktualisiert!")
                st.rerun()
    st.divider()

# ---------------------------------------------------------
# HAUPTSEITE / TABS (Analog zum Entwurf)
# ---------------------------------------------------------
st.markdown("<div class='main-header'>Digitales Fundbüro</div>", unsafe_allow_html=True)

# Navigation zur Startseite oben anzeigen, falls man tief in einer Ansicht ist
if st.session_state.ansicht != "home":
    if st.button("⬅️ Zurück zur Hauptübersicht", key="back_btn"):
        st.session_state.ansicht = "home"
        st.rerun()

# 1. HAUPTÜBERSICHT (Große Buttons gemäß Zeichnung)
if st.session_state.ansicht == "home":
    st.write("---")
    
    col_a, col_b = st.columns([3, 1])
    with col_a:
        if st.button("🔍  Schnellsuche"):
            st.session_state.ansicht = "schnellsuche"
            st.rerun()

        if st.button("📅  Diese Woche gefunden"):
            st.session_state.ansicht = "diese_woche"
            st.rerun()

        if st.button("📦  Alle Stücke"):
            st.session_state.ansicht = "alle_stuecke"
            st.rerun()
            
    with col_b:
        st.info("➕ **Neuer Fund?**")
        if st.button("Gegenstand melden"):
            st.session_state.ansicht = "neu_melden"
            st.rerun()

# 2. ANSICHT: SCHNELLSUCHE
elif st.session_state.ansicht == "schnellsuche":
    st.subheader("🔍 Schnellsuche")
    suchbegriff = st.text_input("Mütze, Schlüssel, Ort...", placeholder="Suchbegriff eingeben...")
    
    filter_status = st.radio("Status-Filter:", ["Nur Aktive", "Nur Abgeholte", "Alle"], horizontal=True)
    
    gefundene = []
    for item in st.session_state.fundstuecke:
        match_text = (suchbegriff.lower() in item["titel"].lower() or 
                      suchbegriff.lower() in item["ort"].lower() or 
                      suchbegriff.lower() in item["beschreibung"].lower()) if suchbegriff else True
        
        match_status = True
        if filter_status == "Nur Aktive":
            match_status = item["status"] == "Aktiv"
        elif filter_status == "Nur Abgeholte":
            match_status = item["status"] == "Abgeholt"
            
        if match_text and match_status:
            gefundene.append(item)
            
    st.write(f"**Treffer:** {len(gefundene)}")
    for item in gefundene:
        item_karte_anzeigen(item)

# 3. ANSICHT: DIESE WOCHE GEFUNDEN
elif st.session_state.ansicht == "diese_woche":
    st.subheader("📅 Diese Woche gefunden")
    vor_einer_woche = datetime.now().date() - timedelta(days=7)
    
    wochen_items = [
        item for item in st.session_state.fundstuecke 
        if item["datum"] >= vor_einer_woche
    ]
    
    if not wochen_items:
        st.info("In den letzten 7 Tagen wurden keine Gegenstände eingetragen.")
    else:
        for item in wochen_items:
            item_karte_anzeigen(item)

# 4. ANSICHT: ALLE STÜCKE
elif st.session_state.ansicht == "alle_stuecke":
    st.subheader("📦 Alle Stücke")
    
    sortierung = st.radio("Sortierung:", ["Chronologisch (Neueste zuerst)", "Alphabetisch (A-Z)"], horizontal=True)
    
    items = st.session_state.fundstuecke.copy()
    if sortierung == "Chronologisch (Neueste zuerst)":
        items.sort(key=lambda x: x["datum"], reverse=True)
    else:
        items.sort(key=lambda x: x["titel"].lower())
        
    for item in items:
        item_karte_anzeigen(item)

# 5. ANSICHT: NEUEN GEGENSTAND MELDEN
elif st.session_state.ansicht == "neu_melden":
    st.subheader("➕ Neuen Fund melden")
    
    with st.form("neuer_fund_form"):
        titel = st.text_input("Was wurde gefunden?")
        kategorie = st.selectbox("Kategorie", ["Kleidung", "Schlüssel", "Elektronik", "Dokumente", "Sonstiges"])
        ort = st.text_input("Fundort")
        datum = st.date_input("Funddatum", datetime.now().date())
        beschreibung = st.text_area("Beschreibung")
        kontakt = st.text_input("Kontakt E-Mail / Telefon")
        
        submitted = st.form_submit_button("Eintrag speichern")
        if submitted:
            neue_id = max([i["id"] for i in st.session_state.fundstuecke], default=0) + 1
            st.session_state.fundstuecke.append({
                "id": neue_id,
                "titel": titel,
                "kategorie": kategorie,
                "ort": ort,
                "datum": datum,
                "beschreibung": beschreibung,
                "kontakt": kontakt,
                "status": "Aktiv"
            })
            st.success("Gegenstand erfolgreich gespeichert!")
            st.session_state.ansicht = "alle_stuecke"
            st.rerun()
