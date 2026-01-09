from deep_translator import GoogleTranslator

def traducir_ingles_espanol(texto):
    return GoogleTranslator(source='en', target='es').translate(texto)
