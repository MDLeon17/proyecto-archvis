# Sistema de Perfil y Configuración de Pantalla con PyQt6

Aplicación de escritorio desarrollada en Python y PyQt6 enfocada en la **personalización completa de la interfaz gráfica** y la **gestión del perfil de usuario**, con arquitectura de persistencia segura mediante **escritura atómica** y **respaldos automáticos (.bak)** en formato **JSON** (UTF-8).

---

## Características Principales

1. **Navegación Simplificada (Sidebar Lateral)**:
   - Panel lateral moderno con tarjeta de perfil (avatar circular con soporte de foto o iniciales con color personalizado, nombre de usuario y etiqueta de rol).
   - Únicamente dos módulos de navegación:
     - **Perfil (Profile)**: Vista de la identidad del usuario y exposición visual de todas las personalizaciones aplicadas.
     - **Configuración (Settings)**: Panel integral para modificar la apariencia de la pantalla, tema, colores, tipografía, idioma y foto de perfil.

2. **Módulo de Perfil (Profile View)**:
   - **Tarjeta de Identidad**: Avatar de alta resolución, nombre, rol/puesto, biografía descriptiva y botón de acceso rápido para modificar ajustes.
   - **Resumen de Personalización Activa**: Muestra en tiempo real el modo de pantalla activo (Claro/Oscuro), idioma del sistema, tamaño de tipografía y muestras de color (Color de botones, color de barra de menú y color de letra).
   - **Laboratorio de Componentes en Vivo**: Previsualización interactiva de botones primarios, secundarios, insignias y textos con los estilos aplicados dinámicamente.

3. **Módulo de Configuración (Settings View)**:
   - **Datos de Usuario**: Modificación de nombre, rol y biografía.
   - **Tema de Pantalla**: Selección entre **Modo Oscuro (Dark Mode)** y **Modo Claro (Light Mode)**.
   - **Idioma del Sistema**: Soporte bilingüe en tiempo real para **Español** e **Inglés**.
   - **Tamaño de Fuente**: Selector numérico de puntos tipográficos (pt).
   - **Color de Botones**: Selector nativo `QColorDialog` para personalizar el color principal de los botones del sistema con cálculo automático de contraste y estados *hover* / *pressed*.
   - **Color de Barra de Menú / Lateral**: Selector nativo `QColorDialog` para el fondo del panel lateral.
   - **Color de Letra / Tipografía**: Selector nativo `QColorDialog` con validación de legibilidad según el modo claro u oscuro.
   - **Foto de Perfil**: Selector de imágenes del sistema (`QFileDialog`) con recorte circular suave y botón para remover fotografía.
   - **Mecanismos de Respaldo**: Guardado atómico en `config.json`, restauración instantánea desde `config.bak` y restablecimiento a valores por defecto.

---

## Arquitectura de Seguridad y Persistencia de Archivos

- **Carga Inicial a Prueba de Fallos**: Lectura robusta de `config.json`. Si no existe o se encuentra dañado, se degrada limpiamente a valores por defecto o se recupera desde `config.bak`.
- **Escritura Segura (Atomic Write)**: El guardado se realiza primero en un archivo temporal (`config.tmp`), se fuerza la escritura física en disco mediante `flush()` y `os.fsync()`, y finalmente se reemplaza atómicamente con `os.replace()`.
- **Respaldo Previo (.bak)**: Antes de sobrescribir `config.json`, se genera automáticamente una copia fiel en `config.bak`.
- **Codificación Explícita UTF-8**: Todas las operaciones de entrada/salida garantizan soporte integral para caracteres especiales, acentos y signos ortográficos internacionales.
- **Captura Global de Excepciones**: Hook centralizado (`sys.excepthook`) con ventana emergente de aviso para evitar caídas imprevistas de la aplicación.

---

## Estructura del Proyecto

```text
proyecto archvis/
├── core/
│   ├── __init__.py
│   ├── i18n.py               # Motor de internacionalización bilingüe (Español / Inglés)
│   └── config_manager.py     # Gestor de configuración con atomic write y .bak
├── ui/
│   ├── __init__.py
│   ├── style.py              # Generador dinámico de temas QSS (Colores, botones, contraste)
│   ├── sidebar.py            # Barra lateral con perfil, avatar y navegación (Perfil / Settings)
│   ├── main_window.py        # Ventana principal y sincronización dinámica
│   └── views/
│       ├── __init__.py
│       ├── profile_view.py   # Vista de Perfil y muestra de personalización activa
│       └── settings_view.py  # Vista de Configuración visual y preferencias
├── assets/                   # Recursos visuales (avatar por defecto)
├── config.json               # Archivo de configuración activo (UTF-8)
├── config.bak                # Copia previa de respaldo de configuración
├── main.py                   # Punto de entrada principal con capturador de excepciones
├── requirements.txt          # Dependencias del proyecto (PyQt6)
└── README.md                 # Documentación del sistema
```

---

## Instalación y Ejecución

1. **Requisitos**: Python 3.10 o superior (compatible con Python 3.14).
2. **Instalación de dependencias**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Iniciar la Aplicación**:
   ```bash
   python main.py
   ```
