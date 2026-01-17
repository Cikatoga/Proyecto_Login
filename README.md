# 🎬 Qué Veo - Sistema de Recomendación de Películas y Series

Una aplicación de escritorio moderna construida con Python que te ayuda a descubrir películas y series según tu estado de ánimo, preferencias y géneros favoritos. Con autenticación de usuarios, perfiles personalizados y un motor de recomendaciones inteligente.

## 🎯 Características Principales

### 🔐 Sistema de Autenticación
- Registro seguro de nuevos usuarios con validación de contraseñas
- Login con verificación de credenciales
- Perfiles personalizados por usuario
- Almacenamiento seguro de datos en JSON

### 📺 Motor de Recomendaciones
- Búsqueda de películas y series por género
- Filtrado por año de estreno
- Recomendaciones personalizadas según tu estado de ánimo
- "Ruleta de la Suerte" para sorpresas aleatorias
- Búsqueda directa de películas y actores

### 🎨 Interfaz de Usuario
- Diseño moderno con tema Netflix (oscuro)
- Interfaz intuitiva construida con CustomTkinter
- Soporte para imágenes de pósters
- Animaciones y notificaciones visuales (toasts)

### ❤️ Gestión de Listas
- **Favoritos**: Guarda hasta 10 películas favoritas con puntuación personal
- **Watchlist**: Lista de películas para ver después
- **Historial**: Registro de búsquedas recientes
- **Notas Personales**: Añade comentarios a cada película

### 🎥 Información de Películas
- Detalles completos (sinopsis, año, calificación IMDb)
- Enlaces directos a tráilers de YouTube
- Información de dónde ver (plataformas de streaming)
- Compatibilidad con múltiples plataformas (Netflix, Prime Video, Disney+, HBO Max)

### 🏆 Sistema de Logros
- Medallas según tu actividad y preferencias
- Motivación gamificada para explorar más contenido
- Felicitaciones en tu cumpleaños

### 📅 Funcionalidades Especiales
- Cálculo automático de edad
- Detección de cumpleaños
- Valoración de películas con sistema de estrellas
- Compartir películas (copiar información al portapapeles)

## 📋 Requisitos

### Dependencias Python
```
customtkinter>=5.0
pillow>=9.0
requests>=2.28
beautifulsoup4>=4.11
selenium>=4.0
pyperclip>=1.8
```

### Requisitos del Sistema
- Python 3.8 o superior
- ChromeDriver (para web scraping de tráilers)
- Conexión a Internet

## 🚀 Instalación

1. **Clonar el repositorio**
   ```bash
   git clone https://github.com/tuusuario/Proyecto_Login.git
   cd Proyecto_Login
   ```

2. **Crear entorno virtual** (recomendado)
   ```bash
   python -m venv venv
   venv\Scripts\activate  # En Windows
   # o source venv/bin/activate en macOS/Linux
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **Descargar ChromeDriver**
   - Descarga desde https://chromedriver.chromium.org/
   - Coloca en el directorio del proyecto o en tu PATH

## 🎮 Uso

### Ejecutar la aplicación
```bash
python main.py
```

### Primeros Pasos
1. **Registrarse**: Crea una nueva cuenta con un email y contraseña
2. **Completar Perfil**: Agrega tu nombre, fecha de nacimiento y géneros preferidos
3. **Explorar**: 
   - Usa los filtros para encontrar películas
   - Selecciona tu estado de ánimo para recomendaciones personalizadas
   - Prueba la "Ruleta de la Suerte" para sorpresas

## 📁 Estructura del Proyecto

```
Proyecto_Login/
│
├── main.py                 # Interfaz gráfica principal (CustomTkinter)
├── auth_logic.py          # Lógica de autenticación y gestión de perfiles
├── api_logic.py           # Integración con API OMDB
├── scraping_logic.py      # Web scraping para trailers y plataformas
│
├── usuarios.json          # Base de datos de usuarios
├── perfiles.json          # Perfiles personalizados de usuarios
│
├── README.md              # Este archivo
└── __pycache__/           # Archivos compilados de Python
```

## 🔧 Detalles Técnicos

### Módulos Principales

#### `main.py`
- **App (clase principal)**: Maneja toda la interfaz gráfica
- Gestiona navegación entre pantallas
- Controla eventos de usuario
- Maneja threading para no bloquear la UI

#### `auth_logic.py`
- Funciones de validación de contraseñas
- Registro e login de usuarios
- Gestión de perfiles
- CRUD de favoritos, watchlist e historial

#### `api_logic.py`
- Integración con OMDB API
- Búsqueda de películas específicas
- Búsqueda de recomendaciones según filtros
- Combinación de datos de API con scraping

#### `scraping_logic.py`
- Web scraping en JustWatch para plataformas de streaming
- Búsqueda de tráilers en YouTube
- Manejo de errores y timeouts

### Base de Datos
- **usuarios.json**: Almacena credenciales de login
- **perfiles.json**: Almacena información personal, favoritos, watchlist e historial

## 🔑 Configuración

### API Key OMDB
La aplicación usa la OMDB API para obtener información de películas. Reemplaza la API_KEY en `api_logic.py`:

```python
API_KEY = "tu_clave_aqui"  # Obtén una en https://www.omdbapi.com/apikey.aspx
```

## 🎨 Tema y Personalización

El diseño usa los colores de Netflix:
- **Primary**: #E50914 (Rojo Netflix)
- **Background**: #0F0F0F (Negro profundo)
- **Secondary**: #181818 y #222 (Grises oscuros)

Puedes personalizar estos colores modificando los valores `fg_color` en las llamadas de CustomTkinter.

## 🐛 Solución de Problemas

### "No encontrada" en búsquedas
- Verifica tu conexión a Internet
- Comprueba que la API key sea válida
- Intenta con un título más exacto

### Tráilers no se cargan
- Asegúrate de tener ChromeDriver en tu PATH
- Verifica que YouTube sea accesible en tu región

### Las imágenes de pósters no se muestran
- Algunos títulos pueden no tener póster disponible
- Verifica tu conexión a Internet

## 📝 Notas Importantes

- Las contraseñas se validan pero no se encriptan (proyecto educativo)
- Para producción, implementar encriptación de contraseñas
- El web scraping puede cambiar si los sitios modifican su estructura
- Respetar los términos de servicio de OMDB, JustWatch y YouTube

## 👥 Contribuciones

Las contribuciones son bienvenidas. Por favor:
1. Fork el proyecto
2. Crea una rama (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 💡 Futuras Mejoras

- [ ] Encriptación de contraseñas con bcrypt
- [ ] Sincronización en la nube
- [ ] App móvil con Flutter
- [ ] Integración con más APIs (TMDB, etc.)
- [ ] Sistema de comentarios y reviews
- [ ] Recomendaciones colaborativas
- [ ] Soporte para múltiples idiomas
- [ ] Tema claro opcional

## 📞 Contacto

Para preguntas o sugerencias, abre un issue en GitHub.

---

**Desarrollado con ❤️ usando Python y CustomTkinter**
