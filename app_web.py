import streamlit as st
import pandas as pd
import os
from datetime import datetime
import io

# Configurazione della pagina
st.set_page_config(page_title="Portale Alloggi Professionale", layout="centered")

st.title("🏨 Sistema Richiesta Alloggio")
st.info("Nota: I dati salvati sono temporanei sul server. Scarica l'Excel periodicamente.")

# Inizializziamo il database in memoria se non esiste nel server
if 'db_access' not in st.session_state:
    st.session_state['db_access'] = pd.DataFrame()

# --- FORM DI INSERIMENTO ---
with st.form("modulo_alloggio", clear_on_submit=True):
    st.subheader("Dati Anagrafici")
    grado = st.text_input("Grado")
    cognome = st.text_input("Cognome").upper()
    nome = st.text_input("Nome").capitalize()
    cf = st.text_input("Codice Fiscale").upper()
    
    st.subheader("Dettagli Soggiorno")
    turno = st.selectbox("Turno", ["1", "2", "3", "4", "5", "6"])
    data_arr = st.date_input("Data Arrivo")
    data_par = st.date_input("Data Partenza")
    
    st.subheader("Documenti")
    file_pdf = st.file_uploader("Carica Documento PDF", type="pdf")

    submit = st.form_submit_button("INVIA RICHIESTA")

if submit:
    if not cognome or not cf or not file_pdf:
        st.error("Errore: Cognome, CF e PDF sono obbligatori!")
    else:
        # 1. Prepariamo i dati
        nuova_richiesta = {
            "Data Invio": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "Grado": grado,
            "Cognome": cognome,
            "Nome": nome,
            "CF": cf,
            "Turno": turno,
            "Arrivo": str(data_arr),
            "Partenza": str(data_par),
            "Nome File": file_pdf.name
        }

        # 2. Salvataggio su file Excel fisico (nel server)
        file_excel = "database_richieste.xlsx"
        if os.path.exists(file_excel):
            df_esistente = pd.read_excel(file_excel)
            df_finale = pd.concat([df_esistente, pd.DataFrame([nuova_richiesta])], ignore_index=True)
        else:
            df_finale = pd.DataFrame([nuova_richiesta])
        
        df_finale.to_excel(file_excel, index=False)
        
        st.success(f"✅ Richiesta inviata correttamente per {cognome} {nome}!")

# --- SEZIONE AMMINISTRATORE (PER SCARICARE I DATI) ---
st.divider()
st.subheader("📥 Area Gestione (Solo per te)")

if os.path.exists("database_richieste.xlsx"):
    df_da_scaricare = pd.read_excel("database_richieste.xlsx")
    
    # Bottone per scaricare l'Excel
    towrite = io.BytesIO()
    df_da_scaricare.to_excel(towrite, index=False, engine='openpyxl')
    towrite.seek(0)
    
    st.download_button(
        label="📊 SCARICA DATABASE EXCEL",
        data=towrite,
        file_name=f"richieste_alloggio_{datetime.now().strftime('%Y%m%d')}.xlsx",
        mime="application/vnd.ms-excel"
    )
else:
    st.write("Nessun dato ancora salvato.")
