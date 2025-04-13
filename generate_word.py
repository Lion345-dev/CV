import streamlit as st
import tempfile
from linkedin_scraper import scrape_linkedin_profile  # Función para obtener datos de LinkedIn
import os
from docx import Document
from docx.shared import Pt
from docx2pdf import convert

# Diccionario para los archivos Markdown
section_files = {
    "Perfil Profesional": "markdown/perfil_profesional.md",
    "Experiencia Profesional": "markdown/experiencia_profesional.md",
    "Experiencia Académica": "markdown/experiencia_academica.md",
    "Idiomas": "markdown/idiomas.md"
}

# Diccionario para traducir los textos relacionados con la descarga
download_texts = {
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
        "Português": "O arquivo Word não foi gerado corretamente.",
        "Deutsch": "Die Word-Datei wurde nicht korrekt generiert."
    },
    "pdf_error": {
        "Español": "El archivo PDF no se generó correctamente.",
        "English": "The PDF file was not generated correctly.",
        "Français": "Le fichier PDF n'a pas été généré correctement.",
        "Português": "O arquivo PDF não foi gerado corretamente.",
        "Deutsch": "Die PDF-Datei wurde nicht korrekt generiert."
    }
}

# Función para cargar contenido desde Markdown
def cargar_contenido_markdown():
    contenido = {}
    for seccion, archivo in section_files.items():
        try:
            with open(archivo, "r", encoding="utf-8") as f:
                contenido[seccion] = f.read()
        except FileNotFoundError:
            contenido[seccion] = None  # Indicar que no se encontró el archivo
    return contenido

# Función para obtener datos del currículum
def obtener_datos_cv():
    # Intentar cargar datos desde Markdown
    contenido_markdown = cargar_contenido_markdown()
    if all(value is None for value in contenido_markdown.values()):
        # Si no hay datos en Markdown, obtenerlos desde LinkedIn
        st.warning("No se encontraron archivos Markdown. Obteniendo datos desde LinkedIn...")
        return scrape_linkedin_profile("https://www.linkedin.com/in/luisyaelcarmona/")
    return contenido_markdown

# Función para generar el CV
def generate_cv(data, language, output_format="docx", output_path="CV_Output"):
    """
    Genera un CV en formato Word o PDF basado en los datos proporcionados.

    Args:
        data (dict): Datos del currículum.
        language (str): Idioma del CV (es, en, fr, pt, de).
        output_format (str): Formato de salida ("docx" o "pdf").
        output_path (str): Ruta base para guardar el archivo.

    Returns:
        str: Ruta del archivo generado.
    """
    # Crear documento Word
    doc = Document()

    # Configurar estilo del documento
    style = doc.styles['Normal']
    font = style.font
    font.name = 'Arial'
    font.size = Pt(11)

    # Agregar contenido al documento
    doc.add_heading(data.get('name', 'Nombre no disponible'), level=1)
    doc.add_paragraph(f"Email: {data.get('email', 'No disponible')}")
    doc.add_paragraph(f"Teléfono: {data.get('phone', 'No disponible')}")

    doc.add_heading("Experiencia Profesional", level=2)
    for exp in data.get('experience', []):
        doc.add_paragraph(f"{exp['title']} en {exp['company']} ({exp['start_date']} - {exp['end_date']})")
        for achievement in exp.get('achievements', []):
            doc.add_paragraph(f"- {achievement}", style='List Bullet')

    doc.add_heading("Educación", level=2)
    for edu in data.get('education', []):
        doc.add_paragraph(f"{edu['degree']} en {edu['institution']} ({edu['start_date']} - {edu['end_date']})")

    doc.add_heading("Idiomas", level=2)
    for lang in data.get('languages', []):
        doc.add_paragraph(f"{lang['language']}: {lang['level']}")

    doc.add_heading("Habilidades", level=2)
    for skill in data.get('skills', []):
        doc.add_paragraph(f"- {skill}", style='List Bullet')

    # Guardar archivo
    filename = f"{output_path}.{output_format}"
    if output_format == "docx":
        doc.save(filename)
    elif output_format == "pdf":
        temp_docx = f"{output_path}.docx"
        doc.save(temp_docx)
        convert(temp_docx, filename)
        os.remove(temp_docx)

    return filename

# Cargar datos del currículum
datos_cv = obtener_datos_cv()

# Generar y descargar el archivo Word
if st.button(download_texts["generate_word"]["Español"]):  # Cambia "Español" según el idioma seleccionado
    try:
        language_code = "es"  # Cambia según el idioma seleccionado
        with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp_file:
            filename_word = generate_cv(datos_cv, language=language_code, output_format="docx", output_path=tmp_file.name)
            st.success(download_texts["generate_word"]["Español"])
            with open(filename_word, "rb") as file:
                st.download_button(
                    label="📥 Descargar Word",
                    data=file,
                    file_name="curriculum_LYCG.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                )
    except Exception as e:
        st.error(f"{download_texts['word_error']['Español']}: {str(e)}")

# Generar y descargar el archivo PDF
if st.button(download_texts["generate_pdf"]["Español"]):  # Cambia "Español" según el idioma seleccionado
    try:
        language_code = "es"  # Cambia según el idioma seleccionado
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            filename_pdf = generate_cv(datos_cv, language=language_code, output_format="pdf", output_path=tmp_file.name)
            st.success(download_texts["generate_pdf"]["Español"])
            with open(filename_pdf, "rb") as file:
                st.download_button(
                    label="📥 Descargar PDF",
                    data=file,
                    file_name="curriculum_LYCG.pdf",
                    mime="application/pdf"
                )
    except Exception as e:
        st.error(f"{download_texts['pdf_error']['Español']}: {str(e)}")