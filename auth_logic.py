import re
import bcrypt
import json
import os

DB_FILE = "usuarios.json"

def validar_password(password, confirm_password):
    if password != confirm_password:
        return False, "Las contraseñas no coinciden"
    if len(password) < 8:
        return False, "Mínimo 8 caracteres"
    if len(re.findall(r'[A-Z]', password)) < 1:
        return False, "Necesitas 2 mayúsculas"
    if len(re.findall(r'\d', password)) < 1:
        return False, "Necesitas al menos 1 número"
    if len(re.findall(r'[!@#$%^&*(),.?":{}|<>]', password)) < 1:
        return False, "Falta carácter especial"
    return True, "Ok"

def registrar_usuario(email, password):
    datos = {}
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as file:
            try: datos = json.load(file)
            except: datos = {}

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
    if email not in datos:
        return False, "Usuario no encontrado"
    
    stored_hash = datos[email].encode('utf-8')
    if bcrypt.checkpw(password.encode('utf-8'), stored_hash):
        return True, "Acceso concedido"
    return False, "Contraseña incorrecta"

def guardar_perfil(email, datos_perfil):
    archivo_perfil = "perfiles.json"
    todos_los_perfiles = {}
    
    if os.path.exists(archivo_perfil):
        with open(archivo_perfil, "r") as f:
            try: todos_los_perfiles = json.load(f)
            except: todos_los_perfiles = {}
    
    todos_los_perfiles[email] = datos_perfil
    with open(archivo_perfil, "w") as f:
        json.dump(todos_los_perfiles, f, indent=4)
    return True

# ESTA ES LA FUNCIÓN QUE FALTABA
def obtener_perfil(email):
    archivo_perfil = "perfiles.json"
    if os.path.exists(archivo_perfil):
        with open(archivo_perfil, "r") as f:
            try:
                todos = json.load(f)
                return todos.get(email)
            except:
                return None
    return None