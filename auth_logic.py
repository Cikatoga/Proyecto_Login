import re
import bcrypt
import json
import os

# Archivos de base de datos local
DB_FILE = "usuarios.json"
PERFIL_FILE = "perfiles.json"

# --- 1. VALIDACIÓN Y SEGURIDAD ---

def validar_password(password, confirm_password):
    if password != confirm_password:
        return False, "Las contraseñas no coinciden"
    if len(password) < 8:
        return False, "Mínimo 8 caracteres"
    if len(re.findall(r'[A-Z]', password)) < 1:
        return False, "Al menos una mayúscula"
    if len(re.findall(r'\d', password)) < 1:
        return False, "Al menos 1 número"
    return True, "Ok"

# --- 2. GESTIÓN DE USUARIOS ---

def registrar_usuario(email, password):
    email = email.strip().lower()
    datos = {}
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as file:
            try:
                datos = json.load(file)
            except:
                datos = {}
    
    if email in datos:
        return False, "El correo ya está registrado"
    
    salt = bcrypt.gensalt()
    hash_pw = bcrypt.hashpw(password.encode('utf-8'), salt)
    datos[email] = hash_pw.decode('utf-8')
    
    with open(DB_FILE, "w") as file:
        json.dump(datos, file, indent=4)
    return True, "Registro exitoso"

def verificar_login(email, password):
    if not os.path.exists(DB_FILE):
        return False, "No hay usuarios registrados"
    with open(DB_FILE, "r") as file:
        datos = json.load(file)
    
    email = email.strip().lower()
    if email not in datos:
        return False, "Usuario no encontrado"
    
    if bcrypt.checkpw(password.encode('utf-8'), datos[email].encode('utf-8')):
        return True, "Acceso concedido"
    return False, "Contraseña incorrecta"

# --- 3. GESTIÓN DE PERFILES Y LOGROS ---

def obtener_perfil(email):
    if os.path.exists(PERFIL_FILE):
        with open(PERFIL_FILE, "r") as f:
            try:
                data = json.load(f)
                return data.get(email)
            except:
                return None
    return None

def guardar_perfil(email, datos_nuevos):
    todos = {}
    if os.path.exists(PERFIL_FILE):
        with open(PERFIL_FILE, "r") as f:
            try:
                todos = json.load(f)
            except:
                todos = {}
    
    perfil_actual = todos.get(email, {})
    perfil_actual.update(datos_nuevos)
    todos[email] = perfil_actual
    
    with open(PERFIL_FILE, "w") as f:
        json.dump(todos, f, indent=4)
    return True

def calcular_logros(email):
    perfil = obtener_perfil(email) or {}
    favs = perfil.get("favoritos", [])
    watch = perfil.get("watchlist", [])
    coments = perfil.get("comentarios", {})
    
    logros = []
    
    # Logros por cantidad de favoritos
    if len(favs) >= 1: logros.append("🎬 Primer Fan (1 Favorito)")
    if len(favs) >= 5: logros.append("🥈 Cinéfilo de Plata (5 Favs)")
    if len(favs) >= 10: logros.append("🥇 Maestro del Cine (10 Favs)")
    
    # Logros por Watchlist
    if len(watch) >= 5: logros.append("🔖 Planificador (5 en Watchlist)")
    
    # Logros por Notas/Comentarios
    if len(coments) >= 3: logros.append("✍️ Crítico Novel (3 Notas)")
    if len(coments) >= 7: logros.append("🧐 Crítico Expert (7 Notas)")
    
    # Logro por variedad de géneros (si tiene favoritos de 3 géneros distintos)
    generos_distintos = set()
    for f in favs:
        # Intentamos obtener género si la API lo devolvió, sino usamos el cine_favorito del perfil
        generos_distintos.add(f.get("Genre", "Unknown").split(",")[0])
    
    if len(generos_distintos) >= 3:
        logros.append("🌈 Explorador de Géneros")

    return logros

# --- 4. LISTAS PERSONALIZADAS ---

def agregar_a_favoritos(email, peli):
    perfil = obtener_perfil(email) or {}
    favs = perfil.get("favoritos", [])
    if any(f.get('imdbID') == peli.get('imdbID') for f in favs):
        return False, "Ya está en favoritos ❤️"
    favs.append(peli)
    guardar_perfil(email, {"favoritos": favs})
    return True, "Añadida a favoritos ✨"

def obtener_favoritos(email):
    p = obtener_perfil(email)
    return p.get("favoritos", []) if p else []

def agregar_a_watchlist(email, peli):
    perfil = obtener_perfil(email) or {}
    watch = perfil.get("watchlist", [])
    if any(w.get('imdbID') == peli.get('imdbID') for w in watch):
        return False, "Ya está en la lista 🔖"
    watch.append(peli)
    guardar_perfil(email, {"watchlist": watch})
    return True, "Guardada para ver 🔖"

def obtener_watchlist(email):
    p = obtener_perfil(email)
    return p.get("watchlist", []) if p else []

# --- 5. INTERACCIONES ADICIONALES ---

def guardar_comentario(email, imdbID, texto):
    perfil = obtener_perfil(email) or {}
    coments = perfil.get("comentarios", {})
    coments[imdbID] = texto
    guardar_perfil(email, {"comentarios": coments})
    return True

def agregar_al_historial(email, busqueda):
    perfil = obtener_perfil(email) or {}
    hist = perfil.get("historial", [])
    if busqueda in hist:
        hist.remove(busqueda)
    hist.insert(0, busqueda)
    guardar_perfil(email, {"historial": hist[:5]})
    return True

def calcular_logros(email):
    """
    Analiza la actividad del usuario y devuelve una lista de medallas (emojis).
    """
    perfil = obtener_perfil(email)
    if not perfil:
        return []

    logros = []
    
    # Medalla por cantidad de Favoritos
    favs = perfil.get("favoritos", [])
    if len(favs) >= 1:
        logros.append("❤️ Fan Principiante")
    if len(favs) >= 5:
        logros.append("🔥 Coleccionista")

    # Medalla por usar la Watchlist
    watch = perfil.get("watchlist", [])
    if len(watch) >= 3:
        logros.append("🔖 Planeador Pro")

    # Medalla por escribir Notas/Comentarios
    comentarios = perfil.get("comentarios", {})
    if len(comentarios) >= 1:
        logros.append("✍️ Crítico de Cine")

    # Medalla por Historial de búsqueda
    historial = perfil.get("historial", [])
    if len(historial) >= 10:
        logros.append("🔍 Investigador")

    return logros

# --- FUNCIÓN AGREGADA ---
def obtener_donde_ver(titulo):
    """Genera enlace de búsqueda para plataformas de streaming."""
    query = titulo.replace(" ", "+")
    return f"https://www.justwatch.com/es/buscar?q={query}"