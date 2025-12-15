from auth import registrar, login
from password_reset import recuperar_contrasena
from chuck_api import chiste_aleatorio, obtener_categorias, chiste_por_categoria
from translator import traducir_ingles_espanol

def menu_chuck():
    print("\n--- MENÚ CHUCK NORRIS ---")
    print("1. Chiste aleatorio")
    print("2. Chiste por categoría")
    print("3. Ver categorías")
    print("4. Salir")

    opcion = input("Elige una opción: ")

    if opcion == "1":
        chiste = chiste_aleatorio()
        print("\nChiste original:")
        print(chiste)
        print("\nChiste en español:")
        print(traducir_ingles_espanol(chiste))

    elif opcion == "2":
        categorias = obtener_categorias()
        print("\nCategorías disponibles:")
        print(", ".join(categorias))

        cat = input("Escribe una categoría: ")

        chiste = chiste_por_categoria(cat)
        print("\nChiste original:")
        print(chiste)
        print("\nChiste en español:")
        print(traducir_ingles_espanol(chiste))

    elif opcion == "3":
        categorias = obtener_categorias()
        print("\nCategorías:")
        print(", ".join(categorias))

    elif opcion == "4":
        print("Volviendo...")
    else:
        print("Opción no válida.")

def main():
    while True:
        print("\n--- MENÚ PRINCIPAL ---")
        print("1. Registrarse")
        print("2. Iniciar sesión")
        print("3. Recuperar contraseña")
        print("4. Salir")

        opcion = input("Elige una opción: ")

        if opcion == "1":
            registrar()

        elif opcion == "2":
            if login():           # <- login devuelve True si fue exitoso
                menu_chuck()     # <- Aquí se llama lo de la API
            else:
                print("Error al iniciar sesión.")

        elif opcion == "3":
            recuperar_contrasena()

        elif opcion == "4":
            print("Adiós :)")
            break

        else:
            print("Opción inválida.")

if __name__ == "__main__":
    main()
