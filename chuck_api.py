import requests
from translator import traducir_texto

API_URL = "https://api.chucknorris.io/jokes"

def chiste_aleatorio():
    """Devuelve un chiste aleatorio traducido."""
    try:
        resp = requests.get(f"{API_URL}/random")
        data = resp.json()
        chiste = data.get("value", "No se encontró chiste.")
        return traducir_texto(chiste)
    except Exception as e:
        return f"Error obteniendo chiste: {e}"

def obtener_categorias():
    """Devuelve una lista de categorías."""
    try:
        resp = requests.get(f"{API_URL}/categories")
        return resp.json()
    except Exception as e:
        return ["Error obteniendo categorías"]

def chiste_por_categoria(categoria):
    """Devuelve un chiste de una categoría traducido."""
    try:
        resp = requests.get(f"{API_URL}/random?category={categoria}")
        data = resp.json()
        chiste = data.get("value", "No se encontró chiste.")
        return traducir_texto(chiste)
    except Exception as e:
        return f"Error obteniendo chiste: {e}"
