import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

HEADERS = {"User-Agent": "Mozilla/5.0"}

def limpiar_titulo(titulo):
    return titulo.lower().replace(":", "").replace("'", "").replace(" ", "-")

def obtener_disponibilidad_trailer(titulo):
    slug = limpiar_titulo(titulo)
    url = f"https://www.justwatch.com/es/pelicula/{slug}"
    plataformas = {}
    trailer = None
    
    try:
        # Timeout para que los botones no se queden "colgados"
        r = requests.get(url, headers=HEADERS, timeout=5)
        if r.status_code != 200:
            return plataformas, trailer

        soup = BeautifulSoup(r.text, "html.parser")

        for a in soup.find_all("a", href=True):
            link = a["href"]
            if "netflix.com" in link: plataformas["Netflix"] = link
            elif "primevideo.com" in link: plataformas["Prime Video"] = link
            elif "disneyplus.com" in link: plataformas["Disney+"] = link
            elif "hbomax.com" in link or "max.com" in link: plataformas["HBO Max"] = link

        for a in soup.find_all("a", href=True):
            if "youtube.com/watch" in a["href"]:
                trailer = a["href"]
                break

        if not trailer:
            trailer = obtener_trailer_youtube(titulo)

        return plataformas, trailer
    except Exception:
        # Si hay error, devolvemos lo que tengamos para no romper el main.py
        return plataformas, trailer

def obtener_trailer_youtube(titulo):
    query = titulo + " trailer español"
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    try:
        driver.get(f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}")
        time.sleep(2)  
        video = driver.find_element(By.ID, "video-title")
        link = video.get_attribute("href")
        driver.quit()
        return link
    except:
        driver.quit()
        return None