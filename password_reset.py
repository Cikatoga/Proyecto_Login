# password_reset.py

from utils import cargar_usuarios

def recuperar_contrasena():
    print("\n--- RECUPERAR CONTRASEÑA ---")
    correo = input("Ingresa tu correo registrado: ").strip()

    usuarios = cargar_usuarios()

    if correo not in usuarios:
        print("Este correo no está registrado.")
        return

    # Aquí simulas el envío del correo
    print(f"Se ha enviado un correo de recuperación a: {correo}")
    print("Revisa tu bandeja de entrada.")
