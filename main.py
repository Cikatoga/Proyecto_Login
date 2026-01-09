import customtkinter as ctk
import requests
import webbrowser
from PIL import Image
from io import BytesIO

from auth_logic import validar_password, registrar_usuario, verificar_login, obtener_perfil, guardar_perfil
from api_logic import buscar_recomendaciones, buscar_pelicula_especifica

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("550x950") 
        self.title("Qué veo 📺")
        self.configure(fg_color="#493061")
        self.usuario_actual = "" 
        self.nombre_usuario = ""
        
        self.main_container = ctk.CTkFrame(self, fg_color="#ffffff", corner_radius=15)
        self.main_container.pack(pady=30, padx=40, fill="both", expand=True)
        self.mostrar_login()

    def limpiar_frame(self):
        for widget in self.main_container.winfo_children():
            widget.destroy()

    def abrir_enlace(self, url):
        webbrowser.open(url)

    # --- PANTALLA DE DESPEDIDA ---
    def cerrar_sesion(self):
        self.limpiar_frame()
        ctk.CTkLabel(self.main_container, text="¡Hasta pronto! 👋", font=("Roboto", 28, "bold"), text_color="#6200ee").pack(pady=(100, 20))
        mensaje = "¡Gracias por visitarnos!\n\nTe esperamos cuando sea tiempo de\n\n✨ Netflix & Chill ✨"
        ctk.CTkLabel(self.main_container, text=mensaje, font=("Roboto", 18), text_color="#1a1a1a", wraplength=300).pack(pady=20)
        ctk.CTkLabel(self.main_container, text="🍿🎬🥤", font=("Roboto", 40)).pack(pady=20)
        ctk.CTkButton(self.main_container, text="Volver al Inicio", fg_color="#6200ee", command=self.mostrar_login).pack(pady=40)

    # --- VISTAS DE ACCESO ---
    def mostrar_login(self):
        self.limpiar_frame()
        ctk.CTkLabel(self.main_container, text="Iniciar Sesión 📺", font=("Roboto", 28, "bold"), text_color="#1a1a1a").pack(pady=20)
        self.email_ent = ctk.CTkEntry(self.main_container, placeholder_text="Correo electrónico", width=280)
        self.email_ent.pack(pady=10)
        self.pw_ent = ctk.CTkEntry(self.main_container, placeholder_text="Contraseña", show="*", width=280)
        self.pw_ent.pack(pady=10)
        self.error_lbl = ctk.CTkLabel(self.main_container, text="", text_color="#ff5555")
        self.error_lbl.pack(pady=5)
        ctk.CTkButton(self.main_container, text="Entrar", fg_color="#6200ee", command=self.logic_login, width=280).pack(pady=10)
        ctk.CTkButton(self.main_container, text="Crear Cuenta", fg_color="transparent", text_color="#6200ee", command=self.mostrar_registro).pack()

    def mostrar_registro(self):
        self.limpiar_frame()
        ctk.CTkLabel(self.main_container, text="Registro 📝", font=("Roboto", 28, "bold"), text_color="#1a1a1a").pack(pady=20)
        self.email_ent = ctk.CTkEntry(self.main_container, placeholder_text="Correo electrónico", width=280)
        self.email_ent.pack(pady=10)
        self.pw_ent = ctk.CTkEntry(self.main_container, placeholder_text="Contraseña", show="*", width=280)
        self.pw_ent.pack(pady=10)
        self.pw_conf_ent = ctk.CTkEntry(self.main_container, placeholder_text="Confirmar Contraseña", show="*", width=280)
        self.pw_conf_ent.pack(pady=10)
        self.error_lbl = ctk.CTkLabel(self.main_container, text="", text_color="#ff5555")
        self.error_lbl.pack(pady=5)
        ctk.CTkButton(self.main_container, text="Registrarse", fg_color="#6200ee", command=self.logic_registro, width=280).pack(pady=10)
        ctk.CTkButton(self.main_container, text="Volver al Login", fg_color="transparent", text_color="#6200ee", command=self.mostrar_login).pack()

    def mostrar_experiencia_diaria(self, nombre):
        self.limpiar_frame()
        self.nombre_usuario = nombre
        ctk.CTkLabel(self.main_container, text=f"Hola, {nombre} 🍿", font=("Roboto", 22, "bold"), text_color="#1a1a1a").pack(pady=10)

        # BUSCADOR DIRECTO
        self.busqueda_ent = ctk.CTkEntry(self.main_container, placeholder_text="Busca una peli...", width=280)
        self.busqueda_ent.pack(pady=5)
        ctk.CTkButton(self.main_container, text="🔍 Buscar Película", fg_color="#6200ee", command=self.ejecutar_busqueda_directa, width=280).pack(pady=(0,15))

        # RECOMENDACIONES (AÑOS ACTUALIZADOS)
        self.tipo_opc = ctk.CTkOptionMenu(self.main_container, values=["Quiero ver una Película 🎬", "Quiero ver una Serie 📺"], width=280, fg_color="#340949")
        self.tipo_opc.pack(pady=5)
        
        self.year_opc = ctk.CTkOptionMenu(self.main_container, 
                                         values=["Todos los años", "Estrenos (2020-2025)", "2015-2020", "2010-2015", "2005-2010", "2000-2005", "90s Retro", "Clásicos", "Ingresar año manualmente"], 
                                         width=280, fg_color="#6200ee", command=self.toggle_año_manual)
        self.year_opc.pack(pady=5)
        self.año_manual_ent = ctk.CTkEntry(self.main_container, placeholder_text="Año ej: 1994", width=280)

        # GÉNEROS (8 OPCIONES)
        self.check_vars = {}
        generos = ["Acción", "Comedia", "Drama", "Terror", "Sci-Fi", "Romance", "Documental", "Animación"]
        for g in generos:
            var = ctk.StringVar(value="off")
            ctk.CTkCheckBox(self.main_container, text=g, variable=var, onvalue=g, offvalue="off", text_color="#1a1a1a").pack(anchor="w", padx=110, pady=1)
            self.check_vars[g] = var

        ctk.CTkButton(self.main_container, text="Dime qué ver ✨", fg_color="#03dac6", text_color="#121212", font=("Roboto", 14, "bold"), command=self.ejecutar_recomendacion, width=280).pack(pady=20)
        ctk.CTkButton(self.main_container, text="Cerrar Sesión 🚪", fg_color="transparent", text_color="#6200ee", command=self.cerrar_sesion).pack(pady=10)

    def toggle_año_manual(self, seleccion):
        if seleccion == "Ingresar año manualmente": self.año_manual_ent.pack(pady=5)
        else: self.año_manual_ent.pack_forget()

    def ejecutar_busqueda_directa(self):
        t = self.busqueda_ent.get()
        if t:
            exito, res = buscar_pelicula_especifica(t)
            if exito: self.mostrar_resultados([res])

    def ejecutar_recomendacion(self):
        g_sel = [v.get() for v in self.check_vars.values() if v.get() != "off"]
        exito, resultados = buscar_recomendaciones(g_sel, self.year_opc.get(), self.año_manual_ent.get(), self.tipo_opc.get())
        if exito: self.mostrar_resultados(resultados)

    def mostrar_resultados(self, lista):
        self.limpiar_frame()
        scroll = ctk.CTkScrollableFrame(self.main_container, fg_color="transparent", height=650)
        scroll.pack(fill="both", expand=True, padx=10)

        for peli in lista:
            card = ctk.CTkFrame(scroll, fg_color="#f8f8f8", corner_radius=15, border_width=1, border_color="#eeeeee")
            card.pack(pady=15, fill="x", padx=5)
            
            if peli.get("Poster") != "N/A":
                try:
                    res_img = requests.get(peli["Poster"], timeout=5)
                    ctk_img = ctk.CTkImage(Image.open(BytesIO(res_img.content)), size=(150, 210))
                    ctk.CTkLabel(card, image=ctk_img, text="").pack(pady=10)
                except: pass
            
            ctk.CTkLabel(card, text=peli["Title"], font=("Roboto", 18, "bold"), text_color="#6200ee", wraplength=250).pack()
            ctk.CTkLabel(card, text=f"⭐ IMDB: {peli.get('imdbRating', 'N/A')} | 📅 {peli.get('Year', 'N/A')}", font=("Roboto", 11, "italic")).pack()
            
            url_g = f"https://www.google.com/search?q=donde+ver+{peli['Title'].replace(' ', '+')}"
            ctk.CTkButton(card, text=peli.get('info_streaming', 'Disponibilidad'), fg_color="#D81E5B", command=lambda u=url_g: self.abrir_enlace(u)).pack(pady=5)
            
            url_y = f"https://www.youtube.com/results?search_query={peli['Title'].replace(' ', '+')}+trailer"
            ctk.CTkButton(card, text="📺 Ver Tráiler", fg_color="#FF0000", command=lambda u=url_y: self.abrir_enlace(u)).pack(pady=5)
            
            ctk.CTkLabel(card, text=peli.get("Plot", "Sin sinopsis."), font=("Roboto", 11), text_color="#444444", wraplength=280).pack(pady=10)

        ctk.CTkButton(self.main_container, text="Volver 🔄", command=lambda: self.mostrar_experiencia_diaria(self.nombre_usuario), fg_color="#6200ee", width=280).pack(pady=10)

    def logic_login(self):
        email, pw = self.email_ent.get(), self.pw_ent.get()
        exito, msg = verificar_login(email, pw)
        if exito:
            self.usuario_actual = email
            p = obtener_perfil(email)
            if p and p.get("nombre"): self.mostrar_experiencia_diaria(p["nombre"])
            else: self.mostrar_datos_personales()
        else: self.error_lbl.configure(text=msg)

    def logic_registro(self):
        e, p, c = self.email_ent.get(), self.pw_ent.get(), self.pw_conf_ent.get()
        valido, msg = validar_password(p, c)
        if valido:
            registrar_usuario(e, p)
            self.mostrar_login()
        else: self.error_lbl.configure(text=msg)

if __name__ == "__main__":
    app = App()
    app.mainloop()