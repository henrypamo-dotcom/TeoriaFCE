import streamlit as st
import pandas as pd
import nltk
from nltk.stem import WordNetLemmatizer
import re

# --- 1. CONFIGURACIÓN DE INTELIGENCIA (NLTK) ---
# Usamos @st.cache_resource para que no se descargue cada vez que tocas un botón
@st.cache_resource
def setup_nltk():
    try:
        nltk.data.find('corpora/wordnet')
        nltk.data.find('corpora/omw-1.4')
    except LookupError:
        nltk.download('wordnet')
        nltk.download('omw-1.4')
    return WordNetLemmatizer()

lemmatizer = setup_nltk()

# --- 2. LA NUEVA LÓGICA DE VALIDACIÓN ---
def check_usage_smart(user_sentence, target_pv_str):
    """
    Verifica si el phrasal verb está en la frase, incluso si está conjugado.
    Ej: Detecta que 'came up with' es válido para 'come up with'.
    """
    # 1. Separamos el phrasal verb original (ej: "come", "up", "with")
    pv_parts = target_pv_str.lower().split()
    verb_root = pv_parts[0]  # "come"
    particles = pv_parts[1:] # ["up", "with"]
    
    # 2. Analizamos la frase del usuario palabra por palabra
    # Limpiamos signos de puntuación básicos para no confundir
    cleaned_sentence = re.sub(r'[^\w\s]', '', user_sentence.lower())
    user_words = cleaned_sentence.split()
    
    # 3. Lematizamos: Convertimos "comes", "came", "coming" -> "come"
    user_lemmas = [lemmatizer.lemmatize(word, pos='v') for word in user_words]
    
    # 4. Comprobación
    # ¿Está la raíz del verbo (ej: "come") en la frase del usuario?
    if verb_root in user_lemmas:
        # ¿Están también las partículas (ej: "up", "with")?
        # Nota: Esto es una validación flexible. Para mayor rigor se requeriría orden secuencial,
        # pero para B2 esto suele bastar y permite separar el verbo (ej: "turn the music down").
        if all(part in user_sentence.lower() for part in particles):
            return True
            
    return False

# --- 3. INTERFAZ GRÁFICA (APP) ---
def run_pv_trainer():
    st.title("🧪 Phrasal Verb Lab")
    st.caption("Powered by NLTK AI & Cambridge Dictionary")

    # URL Raw de tu repositorio TeoriaFCE (¡Asegúrate de que sea la tuya!)
    # Reemplaza 'TU_USUARIO' por tu nombre real en GitHub
    DATA_URL = "https://raw.githubusercontent.com/henrypamo-dotcom/TeoriaFCE/refs/heads/main/phrasal_verbs.csv"
    
    try:
        df = pd.read_csv(DATA_URL)
    except Exception as e:
        st.error(f"Error al cargar datos. Verifica tu URL de GitHub.\nDetalle: {e}")
        return

    # Inicializar estado
    if 'current_pv' not in st.session_state:
        st.session_state.current_pv = df.sample(1).iloc[0]
        st.session_state.feedback_msg = ""
        st.session_state.is_correct = False

    pv = st.session_state.current_pv

    # --- MOSTRAR TARJETA DEL VERBO ---
    with st.container(border=True):
        col1, col2 = st.columns([3, 1])
        with col1:
            st.subheader(f"Target: **{pv['PhrasalVerb']}**")
            # Mostrar la CATEGORÍA como una etiqueta
            if 'Category' in pv:
                st.caption(f"📂 Category: {pv['Category']}")
            else:
                st.caption("📂 Category: General")
        
        with col2:
            # Enlace dinámico a Cambridge
            url_cambridge = f"https://dictionary.cambridge.org/dictionary/english/{pv['PhrasalVerb'].replace(' ', '-')}"
            st.link_button("📖 Cambridge", url_cambridge)

        st.info(f"**Significado:** {pv['Definition']}")
        st.markdown(f"**Ejemplo:** *{pv['Example']}*")

    # --- ZONA DE PRÁCTICA ---
    st.write("---")
    st.write("✍️ **Tu turno:** Escribe una frase usando este verbo (¡puedes conjugarlo!).")
    
    user_text = st.text_input("Tu frase:", key="user_input")
    
    col_check, col_next = st.columns([1, 4])
    
    with col_check:
        if st.button("Corregir"):
            if not user_text:
                st.warning("Escribe algo primero.")
            else:
                # AQUÍ LLAMAMOS A LA NUEVA INTELIGENCIA
                is_valid = check_usage_smart(user_text, pv['PhrasalVerb'])
                
                if is_valid:
                    st.success("✅ ¡Correcto!")
                    st.balloons()
                    st.markdown(f"Detecté una forma válida de **{pv['PhrasalVerb']}**.")
                else:
                    st.error("❌ Mmm...")
                    st.write(f"No detecto el verbo **{pv['PhrasalVerb']}**. ¿Revisaste la ortografía?")

    with col_next:
        if st.button("Siguiente Verbo ➡️"):
            st.session_state.current_pv = df.sample(1).iloc[0]
            st.rerun()

if __name__ == "__main__":
    run_pv_trainer()
