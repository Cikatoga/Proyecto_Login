import customtkinter as ctk
import requests
import webbrowser
from PIL import Image
from io import BytesIO
from tkcalendar import DateEntry

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

    def mostrar_datos_personales(self):
        self.limpiar_frame()

        ctk.CTkLabel(self.main_container, text="Cuéntanos sobre ti 🎬", font=("Roboto", 26, "bold"), text_color="#1a1a1a" ).pack(pady=15)

        self.nombre_ent = ctk.CTkEntry( self.main_container, placeholder_text="Tu nombre", width=280)
        self.nombre_ent.pack(pady=8)

        ctk.CTkLabel(
            self.main_container,
            text="Fecha de nacimiento",
            font=("Roboto", 13, "bold")
        ).pack(pady=(10, 2))

                # --- FECHA DE NACIMIENTO ---
        frame_fecha = ctk.CTkFrame(self.main_container, fg_color="transparent")
        frame_fecha.pack(pady=8)

        # Día
        self.dia_opc = ctk.CTkOptionMenu(
            frame_fecha,
            values=[f"{d:02d}" for d in range(1, 32)],
            width=70
        )
        self.dia_opc.pack(side="left", padx=4)

        # Mes (nombre)
        self.meses = [
            "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
            "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
        ]

        self.mes_opc = ctk.CTkOptionMenu(
            frame_fecha,
            values=self.meses,
            width=130
        )
        self.mes_opc.pack(side="left", padx=4)

        # Año
        self.año_opc = ctk.CTkOptionMenu(
            frame_fecha,
            values=[str(y) for y in range(2025, 1900, -1)],
            width=90
        )
        self.año_opc.pack(side="left", padx=4)



        self.genero_opc = ctk.CTkOptionMenu( self.main_container, values=["Masculino", "Femenino", "Otro"], width=280, fg_color="#6200ee")
        self.genero_opc.pack(pady=8)

        ctk.CTkLabel(self.main_container, text="¿Qué géneros te gustan?", font=("Roboto", 14, "bold")).pack(pady=(15, 5))

        self.generos_pref = {}
        generos = ["Acción", "Comedia", "Drama", "Terror", "Sci-Fi", "Romance", "Documental", "Animación"]

        for g in generos:
            var = ctk.StringVar(value="off")
            ctk.CTkCheckBox(self.main_container, text=g, variable=var, onvalue=g, offvalue="off").pack(anchor="w", padx=130)
            self.generos_pref[g] = var

        self.error_lbl = ctk.CTkLabel(self.main_container, text="", text_color="#ff5555")
        self.error_lbl.pack(pady=5)

        ctk.CTkButton(
            self.main_container,
            text="Guardar y continuar ➡",
            fg_color="#03dac6",
            text_color="#121212",
            font=("Roboto", 14, "bold"),
            command=self.guardar_datos_personales,
            width=280
        ).pack(pady=20)

    def guardar_datos_personales(self):
        nombre = self.nombre_ent.get().strip()

        dia = self.dia_opc.get()
        mes_nombre = self.mes_opc.get()
        año = self.año_opc.get()
        mes_num = f"{self.meses.index(mes_nombre) + 1:02d}"
        fecha = f"{dia}/{mes_num}/{año}"

        genero = self.genero_opc.get()
        cine_favorito = [v.get() for v in self.generos_pref.values() if v.get() != "off"]

        if not nombre or not fecha:
            self.error_lbl.configure(text="Completa todos los campos")
            return

        datos_perfil = {"nombre": nombre, "fecha_nacimiento": fecha, "genero": genero, "cine_favorito": cine_favorito}

        guardar_perfil(self.usuario_actual, datos_perfil)

        # Entrar a la app principal
        self.mostrar_experiencia_diaria(nombre)


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

            # Poster, título, rating, sinopsis...
            if peli.get("Poster") != "N/A":
                try:
                    res_img = requests.get(peli["Poster"], timeout=5)
                    ctk_img = ctk.CTkImage(Image.open(BytesIO(res_img.content)), size=(150, 210))
                    ctk.CTkLabel(card, image=ctk_img, text="").pack(pady=10)
                except: 
                    pass
            ctk.CTkLabel(card, text=peli["Title"], font=("Roboto", 18, "bold"), text_color="#6200ee", wraplength=250).pack()
            ctk.CTkLabel(card, text=f"⭐ IMDB: {peli.get('imdbRating', 'N/A')} | 📅 {peli.get('Year', 'N/A')}", font=("Roboto", 11, "italic")).pack()
            ctk.CTkLabel(card, text=peli.get("Plot", "Sin sinopsis."), font=("Roboto", 11), text_color="#444444", wraplength=280).pack(pady=10)

            # --- Botón Comprobar disponibilidad ---
            # Este va primero
            def toggle_disponibilidad(c_frame=None, p=peli):
                # Limpiar botones si ya existen
                if c_frame.winfo_children():
                    for w in c_frame.winfo_children():
                        w.destroy()
                else:
                    # Crear botones de streaming
                    if p.get("info_streaming"):
                        for plataforma, link in p["info_streaming"].items():
                            ctk.CTkButton(
                                c_frame,
                                text=f"Ver en {plataforma}",
                                command=lambda u=link: self.abrir_enlace(u),
                                width=200,
                                fg_color="#6200ee",
                                text_color="white"
                            ).pack(pady=2)
                    else:
                        ctk.CTkLabel(c_frame, text="❌ No disponible en ninguna plataforma", text_color="gray").pack(pady=2)

            check_btn = ctk.CTkButton(card, text="🎬 Comprobar disponibilidad", fg_color="#444")
            check_btn.pack(pady=5)

            # --- Frame vacío para botones de streaming (justo debajo del botón) ---
            streaming_frame = ctk.CTkFrame(card, fg_color="transparent")
            streaming_frame.pack(pady=0)
            # Ahora enlazamos el botón para alternar
            check_btn.configure(command=lambda c_frame=streaming_frame, p=peli: toggle_disponibilidad(c_frame, p))

            # --- Botón Ver Tráiler (siempre debajo del frame) ---
            trailer_url = peli.get("trailer")
            if not trailer_url:
                trailer_url = "https://www.youtube.com/results?search_query=" + peli["Title"].replace(" ", "+") + "+trailer"
            ctk.CTkButton(card, text="📺 Ver Tráiler", command=lambda u=trailer_url: self.abrir_enlace(u), width=200, fg_color="#03dac6", text_color="#121212").pack(pady=5)

        # --- Botón volver ---
        ctk.CTkButton(self.main_container, text="⬅ Volver", fg_color="#6200ee", width=280, command=lambda: self.mostrar_experiencia_diaria(self.nombre_usuario)).pack(pady=15)

    def logic_login(self):
        email, pw = self.email_ent.get(), self.pw_ent.get()
        exito, msg = verificar_login(email, pw)
        if exito:
            self.usuario_actual = email
            p = obtener_perfil(email)
            if p and p.get("nombre"): 
                self.mostrar_experiencia_diaria(p["nombre"])
            else: 
                self.mostrar_datos_personales()
        else: 
            self.error_lbl.configure(text=msg)

    def logic_registro(self):
        e, p, c = self.email_ent.get(), self.pw_ent.get(), self.pw_conf_ent.get()
        valido, msg = validar_password(p, c)

        if valido:
            exito, msg = registrar_usuario(e, p)
            if exito:
                self.mostrar_login()  # Solo si se registró correctamente
            else:
                self.error_lbl.configure(text=msg)  # Mostrar mensaje: correo ya registrado
        else:
            self.error_lbl.configure(text=msg)  # Mostrar mensaje de validación de contraseña

if __name__ == "__main__":
    app = App()
    app.mainloop()