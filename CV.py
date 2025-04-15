import streamlit as st
from datetime import datetime
from dotenv import load_dotenv
import os
import google.generativeai as genai

# If GenerativeModel is still not found, try:
from google.generativeai import GenerativeModel

# If configure is not found, it might be implicitly available after the main import
# If list_models is not found, double-check the documentation for its current location

import tempfile
from docx import Document  # Corrected import statement
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from descarga_CV import descargar_archivo, convert_to_pdf  # Importar la función desde descarga_CV

# ---- Configuración de la Página ----------
st.set_page_config(page_title="Curriculum Vitae", layout="wide")

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
load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

@st.cache_resource
def configure_genai():
    try:
        if not GOOGLE_API_KEY:
            raise ValueError("API key not found in environment variables")

        genai.configure(api_key=GOOGLE_API_KEY)

        return True
    except Exception as e:
        st.error(f"Error configuring API: {str(e)}")
        return False

################

# Función para traducir texto con manejo de errores y caché
@st.cache_data
def traducir_texto(texto, idioma_destino):
    st.write("Translating...")  # Add this line to check if the function is called
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
        - Conserva el formato original del currículum

        Currículum a traducir:
        {texto}
        """

        try:
            model = genai.GenerativeModel("gemini-2.0-flash")  # or a model from the list
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            st.error(f"Error generating content: {e}. Model may not be available.")
            return ""

    except Exception as e:
        st.error(f"Error in traducir_texto: {e}")
        return ""

# Navigation bar
# Diccionario para traducir los textos de la barra lateral
sidebar_texts = {
    "title": {
        "Español": "Curriculum Vitae",
        "English": "Curriculum Vitae"
    },
    "header": {
        "Español": "Lic. Luis Yael Carmona Gutiérrez",
        "English": "Lic. Luis Yael Carmona Gutiérrez"
    },
    "age": {
        "Español": f"Edad: {edad} años",
        "English": f"Age: {edad} years"
    },
    "sections": {
        "Español": "Secciones",
        "English": "Sections"
    }
}

# Update the language selector to include only English and Spanish
idioma = st.sidebar.selectbox(
    "Language / Idioma",
    ["Español", "English"]
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
        "English": "Contact Information"
    },
    "Experiencia Profesional": {
        "Español": "Experiencia Profesional",
        "English": "Academic Experience"
    },
    "Información Adicional": {
        "Español": "Información Adicional",
        "English": "Additional Information"
    },
    "Idiomas": {
        "Español": "Idiomas",
        "English": "Languages"
    }
}

# Dictionary for markdown file paths
section_files = {
    "Perfil Profesional": "markdown/perfil_profesional.md",
    "Experiencia Profesional": "markdown/experiencia_profesional.md",
    "Experiencia Académica": "markdown/experiencia_academica.md",
    "Información Adicional": "markdown/informacion_adicional.md",
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
else:
    # Cargar y mostrar el contenido del archivo Markdown para otras secciones
    contenido = cargar_markdown(section_files[seccion])
    st.markdown(contenido)

# Diccionario para traducir los textos relacionados con la descarga
download_texts = {
    "download_section": {
        "Español": "Descargar Currículum",
        "English": "Download Resume"
    },
    "download_word": {
        "Español": "Descargar Word",
        "English": "Download Word"
    },
    "download_pdf": {
        "Español": "Descargar PDF",
        "English": "Download PDF"
    },
    "convert_to_pdf": {
        "Español": "Convertir a PDF",
        "English": "Convert to PDF"
    }
}

# Rutas y nombres de los archivos a descargar
ruta_archivo_word_es = r"C:\Users\luisy\Laboral\CV\CV_LYCG_Español.docx"
ruta_archivo_word_en = r"C:\Users\luisy\Laboral\CV\CV_LYCG_English.docx"
ruta_archivo_pdf_es = r"C:\Users\luisy\Laboral\CV\CV_LYCG_Español.pdf"
ruta_archivo_pdf_en = r"C:\Users\luisy\Laboral\CV\CV_LYCG_English.pdf"  # Ruta para el PDF en inglés

# Traducción del currículum
@st.cache_data
def traducir_curriculum(ruta_archivo, idioma_destino):
    try:
        with open(ruta_archivo, "r", encoding="windows-1252") as file:  # Especificar la codificación
            contenido = file.read()

        prompt = f"""
        Traduce el siguiente currículum al {idioma_destino}.
        Importante:
        - NO incluyas marcadores de código como ``` o markdown
        - Mantén los emojis (📞, 🎯, 💫, etc.)
        - Preserva los enlaces y URLs tal cual
        - Mantén el formato de listas con - o *
        - Conserva los títulos con # y ##
        - No modifiques fechas ni números
        - Mantén los nombres propios sin cambios
        - Conserva el formato original del currículum

        Currículum a traducir:
        {contenido}
        """

        model = genai.GenerativeModel("gemini-2.0-flash")  # or the model you confirmed is available
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        st.error(f"Error al traducir el currículum: {e}")
        return None

# Función para traducir el contenido de un documento Word
def traducir_documento_word(ruta_archivo, idioma_destino):
    try:
        doc = Document(ruta_archivo)
        for paragraph in doc.paragraphs:
            if paragraph.text:
                translated_text = traducir_texto(paragraph.text, idioma_destino)
                paragraph.text = translated_text
        return doc
    except Exception as e:
        st.error(f"Error al traducir el documento Word: {e}")
        return None

# Botones para descargar el currículum en Word y PDF
st.markdown(f"## {download_texts['download_section'][idioma]}")

# Rutas de archivo Word según el idioma
ruta_archivo_word = ruta_archivo_word_es if idioma == "Español" else ruta_archivo_word_en

# Descargar el archivo Word
if os.path.exists(ruta_archivo_word):
    # Use a unique key for each download button
    st.download_button(
        label=download_texts['download_word'][idioma],
        data=open(ruta_archivo_word, "rb").read(),
        file_name=os.path.basename(ruta_archivo_word),
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        key=f"word_download_{idioma}"  # Unique key
    )
else:
    st.error(f"No se encontró el archivo Word en la ruta: {ruta_archivo_word}")

# Descargar archivos en inglés
if idioma == "English":
    # Add download PDF button
    if os.path.exists(ruta_archivo_pdf_en):
        st.download_button(
            label=download_texts['download_pdf'][idioma],
            data=open(ruta_archivo_pdf_en, 'rb').read(),
            file_name="CV_LYCG_English.pdf",
            mime="application/pdf",
            key="pdf_download_english"
        )
    else:
        st.error(f"No se encontró el archivo PDF en la ruta: {ruta_archivo_pdf_en}")

# Descargar el archivo PDF en español
if idioma == "Español":
    if os.path.exists(ruta_archivo_pdf_es):
        st.download_button(
            label=download_texts['download_pdf'][idioma],
            data=open(ruta_archivo_pdf_es, 'rb').read(),
            file_name=f"curriculum_LYCG_Español.pdf",
            mime="application/pdf",
            key="pdf_download_spanish"  # Unique key
        )
    else:
        st.error(f"No se encontró el archivo PDF en la ruta: {ruta_archivo_pdf_es}")