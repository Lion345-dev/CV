import streamlit as st
from datetime import datetime
import google.generativeai as genai

from google.api_core import retry

# Configuración de la API de Gemini con manejo de errores
@st.cache_data
def configure_genai():
    try:
        GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
        genai.configure(api_key=GOOGLE_API_KEY)
        return True
    except Exception as e:
        st.error(f"Error configurando API: {str(e)}")
        return False

#  ---- Configuración de la Página ----------
st.set_page_config(page_title="Curriculum Vitae", layout="wide")

# --- Barra Lateral del Comienzo 
st.image("Header.jpg", use_container_width=True)

#### --- Función para calcular la edad #####
anio_nacimiento = datetime(2002,6,29)

def calcular_edad(anio_nacimiento):
    fecha_actual = datetime.now()
    edad = fecha_actual.year - anio_nacimiento.year
    
    # Ajustar la edad si aún no ha llegado el mes de cumpleaños
    if fecha_actual.month < anio_nacimiento.month:
        edad -= 1
    elif fecha_actual.month == anio_nacimiento.month and fecha_actual.day < anio_nacimiento.day:
        edad -= 1
        
    return edad

edad = calcular_edad(anio_nacimiento)

################

# Función para traducir texto con manejo de errores y caché
@st.cache_data
def traducir_texto(texto, idioma_destino):
    try:
        if not configure_genai():
            return texto
        
        prompt = f"""
        Traduce el siguiente contenido al {idioma_destino}.
        Importante:
        - NO incluyas marcadores de código como ``` o markdown
        - Mantén los emojis (📞, 🎯, 💫, etc.)
        - Preserva los enlaces y URLs tal cual
        - Mantén el formato de listas con - o *
        - Conserva los títulos con # y ##
        - No modifiques fechas ni números
        - Mantén los nombres propios sin cambios

        Contenido a traducir:
        {texto}
        """
        
        model = genai.GenerativeModel('gemini-2.0-flash')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        st.warning(f"Error en traducción, mostrando texto original: {str(e)}")
        return texto

# Navigation bar 
st.sidebar.title("Curriculum Vitae")
st.sidebar.header("Lic. Luis Yael Carmona Gutiérrez")
st.sidebar.image("Foto.jpg",width=200)
st.sidebar.subheader(f"Edad: {edad} años")

# Update the language selector to include more options
idioma = st.sidebar.selectbox(
    "Language / Idioma", 
    ["Español", "English", "Français", "Português", "Deutsch"]
)

# Función para cargar y traducir markdown
def cargar_markdown(archivo):
    try:
        with open(archivo, "r", encoding="utf-8") as f:
            contenido = f.read()
            if idioma != "Español":
                translated_text = traducir_texto(contenido, idioma)
                # Remove markdown comment if present
                if translated_text.startswith("```markdown"):
                    translated_text = translated_text.split("\n", 2)[2]
                if translated_text.endswith("```"):
                    translated_text = translated_text[:-3]
                return translated_text.strip()
            return contenido
    except FileNotFoundError:
        return f"Error: No se encontró el archivo {archivo}"

# --- Navegación  del App 

seccion = st.sidebar.radio("Secciones", ["Perfil Profesional","Experiencia Profesional","Experiencia Académica","Idiomas"])

# Dictionary for section titles in all languages
section_titles = {
    "Perfil Profesional": {
        "Español": "Datos de Contacto",
        "English": "Contact Information",
        "Français": "Informations de Contact",
        "Português": "Informações de Contato",
        "Deutsch": "Kontaktinformationen"
    },
    "Experiencia Profesional": {
        "Español": "Experiencia Profesional",
        "English": "Professional Experience",
        "Français": "Expérience Professionnelle",
        "Português": "Experiência Profissional",
        "Deutsch": "Berufserfahrung"
    },
    "Experiencia Académica": {
        "Español": "Experiencia Académica",
        "English": "Academic Experience",
        "Français": "Expérience Académique",
        "Português": "Experiência Acadêmica",
        "Deutsch": "Akademische Erfahrung"
    },
    "Idiomas": {
        "Español": "Idiomas",
        "English": "Languages",
        "Français": "Langues",
        "Português": "Idiomas",
        "Deutsch": "Sprachen"
    }
}

# Dictionary for markdown file paths
section_files = {
    "Perfil Profesional": "markdown/perfil_profesional.md",
    "Experiencia Profesional": "markdown/experiencia_profesional.md",
    "Experiencia Académica": "markdown/experiencia_academica.md",
    "Idiomas": "markdown/idiomas.md"
}

# Display selected section
st.header(section_titles[seccion][idioma])
contenido = cargar_markdown(section_files[seccion])
st.markdown(contenido)

# Add progress bars only for Languages section
if seccion == "Idiomas":
    if "Español" in contenido:
        st.progress(100)
    if "Inglés" in contenido:
        st.progress(70)