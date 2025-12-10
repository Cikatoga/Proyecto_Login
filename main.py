import json
import os
import re
import getpass

ARCHIVO_USUARIOS = "usuarios.json"


# ------------------ FUNCIONES ------------------

# Cargar usuarios desde JSON
def cargar_usuarios():
    if not os.path.exists(ARCHIVO_USUARIOS):
        return {}
    with open(ARCHIVO_USUARIOS, "r", encoding="utf-8") as f:
        return json.load(f)


# Guardar usuarios en JSON
def guardar_usuarios(usuarios):
    with open(ARCHIVO_USUARIOS, "w", encoding="utf-8") as f:
        json.dump(usuarios, f, indent=4, ensure_ascii=False)


# Validar correo
def validar_correo(correo):
    patron = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.fullmatch(patron, correo) is not None


# Validar contraseña (mínimo 6 caracteres, 1 mayúscula, 1 número)
def validar_contrasena(contrasena):
    patron = r"^(?=.*[A-Z])(?=.*\d).{6,}$"
    return re.fullmatch(patron, contrasena) is not None


# Registrar usuario
def registrar():
    print("\n--- REGISTRO ---")
    correo = input("Ingresa tu correo: ").strip()

    if not validar_correo(correo):
        print("❌ Correo inválido.")
        return

    usuarios = cargar_usuarios()

    if correo in usuarios:
        print("❌ Ese correo ya existe.")
        return

    contrasena = getpass.getpass("Crea una contraseña, recuerda que debe tener como mínimo 6 carácteres, 1 mayúscula y 1 número: ")

    if not validar_contrasena(contrasena):
        print("❌ La contraseña debe tener mínimo 6 caracteres, 1 mayúscula y 1 número.")
        return

    usuarios[correo] = contrasena
    guardar_usuarios(usuarios)

    print("✅ Registro exitoso.")


# Login de usuario
def login():
    print("\n--- LOGIN ---")
    correo = input("Ingresa tu correo: ").strip()

    usuarios = cargar_usuarios()

    if correo not in usuarios:
        print("❌ Este correo no está registrado.")
        return

    contrasena = getpass.getpass("Ingresa tu contraseña: ")

    if usuarios[correo] == contrasena:
        print("✅ Inicio de sesión exitoso.")
    else:
        print("❌ Contraseña incorrecta.")


# ------------------ MENÚ PRINCIPAL ------------------

def main():
    while True:
        print("\n===== MENÚ =====")
        print("1. Registrarse")
        print("2. Iniciar sesión")
        print("3. Salir")

        opcion = input("Elige una opción: ").strip()

        if opcion == "1":
            registrar()
        elif opcion == "2":
            login()
        elif opcion == "3":
            print("👋 ¡Hasta luego!")
            break
        else:
            print("❌ Opción no válida.")


if __name__ == "__main__":
    main()
