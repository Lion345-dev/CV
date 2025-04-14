import streamlit as st

# ---- Configuración de la Página ----------
st.set_page_config(page_title="Curriculum Vitae", layout="wide")

from datetime import datetime
from google.api_core import retry
from dotenv import load_dotenv
from generate_word import generate_cv  # Importar la función para generar el CV
import os
import google.generativeai as genai
import tempfile

# --- Barra Lateral del Comienzo 
st.image("Header.jpg", use_container_width=True)

#### --- Función para calcular la edad #####
anio_nacimiento = datetime(2002, 6, 29)

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

# Configuración de la API de Gemini con manejo de errores
@st.cache_data
def configure_genai():
    try:
        # Check if running on Streamlit Cloud or locally
        if 'GOOGLE_API_KEY' in st.secrets:
            GOOGLE_API_KEY = st.secrets['GOOGLE_API_KEY']
        else:
            # Fallback for local development
            load_dotenv()
            GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
        
        if not GOOGLE_API_KEY:
            raise ValueError("API key not found in secrets or environment variables")
            
        genai.configure(api_key=GOOGLE_API_KEY)
        return True
    except Exception as e:
        st.error(f"Error configurando API: {str(e)}")
        return False

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
# Diccionario para traducir los textos de la barra lateral
sidebar_texts = {
    "title": {
        "Español": "Curriculum Vitae",
        "English": "Curriculum Vitae",
        "Français": "Curriculum Vitae",
        "Português": "Currículo",
        "Deutsch": "Lebenslauf"
    },
    "header": {
        "Español": "Lic. Luis Yael Carmona Gutiérrez",
        "English": "Lic. Luis Yael Carmona Gutiérrez",
        "Français": "Lic. Luis Yael Carmona Gutiérrez",
        "Português": "Lic. Luis Yael Carmona Gutiérrez",
        "Deutsch": "Lic. Luis Yael Carmona Gutiérrez"
    },
    "age": {
        "Español": f"Edad: {edad} años",
        "English": f"Age: {edad} years",
        "Français": f"Âge: {edad} ans",
        "Português": f"Idade: {edad} anos",
        "Deutsch": f"Alter: {edad} Jahre"
    },
    "sections": {
        "Español": "Secciones",
        "English": "Sections",
        "Français": "Sections",
        "Português": "Seções",
        "Deutsch": "Abschnitte"
    }
}

# Update the language selector to include more options
idioma = st.sidebar.selectbox(
    "Language / Idioma", 
    ["Español", "English", "Français", "Português", "Deutsch"]
)

# Actualizar la barra lateral según el idioma seleccionado
st.sidebar.title(sidebar_texts["title"][idioma])
st.sidebar.header(sidebar_texts["header"][idioma])
st.sidebar.image("Foto.jpg", width=200)
st.sidebar.subheader(sidebar_texts["age"][idioma])

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
    "Información Adicional": {  # Nueva sección
        "Español": "Información Adicional",
        "English": "Additional Information",
        "Français": "Informations Supplémentaires",
        "Português": "Informações Adicionais",
        "Deutsch": "Zusätzliche Informationen"
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
    "Información Adicional": "markdown/informacion_adicional.md",  # Nueva sección
    "Idiomas": "markdown/idiomas.md"
}

# Crear una lista de secciones traducidas según el idioma seleccionado
secciones_traducidas = [section_titles[seccion][idioma] for seccion in section_titles]

# Selector de secciones con los títulos traducidos
seccion_traducida = st.sidebar.radio(sidebar_texts["sections"][idioma], secciones_traducidas)

# Obtener la clave original de la sección seleccionada
seccion = next(key for key, value in section_titles.items() if value[idioma] == seccion_traducida)

# Mostrar el encabezado de la sección seleccionada
st.header(section_titles[seccion][idioma])

if seccion == "Idiomas":
    # Mostrar contenido alternativo directamente en el código
    st.markdown("### Español: Nativo")
    st.progress(100)  # Español: Nativo

    st.markdown("### Inglés: Avanzado (C1)")
    st.progress(70)  # Inglés: Avanzado (C1)

    st.markdown("### Francés: Intermedio (B1)")
    st.progress(50)  # Francés: Intermedio (B1)

    st.markdown("### Alemán: Básico (A2)")
    st.progress(30)  # Alemán: Básico (A2)
