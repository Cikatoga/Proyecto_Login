import requests
from bs4 import BeautifulSoup

URL = "https://quotes.toscrape.com/tag/humor/"

def obtener_frase_scraping():
    resp = requests.get(URL)
    soup = BeautifulSoup(resp.text, "html.parser")

    frases = soup.find_all("span", class_="text")

    if not frases:
        return "No se encontró ninguna frase."

    return frases[0].get_text()
