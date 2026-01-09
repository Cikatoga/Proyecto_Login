from deep_translator import GoogleTranslator
import requests
from bs4 import BeautifulSoup
import random

URL = "https://quotes.toscrape.com/tag/humor/"

def traducir_ingles_espanol(texto):
    return GoogleTranslator(source='en', target='es').translate(texto)

def obtener_frase_scraping():
    resp = requests.get(URL)
    soup = BeautifulSoup(resp.text, "html.parser")

    frases = soup.find_all("span", class_="text")
    if not frases:
        return "No se encontró ninguna frase."

    frase_random = random.choice(frases).get_text()

    frase_traducida = traducir_ingles_espanol(frase_random)

    return frase_random, frase_traducida
