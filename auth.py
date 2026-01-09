# auth.py

from utils import (
    cargar_usuarios,
    guardar_usuarios,
    validar_correo,
    validar_contrasena,
    hash_contrasena,
    verificar_contrasena
)

# ---------------- LOGIN ----------------
def login(correo, contrasena):
    """
    Login para interfaz gráfica.
    Devuelve True si el login es correcto, False si no.
    """
    usuarios = cargar_usuarios()

    if correo not in usuarios:
        return False

    if verificar_contrasena(contrasena, usuarios[correo]):
        return True

    return False

# ---------------- REGISTRO ----------------
def registrar(correo, contrasena):
    """
    Registro para interfaz gráfica.
    Devuelve (exito, mensaje)
    exito -> True si se registró correctamente
    mensaje -> texto explicativo
    """
    usuarios = cargar_usuarios()

    if not validar_correo(correo):
        return False, "Correo inválido."
    if correo in usuarios:
        return False, "Correo ya registrado."
    if not validar_contrasena(contrasena):
        return False, "Contraseña inválida. Debe tener al menos 6 caracteres, 1 mayúscula y 1 número."

    usuarios[correo] = hash_contrasena(contrasena)
    guardar_usuarios(usuarios)
    return True, "Registro exitoso."
