# Sistema de Archivos CSV y Control de Horarios con PyQt6

Aplicación de escritorio desarrollada en Python y PyQt6 para el control integral de jornada laboral, estados de colaborador y gestión segura de persistencia en archivos **CSV** y **JSON**, incorporando arquitectura a prueba de fallos mediante **escritura atómica** y **respaldos automáticos (.bak)**.

---

##  Características Principales

1. **Gestión de Tiempos y Logins (Clock In/Out)**:
   - Marcado de entrada (*Clock In*) y salida (*Clock Out*).
   - Cambio de estados operativos en tiempo real:
     - `Ready` (En Puesto)
     - `Lunch` (Almuerzo)
     - `Break` (Descanso)
     - `Meeting` (Reunión)
     - `Training` (Capacitación)
   - Cronómetro activo con acumulador de tiempo por estado y guardado automático en CSV al conmutar de estado.

2. **Navegación por Sidebar (Barra Lateral)**:
   - Panel lateral moderno con tarjeta de perfil (foto de avatar, nombre de usuario y etiqueta de estado en vivo).
   - Conmutador entre 7 vistas especializadas.

3. **Vistas Requeridas del Sistema**:
   -  **Control de Tiempo**: Marcación de turnos y estados en vivo.
   -  **Consultar / Leer Registros**: Explorador completo del archivo CSV, búsqueda predictiva, filtros por estado y fecha, estadísticas de horas totales y diálogo modal de detalle de cada registro.
   -  **Agregar Registro**: Formulario de registro manual de horas con cálculo automático de duración.
   -  **Edición de un Dato en Concreto**: Permite modificar cualquier campo de un registro existente, especialmente estados mal marcados (ej. corregir 3 horas de `Lunch` por error a 3 horas de `Ready`) y recalcular las horas trabajadas.
   -  **Eliminación de un Dato**: Tabla de selección con **ventana emergente (pop-up) de advertencia estricta**: *"Si elimina este registro de tiempo, ese tiempo se le descontará de su jornada laboral"*, respaldando el archivo antes de proceder.
   -  **Configuración (Settings)**:
     - Nombre de usuario.
     - Tema de la interfaz (`Claro` / `Oscuro`).
     - Idioma (`Español es/es-ES` / `English en/en-US`).
     - Tamaño de fuente (entero en puntos tipográficos).
     - Color de la barra de menú/lateral mediante selector nativo `QColorDialog`.
     - Color de letra general mediante selector nativo `QColorDialog`.
     - Foto de perfil mediante selector del sistema de archivos `QFileDialog` con previsualización en miniatura.
   -  **Gestión de Copias de Seguridad (.bak)**: Panel para inspeccionar y restaurar copias de respaldo tanto del archivo CSV de registros como de la configuración.

---

##  Arquitectura de Seguridad y Persistencia de Archivos

El sistema implementa rigurosamente los estándares de persistencia segura:

- **Carga Inicial a Prueba de Fallos**: Al iniciar, lee la configuración desde `config.json` o el archivo de registros `registros.csv`. Si alguno no existe, se aplican valores por defecto sin emitir excepciones no controladas.
- **Escritura Segura (Atomic Write)**: Ninguna operación escribe directamente sobre el archivo final. Los datos se escriben en un archivo temporal (`config.tmp` / `registros.tmp`), se vacía el búfer a disco con `flush()` y `os.fsync()`, y luego se reemplaza atómicamente el archivo final con `os.replace()`. Esto previene archivos corruptos si la aplicación se cerrase abruptamente.
- **Respaldo Previo (.bak)**: Antes de sobrescribir `config.json` o `registros.csv`, se genera una copia fiel en `config.bak` y `registros.csv.bak`. El usuario puede restaurar a la versión inmediatamente anterior desde la interfaz.
- **Manejo Explícito de Errores de Archivo**:
  - `FileNotFoundError`: inicialización automática con valores por defecto.
  - Archivo corrupto / formato inválido (`JSONDecodeError` / CSV malformado): captura controlada, degradación a valores seguros o rescate desde el archivo `.bak`.
  - `PermissionError`: notificación visual clara al usuario mediante ventanas de alerta, sin provocar cierres abruptos ni tracebacks sin capturar (`sys.excepthook` integrado).
- **Codificación Explícita UTF-8**: Tanto lectura como escritura utilizan estrictamente `encoding="utf-8"`, garantizando soporte total para tildes, caracteres como la `ñ`, diéresis y signos especiales (`¿`, `¡`).

---

##  Estructura del Proyecto

```text
G:\Mi unidad\SEGUNDO SEMESTRE 2026\ARCHIVOS\proyecto\
├── core/
│   ├── __init__.py
│   ├── i18n.py               # Diccionario y motor bilingüe (Español / Inglés)
│   ├── config_manager.py     # Gestor de configuración con atomic write y .bak
│   └── storage_manager.py    # Gestor de registros CSV con atomic write y .bak
├── ui/
│   ├── __init__.py
│   ├── style.py              # Generador dinámico de temas QSS (Claro/Oscuro, fuentes, colores)
│   ├── sidebar.py            # Barra lateral con perfil, avatar y botones
│   ├── main_window.py        # Ventana principal y sincronización de vistas
│   └── views/
│       ├── __init__.py
│       ├── clock_view.py     # Marcado de tiempos y estados en vivo
│       ├── read_view.py      # Visor y buscador de registros CSV
│       ├── add_view.py       # Registro manual de nuevos bloques
│       ├── edit_view.py      # Modificación de estados (ej. Lunch -> Ready)
│       ├── delete_view.py    # Eliminación con pop-up de descuento de horas
│       ├── settings_view.py  # Panel de configuración personalizada
│       └── backup_view.py    # Restaurador y auditor de copias .bak
├── assets/                   # Recursos visuales y avatares
├── config.json               # Archivo de configuración activo
├── config.bak                # Respaldo previo de configuración
├── registros.csv             # Base de datos en texto plano CSV (UTF-8)
├── registros.csv.bak         # Respaldo previo del CSV
├── main.py                   # Script de inicio con capturador global de errores
├── requirements.txt          # Dependencias (PyQt6)
└── README.md                 # Documentación completa
```

---

##  Instalación y Ejecución

1. **Requisitos**: Python 3.10 o superior (verificado con Python 3.14).
2. **Instalación de dependencias**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Iniciar la Aplicación**:
   ```bash
   python main.py
   ```
