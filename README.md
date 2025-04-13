# CV Digital Interactivo

Aplicación web interactiva construida con Streamlit para mostrar mi Curriculum Vitae con capacidades de traducción automática y exportación a Word.

## Características

- 📱 Interfaz responsiva y moderna
- 🌐 Soporte multilingüe usando Google Gemini AI
  - Español
  - English
  - Français
  - Português
  - Deutsch
- 📊 Visualización dinámica de habilidades
- 📝 Contenido gestionado en archivos Markdown
- 🔄 Actualización automática de edad
- 📥 Exportación a formato Word
- 🔒 Manejo seguro de API keys

## Requisitos

```bash
pip install -r requirements.txt
```

## Configuración

1. Crear archivo `.streamlit/secrets.toml`:

```toml
GOOGLE_API_KEY = "tu-api-key-de-gemini"
```

2. Ejecutar la aplicación:

```bash
streamlit run CV.py
```

## Estructura del Proyecto

```plaintext
CV/
├── CV.py                    # Archivo principal
├── generate_word.py         # Generador de documentos Word
├── Header.jpg              # Imagen de cabecera
├── Foto.jpg               # Foto de perfil
├── requirements.txt        # Dependencias
├── .streamlit/
│   └── secrets.toml       # Configuración API
├── .gitignore            # Configuración de Git
└── markdown/             # Contenido del CV
    ├── perfil_profesional.md
    ├── experiencia_profesional.md
    ├── experiencia_academica.md
    └── idiomas.md
```

## Tecnologías Utilizadas

- Python 3.9+
- Streamlit
- Google Generative AI (Gemini)
- python-docx
- python-dotenv
- Markdown

## Funcionalidades

- Traducción automática del contenido
- Visualización de progreso en idiomas
- Cálculo dinámico de edad
- Exportación a documento Word
- Interfaz multilingüe
- Gestión segura de credenciales

## Autor

Luis Yael Carmona Gutiérrez
[LinkedIn](https://www.linkedin.com/in/luisyaelcarmona/)