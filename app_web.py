import streamlit as st
import pandas as pd
import os
from datetime import datetime
import io

# Configurazione della pagina (Titolo che appare nella scheda del browser)
st.set_page_config(page_title="Portale Richiesta Alloggio", layout="centered")

st.title("🏨 Modulo Richiesta Alloggio Online")
st.markdown("---")

# --- FORM DI INSERIMENTO ---
# Usiamo 'clear_on_submit=True' così il modulo si svuota dopo l'invio
with st.form("modulo_alloggio", clear_on_submit=True):
    
    st.subheader("👤 Dati Anagrafici")
    grado = st.text_input("Grado (es. Capitano, Maresciallo...)")
    cognome = st.text_input("Cognome").upper()
    nome = st.text_input("Nome").capitalize()
    cf = st.text_input("Codice Fiscale (16 caratteri)").upper()
    email = st.text_input("Indirizzo Email")

    st.markdown("---")
    st.subheader("📅 Dettagli del Soggiorno")
    
    col1, col2 = st.columns(2)
    with col1:
        turno = st.selectbox("Seleziona Turno", ["1", "2", "3", "4", "5", "6"])
        # REINSERITO: Numero di persone
        persone = st.number_input("Numero di persone", min_value=1, max_value=20, value=1, step=1)
    
    with col2:
        data_arr = st.date_input("Data Arrivo", format="DD/MM/YYYY")
        data_par = st.date_input("Data Partenza", format="DD/MM/YYYY")

    st.markdown("---")
    st.subheader("📄 Documentazione")
    file_pdf = st.file_uploader("Carica Documento d'Identità (Solo formato PDF)", type="pdf")

    # Tasto di invio professionale
    submit = st.form_submit_button("INVIA RICHIESTA", use_container_width=True)

# --- LOGICA DI SALVATAGGIO ---
if submit:
    # Controllo che i campi fondamentali siano pieni
    if not cognome or not cf or not file_pdf:
        st.error("⚠️ Errore: Cognome, Codice Fiscale e Documento PDF sono obbligatori!")
    else:
        # Preparazione della riga dati
        nuova_riga = {
            "Data/Ora Invio": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "Grado": grado,
            "Cognome": cognome,
            "Nome": nome,
            "Codice Fiscale": cf,
            "Email": email,
            "Turno": turno,
            "Numero Persone": persone,
            "Data Arrivo": data_arr.strftime("%d/%m/%Y"),
            "Data Partenza": data_par.strftime("%d/%m/%Y"),
            "Nome Documento": file_pdf.name
        }

        # Salvataggio temporaneo nel file Excel del server
        file_excel = "database_alloggi.xlsx"
        if os.path.exists(file_excel):
            df_esistente = pd.read_excel(file_excel)
            df_finale = pd.concat([df_esistente, pd.DataFrame([nuova_riga])], ignore_index=True)
        else:
            df_finale = pd.DataFrame([nuova_riga])
        
        df_finale.to_excel(file_excel, index=False)
        
        st.success(f"✅ Grazie {nome}! La richiesta è stata inviata correttamente.")
        st.balloons() # Un piccolo tocco di allegria al successo!

# --- AREA GESTIONE (VISIBILE SOLO IN FONDO ALLA PAGINA) ---
st.markdown("<br><br>", unsafe_allow_html=True)
st.divider()
st.subheader("📥 Area Amministratore")
st.info("Da qui puoi scaricare l'elenco aggiornato in formato Excel sul tuo computer.")

if os.path.exists("database_alloggi.xlsx"):
    df_scarico = pd.read_excel("database_alloggi.xlsx")
    
    # Preparazione del file per il download (in memoria)
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        df_scarico.to_excel(writer, index=False)
    
    st.download_button(
        label="📥 SCARICA ELENCO RICHIESTE (EXCEL)",
        data=buffer.getvalue(),
        file_name=f"database_richieste_{datetime.now().strftime('%Y%m%d')}.xlsx",
        mime="application/vnd.ms-excel",
        help="Clicca per scaricare l'elenco completo delle richieste salvate finora."
    )
else:
    st.warning("Nessuna richiesta ancora registrata.")
