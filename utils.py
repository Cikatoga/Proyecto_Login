import json
import os
import re
import bcrypt

RUTA_JSON = "usuarios.json"

def cargar_usuarios():
    if not os.path.exists(RUTA_JSON):
        return {}
    with open(RUTA_JSON, "r") as f:
        return json.load(f)

def guardar_usuarios(usuarios):
    with open(RUTA_JSON, "w") as f:
        json.dump(usuarios, f, indent=4)

def validar_correo(correo):
    patron = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(patron, correo) is not None

def validar_contrasena(contrasena):
    return (
        len(contrasena) >= 6 and
        any(c.isupper() for c in contrasena) and
        any(c.isdigit() for c in contrasena)
    )

def hash_contrasena(contrasena):
    return bcrypt.hashpw(contrasena.encode(), bcrypt.gensalt()).decode()

def verificar_contrasena(contrasena, hash_guardado):
    return bcrypt.checkpw(contrasena.encode(), hash_guardado.encode())
