import requests
import random
from scraping_logic import obtener_disponibilidad_trailer

API_KEY = "8e8adb8b"

def buscar_recomendaciones(generos, seleccion_año, año_manual, tipo_opc):
    
    traduccion = {
        "Acción": "Action", "Comedia": "Comedy", "Drama": "Drama", 
        "Terror": "Horror", "Sci-Fi": "Sci-Fi", "Romance": "Romance", 
        "Documental": "Documentary", "Animación": "Animation"
    }
    
    favoritos = [traduccion[g] for g in generos if g in traduccion]
    if not favoritos: favoritos = ["Action"]
    
    tipo_busqueda = "movie" if "Película" in tipo_opc else "series"
    genero_elegido = random.choice(favoritos)
    
    años_dict = {
        "Estrenos (2020-2025)": "2023", "2015-2020": "2018", "2010-2015": "2012", 
        "2005-2010": "2007", "2000-2005": "2002", "90s Retro": "1995", "Clásicos": "1980"
    }
    
    # Lógica para "Todos los años"
    if seleccion_año == "Todos los años":
        año_api = ""
    else:
        año_api = año_manual if seleccion_año == "Ingresar año manualmente" else años_dict.get(seleccion_año, "")

    url_search = f"http://www.omdbapi.com/?s={genero_elegido}&y={año_api}&type={tipo_busqueda}&apikey={API_KEY}"
    
    try:
        res = requests.get(url_search, timeout=5).json()
        if res.get("Response") == "True":
            lista = res["Search"]
            seleccionados = random.sample(lista, min(3, len(lista)))
            detalles = []
            for item in seleccionados:
                url_det = f"http://www.omdbapi.com/?i={item['imdbID']}&apikey={API_KEY}"
                peli_data = requests.get(url_det).json()
                plataformas, trailer = obtener_disponibilidad_trailer(peli_data['Title'])
                peli_data['info_streaming'] = plataformas
                peli_data['trailer'] = trailer
                detalles.append(peli_data)
            return True, detalles
        return False, "No se encontraron recomendaciones."
    except:
        return False, "Error de red."

def buscar_pelicula_especifica(titulo):
    from scraping_logic import obtener_disponibilidad
    url = f"http://www.omdbapi.com/?t={titulo.replace(' ', '+')}&apikey={API_KEY}"
    try:
        peli_data = requests.get(url, timeout=5).json()
        if peli_data.get("Response") == "True":
            plataformas, trailer = obtener_disponibilidad_trailer(peli_data['Title'])
            peli_data['info_streaming'] = plataformas
            peli_data['trailer'] = trailer

            return True, peli_data
        return False, "No encontrada."
    except:
        return False, "Error."