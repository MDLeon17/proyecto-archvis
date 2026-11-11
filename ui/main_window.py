# -*- coding: utf-8 -*-
"""
MainWindow: Ventana principal de la aplicación simplificada.
Integra la Sidebar lateral con únicamente los menús de Perfil y Configuración,
el QStackedWidget con ProfileView y SettingsView, y la sincronización dinámica
de estilos QSS en tiempo real.
"""

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QStackedWidget, QStatusBar
)
from PyQt6.QtCore import Qt

from core.i18n import t, I18n
from ui.style import generate_stylesheet
from ui.sidebar import SidebarWidget
from ui.views.profile_view import ProfileView
from ui.views.settings_view import SettingsView

class MainWindow(QMainWindow):
    def __init__(self, config_manager, parent=None):
        super().__init__(parent)
        self.config_manager = config_manager

        # Configurar idioma inicial
        I18n.set_language(self.config_manager.get("idioma", "es"))

        self.setWindowTitle(t("app_title"))
        self.setMinimumSize(950, 680)
        self.resize(1100, 740)

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

        # 1. Sidebar lateral con únicamente Perfil y Configuración
        self.sidebar = SidebarWidget(self.config_manager, self)
        self.sidebar.navigation_requested.connect(self._on_navigation_requested)
        main_layout.addWidget(self.sidebar)

        # 2. Stacked Widget con las 2 vistas solicitadas
        self.stack = QStackedWidget(self)

        # Índice 0: Perfil de Usuario y Muestra de Personalización
        self.view_profile = ProfileView(self.config_manager, self)
        self.view_profile.edit_profile_requested.connect(self._go_to_settings)
        self.stack.addWidget(self.view_profile)

        # Índice 1: Configuración del Sistema (Settings)
        self.view_settings = SettingsView(self.config_manager, self)
        self.view_settings.settings_saved_signal.connect(self._on_settings_saved)
        self.view_settings.theme_changed_signal.connect(self.apply_theme_style)
        self.stack.addWidget(self.view_settings)

        main_layout.addWidget(self.stack)

        # Barra de estado inferior
        self.status_bar = QStatusBar(self)
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Sistema listo • Persistencia segura activa (.tmp -> .json / .bak)")

    def _on_navigation_requested(self, page_index: int):
        self.stack.setCurrentIndex(page_index)
        if page_index == 0:
            self.view_profile.refresh_profile()

    def _go_to_settings(self):
        self.stack.setCurrentIndex(1)
        self.sidebar.set_active_page(1)

    def _on_settings_saved(self):
        # Actualizar textos según idioma
        self.setWindowTitle(t("app_title"))
        self.sidebar.update_user_info()
        self.sidebar.update_language_texts()
        self.view_profile.update_language_texts()
        self.view_profile.refresh_profile()
        self.view_settings.update_language_texts()
        self.apply_theme_style()
        self.status_bar.showMessage("Configuración guardada y personalización aplicada en todo el sistema.")

    def apply_theme_style(self):
        cfg = self.config_manager.config
        theme = cfg.get("tema_interfaz", "oscuro")
        font_size = int(cfg.get("tamaño_fuente", 11))
        sidebar_col = cfg.get("color_barra_menu", "#1e293b")
        font_col = cfg.get("color_letra", "#f8fafc")
        button_col = cfg.get("color_botones", "#2563eb")

        qss = generate_stylesheet(
            theme=theme,
            font_size=font_size,
            sidebar_color=sidebar_col,
            font_color=font_col,
            button_color=button_col
        )
        self.setStyleSheet(qss)
