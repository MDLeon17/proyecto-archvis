# -*- coding: utf-8 -*-
"""
MainWindow: Ventana principal de la aplicación.
Integra la Sidebar lateral, el QStackedWidget con las 7 vistas,
la aplicación dinámica de hojas de estilo (QSS), el enrutamiento y sincronización de datos.
"""

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QStackedWidget, QStatusBar
)
from PyQt6.QtCore import Qt

from core.i18n import t, I18n
from ui.style import generate_stylesheet
from ui.sidebar import SidebarWidget
from ui.views.clock_view import ClockView
from ui.views.read_view import ReadView
from ui.views.add_view import AddView
from ui.views.edit_view import EditView
from ui.views.delete_view import DeleteView
from ui.views.settings_view import SettingsView
from ui.views.backup_view import BackupView

class MainWindow(QMainWindow):
    def __init__(self, config_manager, storage_manager, parent=None):
        super().__init__(parent)
        self.config_manager = config_manager
        self.storage_manager = storage_manager

        # Configurar idioma inicial
        I18n.set_language(self.config_manager.get("idioma", "es"))

        self.setWindowTitle(t("app_title"))
        self.setMinimumSize(1100, 720)
        self.resize(1200, 780)

        self._init_ui()
        self.apply_theme_style()

    def _init_ui(self):
        # Contenedor central
        central_widget = QWidget()
        central_widget.setObjectName("CentralWidget")
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # 1. Sidebar lateral
        self.sidebar = SidebarWidget(self.config_manager, self)
        self.sidebar.navigation_requested.connect(self._on_navigation_requested)
        main_layout.addWidget(self.sidebar)

        # 2. Stacked Widget con las 7 vistas
        self.stack = QStackedWidget(self)

        # Índice 0: Control de Tiempo (Clock)
        self.view_clock = ClockView(self.storage_manager, self.config_manager, self)
        self.stack.addWidget(self.view_clock)

        # Índice 1: Consultar / Leer Registros
        self.view_read = ReadView(self.storage_manager, self.config_manager, self)
        self.stack.addWidget(self.view_read)

        # Índice 2: Agregar Registro Manual
        self.view_add = AddView(self.storage_manager, self.config_manager, self)
        self.stack.addWidget(self.view_add)

        # Índice 3: Editar Registro Específico
        self.view_edit = EditView(self.storage_manager, self.config_manager, self)
        self.stack.addWidget(self.view_edit)

        # Índice 4: Eliminar Registro
        self.view_delete = DeleteView(self.storage_manager, self.config_manager, self)
        self.stack.addWidget(self.view_delete)

        # Índice 5: Configuración (Settings)
        self.view_settings = SettingsView(self.config_manager, self)
        self.stack.addWidget(self.view_settings)

        # Índice 6: Copias de Seguridad (.bak)
        self.view_backup = BackupView(self.storage_manager, self.config_manager, self)
        self.stack.addWidget(self.view_backup)

        main_layout.addWidget(self.stack)

        # Barra de estado inferior
        self.status_bar = QStatusBar(self)
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Sistema listo • Persistencia segura activa (.tmp -> .csv / .bak)")

        # Conectar Señales y Sincronizaciones
        self._connect_signals()

    def _connect_signals(self):
        # Clock View signals
        self.view_clock.state_changed_signal.connect(self.sidebar.set_current_state)
        self.view_clock.records_updated_signal.connect(self._sync_all_views)

        # Add View signals
        self.view_add.record_added_signal.connect(self._sync_all_views)

        # Edit View signals
        self.view_edit.record_updated_signal.connect(self._sync_all_views)

        # Delete View signals
        self.view_delete.record_deleted_signal.connect(self._sync_all_views)

        # Read View actions (Editar y Eliminar directos)
        self.view_read.edit_record_requested.connect(self._go_to_edit_record)
        self.view_read.delete_record_requested.connect(self._go_to_delete_record)

        # Settings View signals
        self.view_settings.settings_saved_signal.connect(self._on_settings_saved)
        self.view_settings.theme_changed_signal.connect(self.apply_theme_style)

        # Backup View signals
        self.view_backup.records_restored_signal.connect(self._sync_all_views)
        self.view_backup.settings_restored_signal.connect(self._on_settings_saved)

    def _on_navigation_requested(self, page_index: int):
        self.stack.setCurrentIndex(page_index)
        
        # Acciones al entrar a cada vista
        if page_index == 1:
            self.view_read.reload_data()
        elif page_index == 3:
            self.view_edit.reload_records_selector()
        elif page_index == 4:
            self.view_delete.reload_data()
        elif page_index == 6:
            self.view_backup.refresh_status()

    def _go_to_edit_record(self, record_id: int):
        self.view_edit.load_record_by_id(record_id)
        self.stack.setCurrentIndex(3)
        self.sidebar.set_active_page(3)

    def _go_to_delete_record(self, record_id: int):
        self.view_delete.select_record_by_id(record_id)
        self.stack.setCurrentIndex(4)
        self.sidebar.set_active_page(4)

    def _sync_all_views(self):
        self.view_read.reload_data()
        self.view_edit.reload_records_selector()
        self.view_delete.reload_data()
        self.view_backup.refresh_status()
        self.status_bar.showMessage("Registros sincronizados con base de datos CSV y respaldo .bak.")

    def _on_settings_saved(self):
        # Actualizar textos de idioma
        self.setWindowTitle(t("app_title"))
        self.sidebar.update_user_info()
        self.sidebar.update_language_texts()
        self.view_clock.update_language_texts()
        self.view_read.update_language_texts()
        self.view_add.update_language_texts()
        self.view_edit.update_language_texts()
        self.view_delete.update_language_texts()
        self.view_settings.update_language_texts()
        self.view_backup.update_language_texts()
        self.apply_theme_style()
        self.status_bar.showMessage("Configuración aplicada exitosamente.")

    def apply_theme_style(self):
        cfg = self.config_manager.config
        theme = cfg.get("tema_interfaz", "oscuro")
        font_size = int(cfg.get("tamaño_fuente", 11))
        sidebar_col = cfg.get("color_barra_menu", "#1e293b")
        font_col = cfg.get("color_letra", "#f8fafc")

        qss = generate_stylesheet(
            theme=theme,
            font_size=font_size,
            sidebar_color=sidebar_col,
            font_color=font_col
        )
        self.setStyleSheet(qss)
