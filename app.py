import os
import streamlit as st
from google import genai

# Configuración de la página
st.set_page_config(page_title="PhishGuard AI", page_icon="🛡️")

st.title("🛡️ PhishGuard AI")
st.subheader("Detector Inteligente de Phishing con IA")
st.write("Pegá el contenido de un correo sospechoso para que nuestro analizador determine si es un ataque.")

# Obtener API Key de Secrets o variables de entorno
api_key = st.secrets.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")

# Barra lateral informativa
with st.sidebar:
    st.header("Configuración")
    st.markdown("[Obtener API Key en Google AI Studio](https://aistudio.google.com/)")

# Área de texto principal
email_text = st.text_area("Contenido del correo electrónico:", height=200, placeholder="Estimado cliente, su cuenta ha sido suspendida...")

# Botón de análisis
if st.button("Analizar Correo"):
    if not email_text.strip():
        st.warning("Por favor, pegá el texto de un correo para analizar.")
    else:
        with st.spinner("Analizando patrones de ingeniería social..."):
            try:
                # Inicializar el cliente de Gemini con la API Key
                client = genai.Client(api_key=api_key)
                
                # Prompt estructurado para la IA
                system_prompt = (
                    "Actúa como un motor de análisis de Ciberseguridad especializado en detección de Phishing e Ingeniería Social. "
                    "Analizá el siguiente texto y generá un informe técnico directo y profesional."
                    "No te presentes ni uses frases en primera persona (como "Hola" o "Como Analista...")."
                    "Respondé directamente con la siguiente estructura:\n\n"
                    "1. NIVEL DE RIESGO: (Bajo, Medio, Alto o Crítico)\n"
                    "2. PUNTAJE DE RIESGO: (Del 1 al 10)\n"
                    "3. INDICADORES SOSPECHOSOS: (Tácticas de urgencia, suplantación, enlaces raros, amenazas, etc.)\n"
                    "4. RECOMENDACIÓN: (Acciones concretas para el usuario)\n\n"
                    f"Texto del correo a analizar:\n{email_text}"
                )
                
                response = client.models.generate_content(
                    model='gemini-3.6-flash',
                    contents=system_prompt,
                )
                
                st.success("Análisis completado")
                st.markdown("### Resultado del Análisis")
                st.write(response.text)
                
            except Exception as e:
                st.error(f"Error al conectar con la API: {e}")