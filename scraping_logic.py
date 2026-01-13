import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def limpiar_titulo(titulo):
    return titulo.lower().replace(":", "").replace("'", "").replace(" ", "-")

def obtener_disponibilidad_trailer(titulo):
    """
    Scraping desde JustWatch:
    - Plataformas con link directo
    - Trailer directo de YouTube
    """
    slug = limpiar_titulo(titulo)
    url = f"https://www.justwatch.com/es/pelicula/{slug}"

    plataformas = {}
    trailer = None

    try:
        r = requests.get(url, headers=HEADERS, timeout=6)
        if r.status_code != 200:
            return plataformas, trailer

        soup = BeautifulSoup(r.text, "html.parser")

        # --- SCRAPING PLATAFORMAS ---
        for a in soup.find_all("a", href=True):
            link = a["href"]

            if "netflix.com" in link:
                plataformas["Netflix"] = link
            elif "primevideo.com" in link:
                plataformas["Prime Video"] = link
            elif "disneyplus.com" in link:
                plataformas["Disney+"] = link
            elif "hbomax.com" in link or "max.com" in link:
                plataformas["HBO Max"] = link

        # --- SCRAPING TRÁILER ---
        for a in soup.find_all("a", href=True):
            if "youtube.com/watch" in a["href"]:
                trailer = a["href"]
                break

        return plataformas, trailer

    except Exception as e:
        return plataformas, trailer
