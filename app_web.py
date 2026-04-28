import streamlit as st
import pandas as pd
import os
from datetime import datetime
import io

# Configurazione della pagina
st.set_page_config(page_title="Portale Alloggi Professionale", layout="centered")

st.title("Richiesta Alloggio Capo San Lorenzo")
st.markdown("---")

# Inizializziamo un database in memoria per la sessione corrente
if 'richieste' not in st.session_state:
    st.session_state['richieste'] = []

# --- FORM DI INSERIMENTO ---
with st.form("modulo_alloggio", clear_on_submit=True):
    st.subheader("👤 Dati Anagrafici")
    grado = st.text_input("Grado")
    cognome = st.text_input("Cognome").upper()
    nome = st.text_input("Nome").capitalize()
    cf = st.text_input("Codice Fiscale").upper()
    email = st.text_input("Indirizzo Email")

    st.subheader("📅 Dettagli Soggiorno")
    col1, col2 = st.columns(2)
    with col1:
        turno = st.selectbox("Turno", ["1", "2", "3", "4", "5", "6"])
        persone = st.number_input("Persone", min_value=1, value=1)
    with col2:
        data_arr = st.date_input("Data Arrivo")
        data_par = st.date_input("Data Partenza")

    st.subheader("📄 Documentazione")
    file_pdf = st.file_uploader("Carica PDF", type="pdf")

    submit = st.form_submit_button("INVIA RICHIESTA", use_container_width=True)

if submit:
    if not cognome or not cf or not file_pdf:
        st.error("⚠️ Cognome, CF e PDF sono obbligatori!")
    else:
        # Leggiamo il contenuto del PDF per poterlo "ricordare"
        pdf_bytes = file_pdf.getvalue()
        
        nuova_riga = {
            "Data Invio": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "Grado": grado, "Cognome": cognome, "Nome": nome, "CF": cf,
            "Email": email, "Turno": turno, "Persone": persone,
            "Arrivo": data_arr.strftime("%d/%m/%Y"),
            "Partenza": data_par.strftime("%d/%m/%Y"),
            "Nome File": file_pdf.name,
            "PDF_Data": pdf_bytes  # Salviamo il file in memoria
        }
        
        st.session_state['richieste'].append(nuova_riga)
        st.success(f"✅ Richiesta di {cognome} inviata!")

# --- AREA GESTIONE (AREA AMMINISTRATORE) ---
st.markdown("<br><br>", unsafe_allow_html=True)
st.divider()
st.subheader("📥 Area Gestione Richieste")

if st.session_state['richieste']:
    # Creiamo un DataFrame per l'Excel (senza i dati pesanti del PDF)
    df_excel = pd.DataFrame(st.session_state['richieste']).drop(columns=['PDF_Data'])
    
    # Bottone Download Excel
    buffer = io.BytesIO()
    df_excel.to_excel(buffer, index=False, engine='openpyxl')
    st.download_button("📊 Scarica Tabella Excel", buffer.getvalue(), "richieste.xlsx", "application/vnd.ms-excel")

    # VISUALIZZAZIONE E DOWNLOAD DEI PDF CARICATI
    st.write("### 📂 Documenti PDF da scaricare:")
    for idx, r in enumerate(st.session_state['richieste']):
        st.download_button(
            label=f"📄 Scarica PDF di {r['Cognome']} ({r['Nome File']})",
            data=r['PDF_Data'],
            file_name=f"DOC_{r['CF']}.pdf",
            mime="application/pdf",
            key=f"btn_{idx}"
        )
else:
    st.info("In attesa di nuove richieste...")
