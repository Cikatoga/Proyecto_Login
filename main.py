import customtkinter as ctk
import requests
import webbrowser
from PIL import Image
from io import BytesIO
import os
import threading
import random
from datetime import datetime

try:
    import pyperclip
except ImportError:
    os.system('pip install pyperclip')
    import pyperclip

# IMPORTACIÓN ACTUALIZADA
from auth_logic import (
    validar_password, registrar_usuario, verificar_login, 
    obtener_perfil, guardar_perfil, agregar_a_favoritos, 
    obtener_favoritos, agregar_a_watchlist, obtener_watchlist, 
    guardar_comentario, agregar_al_historial, calcular_logros,
    obtener_donde_ver
)
from api_logic import buscar_recomendaciones, buscar_pelicula_especifica

# CONFIGURACIÓN DE TEMA GLOBAL
ctk.set_appearance_mode("dark")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("550x950") 
        self.title("Qué veo 📺")
        # Colores Netflix: Fondo muy oscuro
        self.configure(fg_color="#0F0F0F")
        self.usuario_actual = "" 
        self.nombre_usuario = ""
        
        # Contenedor principal ahora es oscuro y elegante
        self.main_container = ctk.CTkFrame(self, fg_color="#181818", corner_radius=20, border_width=1, border_color="#2A2A2A")
        self.main_container.pack(pady=25, padx=30, fill="both", expand=True)
        self.mostrar_login()

    def limpiar_frame(self):
        for widget in self.main_container.winfo_children():
            widget.destroy()

    def abrir_enlace(self, url):
        webbrowser.open(url)

    def mostrar_progreso(self):
        self.progreso = ctk.CTkProgressBar(self.main_container, orientation="horizontal", mode="indeterminate", progress_color="#E50914")
        self.progreso.pack(pady=10, padx=20, fill="x")
        self.progreso.start()

    def ocultar_progreso(self):
        if hasattr(self, 'progreso'):
            self.progreso.stop()
            self.progreso.destroy()

    def mostrar_error_visual(self, mensaje="¡Ups! Algo salió mal"):
        self.limpiar_frame()
        error_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        error_frame.pack(expand=True)
        ctk.CTkLabel(error_frame, text="🕵️‍♂️", font=("Roboto", 70)).pack()
        ctk.CTkLabel(error_frame, text=mensaje, font=("Roboto", 18, "bold"), text_color="#FFFFFF").pack(pady=10)
        ctk.CTkButton(error_frame, text="Intentar de nuevo", fg_color="#E50914", hover_color="#B20710",
                      command=lambda: self.mostrar_experiencia_diaria(self.nombre_usuario)).pack(pady=20)

    def compartir_peli(self, peli):
        texto = f"¡Mira esta peli que encontré en 'Qué Veo'! 📺\n🎬 {peli['Title']} ({peli['Year']})\n⭐ Rating: {peli.get('imdbRating', 'N/A')}"
        pyperclip.copy(texto)
        self.mostrar_toast("¡Enlace copiado! 🚀")

    def mostrar_toast(self, mensaje):
        toast = ctk.CToplevel(self)
        toast.geometry(f"250x40+{self.winfo_x()+150}+{self.winfo_y()+850}")
        toast.overrideredirect(True)
        toast.configure(fg_color="#2F2F2F")
        ctk.CTkLabel(toast, text=mensaje, text_color="white", font=("Roboto", 12)).pack(expand=True)
        self.after(2000, toast.destroy)

    def mostrar_login(self):
        self.limpiar_frame()
        ctk.CTkLabel(self.main_container, text="Qué Veo", font=("Roboto", 45, "bold"), text_color="#E50914").pack(pady=(40, 10))
        ctk.CTkLabel(self.main_container, text="Inicia sesión para empezar 📺", font=("Roboto", 16), text_color="#AAAAAA").pack(pady=(0, 30))
        
        self.email_ent = ctk.CTkEntry(self.main_container, placeholder_text="Correo electrónico", width=320, height=45, fg_color="#333333", border_color="#444444")
        self.email_ent.pack(pady=10)

        pw_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        pw_frame.pack(pady=10)
        self.pw_ent = ctk.CTkEntry(pw_frame, placeholder_text="Contraseña", show="*", width=270, height=45, fg_color="#333333", border_color="#444444")
        self.pw_ent.pack(side="left")

        def toggle_password():
            if self.pw_ent.cget("show") == "*":
                self.pw_ent.configure(show=""); btn_reveal.configure(text="👁️")
            else:
                self.pw_ent.configure(show="*"); btn_reveal.configure(text="🙈")

        btn_reveal = ctk.CTkButton(pw_frame, text="🙈", width=40, fg_color="transparent", hover_color="#2A2A2A", command=toggle_password, font=("Roboto", 20))
        btn_reveal.pack(side="left", padx=5)

        self.error_lbl = ctk.CTkLabel(self.main_container, text="", text_color="#E50914")
        self.error_lbl.pack(pady=5)
        
        ctk.CTkButton(self.main_container, text="Iniciar Sesión", fg_color="#E50914", hover_color="#B20710", text_color="white", font=("Roboto", 16, "bold"), command=self.logic_login, width=320, height=45).pack(pady=20)
        ctk.CTkButton(self.main_container, text="¿Nuevo aquí? Crea una cuenta", fg_color="transparent", text_color="#FFFFFF", hover_color="#2A2A2A", command=self.mostrar_registro).pack()

    def mostrar_experiencia_diaria(self, nombre):
        self.limpiar_frame()
        self.nombre_usuario = nombre
        perfil = obtener_perfil(self.usuario_actual)

        # Header elegante
        menu_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        menu_frame.pack(fill="x", padx=25, pady=20)
        ctk.CTkLabel(menu_frame, text=f"Hola, {nombre} 🍿", font=("Roboto", 22, "bold"), text_color="#FFFFFF").pack(side="left")
        ctk.CTkButton(menu_frame, text="👤", width=40, height=40, fg_color="#333333", hover_color="#444444", corner_radius=20, command=self.abrir_perfil).pack(side="right")

        # Lógica de Cumpleaños
        if perfil and perfil.get("fecha_nacimiento"):
            try:
                hoy = datetime.now()
                fecha_n_str = perfil["fecha_nacimiento"]
                fecha_n = datetime.strptime(fecha_n_str, "%d/%m/%Y")
                if hoy.day == fecha_n.day and hoy.month == fecha_n.month:
                    frases = [
                        "¡Feliz cumpleaños! 'Hakuna Matata, vive y sé feliz.' 🦁",
                        "¡Felicidades! 'Que la fuerza te acompañe' en tu nuevo año. ✨",
                        "¡Feliz cumple! 'La vida es como una caja de bombones...' 🍫",
                        "¡Felicidades! 'Hasta el infinito y más allá.' 🚀"
                    ]
                    bday_frame = ctk.CTkFrame(self.main_container, fg_color="#E50914", corner_radius=10)
                    bday_frame.pack(fill="x", padx=25, pady=(0, 10))
                    ctk.CTkLabel(bday_frame, text=random.choice(frases), font=("Roboto", 13, "bold"), text_color="white").pack(pady=10)
            except: pass

        # Botón Ruleta Estilo "Premium"
        ctk.CTkButton(self.main_container, text="🎰 Ruleta de la Suerte", fg_color="#E50914", hover_color="#B20710", text_color="white", font=("Roboto", 14, "bold"), height=40, command=self.ejecutar_ruleta).pack(pady=10, padx=30, fill="x")

        # Recomendación personalizada
        if perfil and perfil.get("cine_favorito"):
            rec_frame = ctk.CTkFrame(self.main_container, fg_color="#222", corner_radius=10)
            rec_frame.pack(fill="x", padx=25, pady=10)
            ctk.CTkLabel(rec_frame, text=f"Para ti: {perfil['cine_favorito'][0]}", font=("Roboto", 12, "italic"), text_color="#AAA").pack(pady=(5,0))
            ctk.CTkButton(rec_frame, text="✨ Ver recomendaciones", fg_color="transparent", text_color="#E50914", hover_color="#333", command=lambda: self.ejecutar_recomendacion(perfil['cine_favorito'])).pack()

        # Barra de búsqueda Pro
        search_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        search_frame.pack(pady=10, padx=25, fill="x")
        self.busqueda_ent = ctk.CTkEntry(search_frame, placeholder_text="Películas, series, actores...", width=200, height=40, fg_color="#333333", border_color="#444444")
        self.busqueda_ent.pack(side="left", fill="x", expand=True, padx=(0,10))
        ctk.CTkButton(search_frame, text="🔍", width=50, height=40, fg_color="#E50914", command=self.ejecutar_busqueda_directa).pack(side="right")

        # Opciones de Filtros
        filtros_frame = ctk.CTkScrollableFrame(self.main_container, height=280, fg_color="transparent")
        filtros_frame.pack(fill="both", expand=True, padx=20)

        ctk.CTkLabel(filtros_frame, text="¿Cómo está tu ánimo hoy?", font=("Roboto", 14, "bold"), text_color="#EEE").pack(pady=(10,5))
        self.animo_opc = ctk.CTkOptionMenu(filtros_frame, values=["Normal 😐", "Feliz 😊", "Triste 😢", "Con Adrenalina ⚡", "Romántico ❤️", "Asustado 😱"], 
                                         fg_color="#333", button_color="#444", width=280)
        self.animo_opc.pack(pady=5)

        self.tipo_opc = ctk.CTkOptionMenu(filtros_frame, values=["Quiero ver una Película 🎬", "Quiero ver una Serie 📺"], fg_color="#333", button_color="#444", width=280)
        self.tipo_opc.pack(pady=5)
        
        self.year_opc = ctk.CTkOptionMenu(filtros_frame, values=["Todos los años", "Estrenos (2020-2025)", "2015-2020", "Clásicos", "Ingresar año manualmente"], fg_color="#333", button_color="#444", width=280, command=self.toggle_año_manual)
        self.year_opc.pack(pady=5)
        self.año_manual_ent = ctk.CTkEntry(filtros_frame, placeholder_text="Ej: 1994", fg_color="#333", width=280)

        # Géneros en Grid
        ctk.CTkLabel(filtros_frame, text="Géneros preferidos", font=("Roboto", 14, "bold"), text_color="#EEE").pack(pady=(10,5))
        self.check_vars = {}
        grid_g = ctk.CTkFrame(filtros_frame, fg_color="transparent")
        grid_g.pack()
        gens = ["Acción", "Comedia", "Drama", "Terror", "Sci-Fi", "Romance"]
        for i, g in enumerate(gens):
            var = ctk.StringVar(value="off")
            cb = ctk.CTkCheckBox(grid_g, text=g, variable=var, onvalue=g, offvalue="off", text_color="#FFFFFF", border_color="#E50914", checkmark_color="#E50914")
            cb.grid(row=i//2, column=i%2, padx=15, pady=5, sticky="w")
            self.check_vars[g] = var

        ctk.CTkButton(self.main_container, text="Dime qué ver ✨", fg_color="#E50914", text_color="white", font=("Roboto", 16, "bold"), height=50, command=self.ejecutar_recomendacion).pack(pady=20, padx=30, fill="x")
        ctk.CTkButton(self.main_container, text="Cerrar Sesión", fg_color="transparent", text_color="#666", command=self.cerrar_sesion).pack(pady=(0, 10))

    def mostrar_resultados(self, lista):
        self.limpiar_frame()
        scroll = ctk.CTkScrollableFrame(self.main_container, fg_color="transparent", height=750)
        scroll.pack(fill="both", expand=True, padx=15, pady=15)
        
        perfil = obtener_perfil(self.usuario_actual)
        comentarios = perfil.get("comentarios", {}) if perfil else {}

        for peli in lista:
            card = ctk.CTkFrame(scroll, fg_color="#222", corner_radius=15, border_width=1, border_color="#333")
            card.pack(pady=15, fill="x")

            info_row = ctk.CTkFrame(card, fg_color="transparent")
            info_row.pack(fill="x", padx=10, pady=10)

            if peli.get("Poster") != "N/A":
                try:
                    res_img = requests.get(peli["Poster"], timeout=5)
                    ctk_img = ctk.CTkImage(Image.open(BytesIO(res_img.content)), size=(120, 180))
                    ctk.CTkLabel(info_row, image=ctk_img, text="").pack(side="left", padx=5)
                except: pass
            
            detalles = ctk.CTkFrame(info_row, fg_color="transparent")
            detalles.pack(side="left", fill="both", expand=True, padx=10)
            
            ctk.CTkLabel(detalles, text=peli["Title"], font=("Roboto", 18, "bold"), text_color="#FFFFFF", wraplength=200, justify="left").pack(anchor="w")
            ctk.CTkLabel(detalles, text=f"📅 {peli['Year']}  ⭐ {peli.get('imdbRating', 'N/A')}", font=("Roboto", 12), text_color="#E50914").pack(anchor="w")
            
            actions = ctk.CTkFrame(detalles, fg_color="transparent")
            actions.pack(anchor="w", pady=10)
            ctk.CTkButton(actions, text="❤️", width=35, fg_color="#333", command=lambda p=peli: self.logic_favoritos(p)).pack(side="left", padx=2)
            ctk.CTkButton(actions, text="🔖", width=35, fg_color="#333", command=lambda p=peli: self.logic_watchlist(p)).pack(side="left", padx=2)
            ctk.CTkButton(actions, text="🚀", width=35, fg_color="#333", command=lambda p=peli: self.compartir_peli(p)).pack(side="left", padx=2)

            ctk.CTkLabel(card, text=peli.get("Plot", "Sin sinopsis."), font=("Roboto", 11), text_color="#BBB", wraplength=450, justify="left").pack(pady=5, padx=15)

            stars_f = ctk.CTkFrame(card, fg_color="transparent")
            stars_f.pack(pady=5)
            for i in range(1, 6):
                ctk.CTkButton(stars_f, text="⭐", width=30, fg_color="transparent", hover_color="#333", text_color="#666", command=lambda r=i, p=peli: self.guardar_rating(p, r)).pack(side="left")

            enlaces_frame = ctk.CTkFrame(card, fg_color="transparent")
            enlaces_frame.pack(pady=10, padx=20, fill="x")
            
            ctk.CTkButton(enlaces_frame, text="▶ Ver Tráiler", 
                          command=lambda u=peli.get("trailer") or f"https://www.youtube.com/results?search_query={peli['Title']}+trailer": self.abrir_enlace(u), 
                          fg_color="#FFFFFF", text_color="#000000", font=("Roboto", 13, "bold"), hover_color="#DDD", width=180).pack(side="left", padx=5, expand=True)

            ctk.CTkButton(enlaces_frame, text="🔍 Dónde Ver", 
                          command=lambda t=peli['Title']: self.abrir_enlace(obtener_donde_ver(t)), 
                          fg_color="#E50914", text_color="#FFFFFF", font=("Roboto", 13, "bold"), hover_color="#B20710", width=180).pack(side="left", padx=5, expand=True)

            nota_actual = comentarios.get(peli["imdbID"], "")
            entry_coment = ctk.CTkEntry(card, placeholder_text="Añadir nota personal...", height=30, fg_color="#111", border_color="#333")
            entry_coment.pack(pady=(5, 5), padx=20, fill="x")
            entry_coment.insert(0, nota_actual)
            
            def save_n(p=peli, e=entry_coment):
                guardar_comentario(self.usuario_actual, p["imdbID"], e.get())
                self.mostrar_toast("¡Nota guardada! ✍️")
            ctk.CTkButton(card, text="Guardar Nota", height=20, fg_color="transparent", text_color="#AAA", command=save_n).pack(pady=(0, 10))

        ctk.CTkButton(self.main_container, text="⬅ Volver al inicio", fg_color="#333", hover_color="#444", width=280, command=lambda: self.mostrar_experiencia_diaria(self.nombre_usuario)).pack(pady=15)

    def ejecutar_ruleta(self):
        perfil = obtener_perfil(self.usuario_actual)
        generos_base = perfil.get("cine_favorito", ["Acción", "Comedia"]) if perfil else ["Acción"]
        self.mostrar_progreso()
        def tarea():
            try:
                exito, resultados = buscar_recomendaciones(generos_base, "Todos los años", "", "Quiero ver una Película 🎬")
                self.after(0, self.ocultar_progreso)
                if exito and resultados:
                    peli_random = random.choice(resultados)
                    self.after(0, lambda: self.mostrar_resultados([peli_random]))
                else: self.after(0, lambda: self.mostrar_error_visual())
            except: 
                self.after(0, self.ocultar_progreso); self.after(0, lambda: self.mostrar_error_visual())
        threading.Thread(target=tarea).start()

    def abrir_perfil(self):
        self.limpiar_frame()
        perfil = obtener_perfil(self.usuario_actual)
        ctk.CTkLabel(self.main_container, text="Mi Perfil", font=("Roboto", 30, "bold"), text_color="#E50914").pack(pady=25)
        
        # Medallas / Logros
        logros = calcular_logros(self.usuario_actual)
        if logros:
            # TITULO DE LOGROS ACTUALIZADO
            ctk.CTkLabel(self.main_container, text="¡En hora buena! Estos son tus logros, lo sabemos, también amamos el cine.🥳", 
                        font=("Roboto", 12, "italic"), text_color="#AAA", wraplength=400).pack(pady=(0, 5))
            
            l_frame = ctk.CTkScrollableFrame(self.main_container, height=70, orientation="horizontal", fg_color="#222", corner_radius=15)
            l_frame.pack(fill="x", padx=30, pady=10)
            for log in logros:
                ctk.CTkLabel(l_frame, text=f" {log} ", fg_color="#E50914", text_color="white", corner_radius=10, font=("Roboto", 12, "bold")).pack(side="left", padx=5)

        info_card = ctk.CTkFrame(self.main_container, fg_color="#222", corner_radius=15)
        info_card.pack(pady=10, padx=30, fill="x")
        ctk.CTkLabel(info_card, text=perfil.get('nombre', 'Usuario'), font=("Roboto", 20, "bold")).pack(pady=5)
        
        # Cálculo de Edad
        edad_texto = "Edad: Desconocida"
        if perfil and perfil.get("fecha_nacimiento"):
            try:
                fecha_n = datetime.strptime(perfil["fecha_nacimiento"], "%d/%m/%Y")
                hoy = datetime.now()
                edad = hoy.year - fecha_n.year - ((hoy.month, hoy.day) < (fecha_n.month, fecha_n.day))
                edad_texto = f"Edad: {edad} años"
            except: pass
        
        ctk.CTkLabel(info_card, text=edad_texto, font=("Roboto", 14), text_color="#CCC").pack()
        ctk.CTkLabel(info_card, text=self.usuario_actual, text_color="#888").pack(pady=(0,10))
        
        ctk.CTkButton(self.main_container, text="Editar Datos", fg_color="#333", command=self.mostrar_datos_personales).pack(pady=10)
        
        # Listas en el perfil
        listas_scroll = ctk.CTkScrollableFrame(self.main_container, height=350, fg_color="transparent")
        listas_scroll.pack(fill="both", expand=True, padx=20)

        ctk.CTkLabel(listas_scroll, text="🔖 Mi Watchlist", font=("Roboto", 16, "bold"), text_color="#E50914").pack(pady=10, anchor="w")
        for w in obtener_watchlist(self.usuario_actual):
            ctk.CTkButton(listas_scroll, text=f"• {w['Title']}", anchor="w", fg_color="transparent", hover_color="#222", command=lambda p=w: self.mostrar_resultados([p])).pack(fill="x")

        ctk.CTkLabel(listas_scroll, text="❤️ Mis Favoritos", font=("Roboto", 16, "bold"), text_color="#E50914").pack(pady=10, anchor="w")
        for f in obtener_favoritos(self.usuario_actual):
            ctk.CTkButton(listas_scroll, text=f"• {f['Title']} ({f.get('mi_puntuacion', '?')}⭐)", anchor="w", fg_color="transparent", hover_color="#222", command=lambda p=f: self.mostrar_resultados([p])).pack(fill="x")
        
        # HISTORIAL DE BÚSQUEDA
        ctk.CTkLabel(listas_scroll, text="🕒 Historial de Búsqueda", font=("Roboto", 16, "bold"), text_color="#E50914").pack(pady=(20, 5), anchor="w")
        historial = perfil.get("historial", []) if perfil else []
        if historial:
            for item in reversed(historial[-10:]):
                ctk.CTkButton(listas_scroll, text=f"🔍 {item}", anchor="w", fg_color="transparent", hover_color="#222", 
                              text_color="#AAA", command=lambda x=item: self.ejecutar_busqueda_rapida(x)).pack(fill="x")
        else:
            ctk.CTkLabel(listas_scroll, text="Historial vacío.", font=("Roboto", 12), text_color="#666").pack(anchor="w", padx=10)

        ctk.CTkButton(self.main_container, text="⬅ Volver", fg_color="#E50914", width=280, command=lambda: self.mostrar_experiencia_diaria(self.nombre_usuario)).pack(pady=20)

    def guardar_rating(self, peli, rating):
        peli["mi_puntuacion"] = rating
        self.logic_favoritos(peli)
        self.mostrar_toast(f"¡Le diste {rating} estrellas! ⭐")

    def ejecutar_recomendacion(self, generos_predef=None):
        self.mostrar_progreso()
        mapeo_animo = {
            "Feliz 😊": ["Comedia", "Romance"], "Triste 😢": ["Drama"],
            "Con Adrenalina ⚡": ["Acción", "Sci-Fi"], "Romántico ❤️": ["Romance", "Drama"], "Asustado 😱": ["Terror"]
        }
        def tarea():
            try:
                g_sel = generos_predef if generos_predef else [v.get() for v in self.check_vars.values() if v.get() != "off"]
                animo = self.animo_opc.get()
                if animo in mapeo_animo: g_sel.extend(mapeo_animo[animo])
                g_sel = list(set(g_sel))
                exito, resultados = buscar_recomendaciones(g_sel, self.year_opc.get(), self.año_manual_ent.get(), self.tipo_opc.get())
                self.after(0, self.ocultar_progreso)
                if exito and resultados: self.after(0, lambda: self.mostrar_resultados(resultados))
                else: self.after(0, lambda: self.mostrar_error_visual("Sin resultados"))
            except: self.after(0, self.ocultar_progreso); self.after(0, lambda: self.mostrar_error_visual("Error de conexión"))
        threading.Thread(target=tarea).start()

    def ejecutar_busqueda_directa(self):
        t = self.busqueda_ent.get()
        if t:
            agregar_al_historial(self.usuario_actual, t) 
            self.mostrar_progreso()
            def tarea():
                try:
                    exito, res = buscar_pelicula_especifica(t)
                    self.after(0, self.ocultar_progreso)
                    if exito: self.after(0, lambda: self.mostrar_resultados([res]))
                    else: self.after(0, lambda: self.mostrar_error_visual(f"No encontramos '{t}'"))
                except: self.after(0, self.ocultar_progreso); self.after(0, lambda: self.mostrar_error_visual("Error"))
            threading.Thread(target=tarea).start()

    def ejecutar_busqueda_rapida(self, texto):
        self.busqueda_ent.delete(0, 'end'); self.busqueda_ent.insert(0, texto); self.ejecutar_busqueda_directa()

    def logic_favoritos(self, peli_datos):
        exito, msg = agregar_a_favoritos(self.usuario_actual, peli_datos); self.mostrar_toast(msg)

    def logic_watchlist(self, peli_datos):
        exito, msg = agregar_a_watchlist(self.usuario_actual, peli_datos); self.mostrar_toast(msg)

    def logic_login(self):
        email, pw = self.email_ent.get(), self.pw_ent.get()
        exito, msg = verificar_login(email, pw)
        if exito:
            self.usuario_actual = email; p = obtener_perfil(email)
            if p and p.get("nombre"): self.mostrar_experiencia_diaria(p["nombre"])
            else: self.mostrar_datos_personales()
        else: self.error_lbl.configure(text=msg)

    def mostrar_registro(self):
        self.limpiar_frame()
        ctk.CTkLabel(self.main_container, text="Únete a Qué Veo", font=("Roboto", 28, "bold"), text_color="#E50914").pack(pady=30)
        self.email_ent = ctk.CTkEntry(self.main_container, placeholder_text="Correo electrónico", width=300, height=40, fg_color="#333")
        self.email_ent.pack(pady=10)
        self.pw_ent = ctk.CTkEntry(self.main_container, placeholder_text="Contraseña", show="*", width=300, height=40, fg_color="#333")
        self.pw_ent.pack(pady=10)
        self.pw_conf_ent = ctk.CTkEntry(self.main_container, placeholder_text="Confirmar Contraseña", show="*", width=300, height=40, fg_color="#333")
        self.pw_conf_ent.pack(pady=10)
        self.error_lbl = ctk.CTkLabel(self.main_container, text="", text_color="#E50914"); self.error_lbl.pack(pady=5)
        ctk.CTkButton(self.main_container, text="Registrarse", fg_color="#E50914", hover_color="#B20710", command=self.logic_registro, width=300, height=45).pack(pady=20)
        ctk.CTkButton(self.main_container, text="Volver al Login", fg_color="transparent", text_color="#AAA", command=self.mostrar_login).pack()

    def mostrar_datos_personales(self):
        self.limpiar_frame()
        perfil = obtener_perfil(self.usuario_actual)
        nombre_actual = perfil.get('nombre', 'Usuario') if perfil else 'Usuario'
        
        # TITULO ACTUALIZADO
        texto_titulo = f"Hola, {nombre_actual}\n¿Qué te gustaría cambiar en tu perfil?"
        ctk.CTkLabel(self.main_container, text=texto_titulo, font=("Roboto", 20, "bold"), text_color="#E50914", justify="center").pack(pady=20)
        
        self.nombre_ent = ctk.CTkEntry(self.main_container, placeholder_text="Tu nombre", width=300, height=40, fg_color="#333")
        self.nombre_ent.pack(pady=10)
        if perfil: self.nombre_ent.insert(0, nombre_actual)
        
        frame_fecha = ctk.CTkFrame(self.main_container, fg_color="transparent"); frame_fecha.pack(pady=10)
        self.dia_opc = ctk.CTkOptionMenu(frame_fecha, values=[f"{d:02d}" for d in range(1, 32)], width=70, fg_color="#333"); self.dia_opc.pack(side="left", padx=2)
        self.meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
        self.mes_opc = ctk.CTkOptionMenu(frame_fecha, values=self.meses, width=110, fg_color="#333"); self.mes_opc.pack(side="left", padx=2)
        self.año_opc = ctk.CTkOptionMenu(frame_fecha, values=[str(y) for y in range(2025, 1950, -1)], width=90, fg_color="#333"); self.año_opc.pack(side="left", padx=2)
        
        self.genero_opc = ctk.CTkOptionMenu(self.main_container, values=["Masculino", "Femenino", "Otro"], width=300, fg_color="#333"); self.genero_opc.pack(pady=10)
        
        grid = ctk.CTkFrame(self.main_container, fg_color="transparent"); grid.pack(pady=10)
        self.generos_pref = {}
        for i, g in enumerate(["Acción", "Comedia", "Drama", "Terror", "Sci-Fi", "Romance"]):
            var = ctk.StringVar(value="off")
            ctk.CTkCheckBox(grid, text=g, variable=var, onvalue=g, offvalue="off", text_color="white", border_color="#E50914").grid(row=i//2, column=i%2, padx=10, pady=5)
            self.generos_pref[g] = var
            
        ctk.CTkButton(self.main_container, text="Guardar Perfil", fg_color="#E50914", text_color="white", font=("Roboto", 14, "bold"), command=self.guardar_datos_personales, width=300, height=45).pack(pady=(25, 5))
        
        # BOTÓN CANCELAR AGREGADO
        ctk.CTkButton(self.main_container, text="Cancelar", fg_color="#333", text_color="white", width=300, height=40, 
                     command=lambda: self.mostrar_experiencia_diaria(self.nombre_usuario)).pack(pady=5)

    def guardar_datos_personales(self):
        nombre = self.nombre_ent.get().strip()
        mes_num = f"{self.meses.index(self.mes_opc.get()) + 1:02d}"
        fecha = f"{self.dia_opc.get()}/{mes_num}/{self.año_opc.get()}"
        cine_favorito = [v.get() for v in self.generos_pref.values() if v.get() != "off"]
        if not nombre: return
        guardar_perfil(self.usuario_actual, {"nombre": nombre, "fecha_nacimiento": fecha, "genero": self.genero_opc.get(), "cine_favorito": cine_favorito})
        self.mostrar_experiencia_diaria(nombre)

    def cerrar_sesion(self): self.mostrar_login()
    def toggle_año_manual(self, seleccion):
        if seleccion == "Ingresar año manualmente": self.año_manual_ent.pack(pady=5)
        else: self.año_manual_ent.pack_forget()
    def logic_registro(self):
        e, p, c = self.email_ent.get(), self.pw_ent.get(), self.pw_conf_ent.get()
        valido, msg = validar_password(p, c)
        if valido:
            exito, msg = registrar_usuario(e, p)
            if exito: self.mostrar_login()
            else: self.error_lbl.configure(text=msg)
        else: self.error_lbl.configure(text=msg)

if __name__ == "__main__":
    app = App()
    app.mainloop()