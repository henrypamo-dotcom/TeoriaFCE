import streamlit as st
import pandas as pd
import random

def run_pv_trainer():
    st.title("🧪 Phrasal Verb Lab")
    st.write("Practica los verbos oficiales de Cambridge.")

    # URL Raw de tu nuevo repo (sustituye TU_USUARIO)
    DATA_URL = "https://raw.githubusercontent.com/henrypamo-dotcom/TeoriaFCE/refs/heads/main/phrasal_verbs.csv"
    
    try:
        df = pd.read_csv(DATA_URL)
    except:
        st.error("Error al cargar el CSV. Verifica la URL de GitHub.")
        return

    if 'current_pv' not in st.session_state:
        st.session_state.current_pv = df.sample(1).iloc[0]

    pv = st.session_state.current_pv

    # Interfaz de estudio
    col1, col2 = st.columns([2, 1])
    with col1:
        st.subheader(f"Target: **{pv['PhrasalVerb']}**")
    with col2:
        # Enlace al diccionario según la recomendación de la fuente 
        url_cambridge = f"https://dictionary.cambridge.org/dictionary/english/{pv['PhrasalVerb'].replace(' ', '-')}"
        st.link_button("📖 Ver en Cambridge", url_cambridge)

    st.info(f"**Significado:** {pv['Definition']}")
    st.markdown(f"**Ejemplo de referencia:** *{pv['Example']}*")

    # Zona de Práctica
    user_text = st.text_input("Escribe tu propia oración usando este phrasal verb:")
    
    if st.button("Corregir"):
        if pv['PhrasalVerb'].lower() in user_text.lower():
            st.success("✅ ¡Bien hecho! Has incluido el phrasal verb correctamente.")
            st.balloons()
        else:
            st.warning(f"Intenta incluir '{pv['PhrasalVerb']}' en tu oración.")

    if st.button("Siguiente Verbo ➡️"):
        st.session_state.current_pv = df.sample(1).iloc[0]
        st.rerun()

if __name__ == "__main__":
    run_pv_trainer()
