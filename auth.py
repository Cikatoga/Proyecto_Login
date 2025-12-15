import getpass
from utils import (
    cargar_usuarios,
    guardar_usuarios,
    validar_correo,
    validar_contrasena,
    hash_contrasena,
    verificar_contrasena
)

def registrar():
    print("\n--- REGISTRO ---")

    usuarios = cargar_usuarios()

    while True:
        correo = input("Correo: ").strip()

        if not validar_correo(correo):
            print("❌ Correo inválido.\n")
            continue
        if correo in usuarios:
            print("❌ Este correo ya está registrado.\n")
            continue
        break

    while True:
        contrasena = getpass.getpass("Contraseña: ")
        if not validar_contrasena(contrasena):
            print("❌ Debe tener 6 caracteres, 1 mayúscula y 1 número.\n")
            continue

        repetir = getpass.getpass("Repite contraseña: ")
        if repetir != contrasena:
            print("❌ No coinciden.\n")
            continue
        break

    usuarios[correo] = hash_contrasena(contrasena)
    guardar_usuarios(usuarios)
    print("✅ Registro exitoso.")
    pass

def login():
    print("\n--- LOGIN ---")

    usuarios = cargar_usuarios()

    correo = input("Correo: ").strip()

    if correo not in usuarios:
        print("❌ El correo no existe.")
        return False

    contrasena = getpass.getpass("Contraseña: ")

    if verificar_contrasena(contrasena, usuarios[correo]):
        print("✅ Inicio de sesión exitoso.")
        return True

    print("❌ Contraseña incorrecta.")
    return False
    pass
