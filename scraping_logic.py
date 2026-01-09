import requests
from bs4 import BeautifulSoup

def obtener_disponibilidad(titulo_pelicula):
    # Buscamos específicamente dónde ver la película
    query = titulo_pelicula.replace(" ", "+") + "+donde+ver+streaming"
    url = f"https://www.google.com/search?q={query}"
    
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
    
    try:
        respuesta = requests.get(url, headers=headers, timeout=5)
        soup = BeautifulSoup(respuesta.text, "html.parser")
        
        # El scraping busca logotipos o nombres de plataformas en el texto de Google
        texto = soup.get_text().lower()
        
        plataformas = []
        if "netflix" in texto: plataformas.append("Netflix 🔴")
        if "disney" in texto: plataformas.append("Disney+ 🏰")
        if "prime video" in texto: plataformas.append("Prime Video 📦")
        if "hbo" in texto: plataformas.append("HBO Max 🎬")
        
        if plataformas:
            return "Disponible en: " + ", ".join(plataformas)
        return "Streaming: Consultar disponibilidad"
    except:
        return "Streaming: No se pudo verificar"