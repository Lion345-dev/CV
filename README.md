# CV Digital Interactivo

Aplicación web interactiva construida con Streamlit para mostrar mi Curriculum Vitae con capacidades de traducción automática.

## Características

- 📱 Interfaz responsiva y moderna
- 🌐 Soporte multilingüe usando Google Gemini API
- 📊 Visualización dinámica de habilidades
- 📝 Contenido gestionado en archivos Markdown
- 🔄 Actualización automática de edad

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

```

CV/
├── CV.py                    # Archivo principal
├── Header.jpg              # Imagen de cabecera
├── requirements.txt        # Dependencias
├── .streamlit/
│   └── secrets.toml       # Configuración API
└── markdown/
    ├── perfil_profesional.md
    ├── experiencia_profesional.md
    ├── experiencia_academica.md
    └── idiomas.md
```

## Tecnologías Utilizadas

- Python 3.9+
- Streamlit
- Google Generative AI (Gemini)
- Markdown

## Autor

Luis Yael Carmona Gutiérrez
[LinkedIn](https://www.linkedin.com/in/luisyaelcarmona/)