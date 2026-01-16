import requests
# Importamos la lógica de scraping para que el main reciba también los trailers y plataformas
from scraping_logic import obtener_disponibilidad_trailer

API_KEY = "8e8adb8b"  # Tu clave real ya configurada

def buscar_pelicula_especifica(titulo):
    try:
        # CORRECCIÓN: Ahora usa la variable API_KEY correctamente
        url = f"http://www.omdbapi.com/?t={titulo}&apikey={API_KEY}&plot=full"
        response = requests.get(url)
        datos = response.json()

        if datos.get("Response") == "True":
            # CORRECCIÓN: Se envía solo el título como requiere tu scraping_logic.py
            plataformas, trailer = obtener_disponibilidad_trailer(datos.get("Title"))
            datos["info_streaming"] = plataformas
            datos["trailer"] = trailer
            return True, datos
        else:
            return False, "No encontrada"
    except Exception as e:
        print(f"Error en la búsqueda: {e}")
        return False, str(e)

def buscar_recomendaciones(generos, rango_año, año_manual, tipo):
    """Busca varias películas según los filtros seleccionados."""
    s_type = "movie" if "Película" in tipo else "series"
    
    year_query = ""
    if rango_año == "Ingresar año manualmente" and año_manual:
        year_query = f"&y={año_manual}"
    elif "2020-2025" in rango_año:
        year_query = "&y=2023"

    search_term = generos[0] if generos else "Movie"
    
    try:
        url = f"http://www.omdbapi.com/?s={search_term}&type={s_type}{year_query}&apikey={API_KEY}"
        res = requests.get(url).json()
        
        resultados_completos = []
        if res.get("Response") == "True":
            for item in res.get("Search")[:3]: 
                id_peli = item["imdbID"]
                # Pedimos plot=full para que el main.py muestre la sinopsis
                detalle = requests.get(f"http://www.omdbapi.com/?i={id_peli}&plot=full&apikey={API_KEY}").json()
                
                # CORRECCIÓN: Ajuste de argumentos para el scraping
                plataformas, trailer = obtener_disponibilidad_trailer(detalle.get("Title"))
                detalle["info_streaming"] = plataformas
                detalle["trailer"] = trailer
                
                resultados_completos.append(detalle)
            
            return True, resultados_completos
        return False, "No se hallaron resultados"
    except Exception as e:
        return False, str(e)