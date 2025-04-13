import requests
from bs4 import BeautifulSoup

def scrape_linkedin_profile(profile_url):
    """
    Scrapea datos básicos de un perfil público de LinkedIn.
    Args:
        profile_url (str): URL del perfil de LinkedIn.
    Returns:
        dict: Datos del perfil.
    """
    try:
        # Simular un navegador para evitar bloqueos
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(profile_url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

        # Extraer datos básicos (esto es un ejemplo, ajusta según la estructura de LinkedIn)
        name = soup.find("h1").text.strip()
        headline = soup.find("h2").text.strip()
        experience = [
            exp.text.strip() for exp in soup.find_all("span", class_="experience-item")
        ]

        return {
            "name": name,
            "headline": headline,
            "experience": experience,
        }
    except Exception as e:
        return {"error": f"Error al obtener datos de LinkedIn: {str(e)}"}