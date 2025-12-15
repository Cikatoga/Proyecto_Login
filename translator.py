# translator.py

from googletrans import Translator

translator = Translator()

def traducir_ingles_espanol(texto):
    resultado = translator.translate(texto, src='en', dest='es')
    return resultado.text