else:
    # Cargar y mostrar el contenido del archivo Markdown para otras secciones
    contenido = cargar_markdown(section_files[seccion])
    st.markdown(contenido)

# Diccionario para traducir los textos relacionados con la descarga
download_texts = {
    "download_section": {
        "Español": "Descargar Currículum",
        "English": "Download Resume",
        "Français": "Télécharger le CV",
        "Português": "Baixar Currículo",
        "Deutsch": "Lebenslauf herunterladen"
    },
    "generate_word": {
        "Español": "Generar Word",
        "English": "Generate Word",
        "Français": "Générer Word",
        "Português": "Gerar Word",
        "Deutsch": "Word generieren"
    },
    "generate_pdf": {
        "Español": "Generar PDF",
        "English": "Generate PDF",
        "Français": "Générer PDF",
        "Português": "Gerar PDF",
        "Deutsch": "PDF generieren"
    },
    "word_error": {
        "Español": "El archivo Word no se generó correctamente.",
        "English": "The Word file was not generated correctly.",
        "Français": "Le fichier Word n'a pas été généré correctement.",
        "Português": "O arquivo Word não foi gerado correctamente.",
        "Deutsch": "Die Word-Datei wurde nicht korrekt generiert."
    },
    "pdf_error": {
        "Español": "El archivo PDF no se generó correctamente.",
        "English": "The PDF file was not generated correctly.",
        "Français": "Le fichier PDF n'a pas été généré correctement.",
        "Português": "O arquivo PDF não foi gerado correctamente.",
        "Deutsch": "Die PDF-Datei wurde nicht korrekt generiert."
    }
}

# Función para cargar contenido de los archivos Markdown
def cargar_contenido_markdown():
    contenido = {}
    for seccion, archivo in section_files.items():
        try:
            with open(archivo, "r", encoding="utf-8") as f:
                contenido[seccion] = f.read()
        except FileNotFoundError:
            contenido[seccion] = f"Error: No se encontró el archivo {archivo}"
    return contenido

# Cargar contenido de los archivos Markdown
contenido_markdown = cargar_contenido_markdown()

# Diccionario para mapear nombres de idiomas a códigos
language_codes = {
    "Español": "es",
    "English": "en",
    "Français": "fr",
    "Português": "pt",
    "Deutsch": "de"
}

# Botones para descargar el currículum en Word y PDF
st.markdown(f"## {download_texts['download_section'][idioma]}")

# Generar y descargar el archivo Word
if st.button(download_texts["generate_word"][idioma]):
    try:
        # Convertir el idioma seleccionado al código esperado
        language_code = language_codes.get(idioma, "en")  # Por defecto, inglés

        # Generar el archivo Word usando contenido de Markdown
        with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp_file:
            filename_word = generate_cv(contenido_markdown, language=language_code, output_format="docx", output_path=tmp_file.name)
            st.success(download_texts["generate_word"][idioma])
            with open(filename_word, "rb") as file:
                st.download_button(
                    label="📥 Descargar Word",
                    data=file,
                    file_name="curriculum_LYCG.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                )
    except Exception as e:
        st.error(f"{download_texts['word_error'][idioma]}: {str(e)}")

# Generar y descargar el archivo PDF
if st.button(download_texts["generate_pdf"][idioma]):
    try:
        # Convertir el idioma seleccionado al código esperado
        language_code = language_codes.get(idioma, "en")  # Por defecto, inglés

        # Generar el archivo PDF usando contenido de Markdown
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            filename_pdf = generate_cv(contenido_markdown, language=language_code, output_format="pdf", output_path=tmp_file.name)
            st.success(download_texts["generate_pdf"][idioma])
            with open(filename_pdf, "rb") as file:
                st.download_button(
                    label="📥 Descargar PDF",
                    data=file,
                    file_name="curriculum_LYCG.pdf",
                    mime="application/pdf"
                )
    except Exception as e:
        st.error(f"{download_texts['pdf_error'][idioma]}: {str(e)}")