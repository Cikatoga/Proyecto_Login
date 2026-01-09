import tkinter as tk
from tkinter import messagebox, simpledialog
from auth import registrar, login
from password_reset import recuperar_contrasena
from chuck_api import chiste_aleatorio, obtener_categorias, chiste_por_categoria
from scraper import obtener_frase_scraping  

# ---------------- LOGIN ----------------
def ventana_login():
    ventana = tk.Tk()
    ventana.title("Login Proyecto")
    ventana.geometry("300x200")

    tk.Label(ventana, text="Correo:").pack(pady=5)
    entry_correo = tk.Entry(ventana)
    entry_correo.pack()

    tk.Label(ventana, text="Contraseña:").pack(pady=5)
    entry_contrasena = tk.Entry(ventana, show="*")
    entry_contrasena.pack()

    # --- Funciones internas ---
    def intentar_login():
        correo = entry_correo.get()
        contrasena = entry_contrasena.get()
        if login(correo, contrasena):
            messagebox.showinfo("Login OK", "¡Has iniciado sesión!")
            ventana.destroy()
            ventana_principal()
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")

    def intentar_registro():
        correo = entry_correo.get()
        contrasena = entry_contrasena.get()
        exito, mensaje = registrar(correo, contrasena)
        if exito:
            messagebox.showinfo("Registro", mensaje)
        else:
            messagebox.showerror("Error", mensaje)

    # --- Botones ---
    tk.Button(ventana, text="Iniciar sesión", command=intentar_login).pack(pady=5)
    tk.Button(ventana, text="Registrarse", command=intentar_registro).pack()
    tk.Button(ventana, text="Recuperar contraseña", command=recuperar_contrasena).pack(pady=5)

    ventana.mainloop()


# ---------------- MENÚ PRINCIPAL ----------------
def ventana_principal():
    ventana = tk.Tk()
    ventana.title("Menú Principal")
    ventana.geometry("400x300")

    tk.Label(ventana, text="Bienvenido al proyecto de Chuck Norris y frases", font=("Arial", 12)).pack(pady=10)

    # --- Botones ---
    tk.Button(ventana, text="Chiste aleatorio", width=25, command=mostrar_chiste_aleatorio).pack(pady=5)
    tk.Button(ventana, text="Chiste por categoría", width=25, command=mostrar_chiste_categoria).pack(pady=5)
    tk.Button(ventana, text="Ver categorías", width=25, command=mostrar_categorias).pack(pady=5)
    tk.Button(ventana, text="Frase humor aleatoria", width=25, command=mostrar_frase).pack(pady=5)
    tk.Button(ventana, text="Salir", width=25, command=ventana.destroy).pack(pady=10)

    ventana.mainloop()


# ---------------- FUNCIONES DE MENÚ ----------------
def mostrar_chiste_aleatorio():
    chiste = chiste_aleatorio()
    messagebox.showinfo("Chiste Aleatorio", chiste)

def mostrar_categorias():
    categorias = obtener_categorias()
    messagebox.showinfo("Categorías", ", ".join(categorias))

def mostrar_chiste_categoria():
    categorias = obtener_categorias()
    cat = simpledialog.askstring("Categoría", f"Escribe una categoría:\n{', '.join(categorias)}")
    if cat and cat in categorias:
        chiste = chiste_por_categoria(cat)
        messagebox.showinfo(f"Chiste {cat}", chiste)
    else:
        messagebox.showerror("Error", "Categoría inválida")

def mostrar_frase():
    # ahora usamos la versión que devuelve original y traducida
    original, traducida = obtener_frase_scraping()
    messagebox.showinfo("Frase Humor Aleatoria", f"Original: {original}\n\nTraducida: {traducida}")


# ---------------- INICIO ----------------
if __name__ == "__main__":
    ventana_login()
