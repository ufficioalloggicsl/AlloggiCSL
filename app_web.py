import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Configurazione della pagina
st.set_page_config(page_title="Portale Alloggi", layout="centered")

st.title("🏨 Richiesta Alloggio Online")
st.write("Compila il modulo per inviare la tua richiesta.")

# --- FORM DI INSERIMENTO ---
with st.form("modulo_alloggio", clear_on_submit=True):
    st.subheader("Dati Personali")
    grado = st.text_input("Grado")
    cognome = st.text_input("Cognome").upper()
    nome = st.text_input("Nome").capitalize()
    cf = st.text_input("Codice Fiscale").upper()
    email = st.text_input("Email")

    st.subheader("Dettagli Soggiorno")
    col1, col2 = st.columns(2)
    with col1:
        turno = st.selectbox("Seleziona Turno", ["1", "2", "3", "4", "5", "6"])
        persone = st.number_input("Numero Persone", min_value=1, step=1)
    with col2:
        data_arr = st.date_input("Data Arrivo")
        data_par = st.date_input("Data Partenza")

    st.subheader("Documentazione")
    file_pdf = st.file_uploader("Carica Documento PDF", type="pdf")

    # Tasto di invio
    submit = st.form_submit_button("INVIA RICHIESTA")

if submit:
    if not cognome or not cf or not file_pdf:
        st.error("Per favore, compila i campi obbligatori e carica il PDF!")
    else:
        # Creazione cartella per i PDF (sul server)
        cartella_dest = f"DOCUMENTI/{cognome}_{nome}"
        if not os.path.exists(cartella_dest):
            os.makedirs(cartella_dest)
        
        # Salvataggio del file PDF
        percorso_pdf = os.path.join(cartella_dest, file_pdf.name)
        with open(percorso_pdf, "wb") as f:
            f.write(file_pdf.getbuffer())

        # Salvataggio dati in Excel
        nuovi_dati = {
            "Data": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "Grado": grado, "Cognome": cognome, "Nome": nome, "CF": cf,
            "Turno": turno, "Persone": persone, 
            "Arrivo": str(data_arr), "Partenza": str(data_par),
            "File": percorso_pdf
        }
        
        file_excel = "database_web.xlsx"
        if os.path.exists(file_excel):
            df = pd.read_excel(file_excel)
            df = pd.concat([df, pd.DataFrame([nuovi_dati])], ignore_index=True)
        else:
            df = pd.DataFrame([nuovi_dati])
        
        df.to_excel(file_excel, index=False)
        st.success(f"Grazie {nome}! La tua richiesta è stata registrata con successo.")