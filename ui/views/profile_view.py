# -*- coding: utf-8 -*-
"""
ProfileView: Vista de Perfil de Usuario y Muestra de Personalización.
Muestra la identidad del usuario y expone en detalle la personalización
visual (tema claro/oscuro, idioma, color de botones, color de barra,
color de letra y tamaño de fuente) configurada en Settings.
"""

import os
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QGridLayout, QScrollArea
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QPixmap, QPainter, QPainterPath, QColor, QFont

from core.i18n import t
from ui.style import is_color_dark

class ProfileView(QWidget):
    edit_profile_requested = pyqtSignal()

    def __init__(self, config_manager, parent=None):
        super().__init__(parent)
        self.config_manager = config_manager
        self._init_ui()
        self.refresh_profile()

    def _init_ui(self):
        # Usar un QScrollArea para asegurar visualización perfecta en cualquier resolución
        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)

        content_widget = QWidget()
        self.main_layout = QVBoxLayout(content_widget)
        self.main_layout.setContentsMargins(24, 24, 24, 24)
        self.main_layout.setSpacing(20)

        # 1. Header Card
        self.header_card = QFrame()
        self.header_card.setProperty("class", "card")
        h_layout = QVBoxLayout(self.header_card)

        self.title_lbl = QLabel(t("profile_title"))
        self.title_lbl.setProperty("class", "heading-1")
        h_layout.addWidget(self.title_lbl)

        self.subtitle_lbl = QLabel(t("profile_subtitle"))
        self.subtitle_lbl.setProperty("class", "subtitle")
        h_layout.addWidget(self.subtitle_lbl)

        self.main_layout.addWidget(self.header_card)

        # 2. Main Identity & Customization Grid
        grid_top = QGridLayout()
        grid_top.setSpacing(20)

        # 2.1 Tarjeta de Identidad del Usuario (User Identity Card)
        self.user_card = QFrame()
        self.user_card.setProperty("class", "card")
        u_layout = QVBoxLayout(self.user_card)
        u_layout.setSpacing(14)

        self.user_card_title = QLabel(t("profile_card_title"))
        self.user_card_title.setProperty("class", "heading-2")
        u_layout.addWidget(self.user_card_title)

        # Avatar Container
        avatar_box = QHBoxLayout()
        avatar_box.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.avatar_label = QLabel()
        self.avatar_label.setFixedSize(110, 110)
        self.avatar_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        avatar_box.addWidget(self.avatar_label)
        u_layout.addLayout(avatar_box)

        # User Info Text
        self.name_label = QLabel()
        self.name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        n_font = QFont("Segoe UI", 16, QFont.Weight.Bold)
        self.name_label.setFont(n_font)
        u_layout.addWidget(self.name_label)

        self.role_badge = QLabel()
        self.role_badge.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.role_badge.setStyleSheet(
            "background-color: #3b82f6; color: #ffffff; border-radius: 12px; "
            "padding: 5px 14px; font-weight: 600; font-size: 9.5pt;"
        )
        role_box = QHBoxLayout()
        role_box.setAlignment(Qt.AlignmentFlag.AlignCenter)
        role_box.addWidget(self.role_badge)
        u_layout.addLayout(role_box)

        self.bio_label = QLabel()
        self.bio_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.bio_label.setWordWrap(True)
        self.bio_label.setStyleSheet("color: #64748b; font-style: italic; padding: 4px 10px;")
        u_layout.addWidget(self.bio_label)

        u_layout.addStretch()

        # Botón de acceso directo a Configuración
        self.btn_edit_profile = QPushButton(t("btn_go_to_settings"))
        self.btn_edit_profile.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_edit_profile.clicked.connect(self.edit_profile_requested.emit)
        u_layout.addWidget(self.btn_edit_profile)

        grid_top.addWidget(self.user_card, 0, 0)

        # 2.2 Tarjeta de Resumen de Personalización Activa
        self.customization_card = QFrame()
        self.customization_card.setProperty("class", "card")
        c_layout = QVBoxLayout(self.customization_card)
        c_layout.setSpacing(14)

        self.customization_title = QLabel(t("profile_customization_title"))
        self.customization_title.setProperty("class", "heading-2")
        c_layout.addWidget(self.customization_title)

        # Cuadrícula de Atributos Personalizados
        c_grid = QGridLayout()
        c_grid.setSpacing(12)

        # Tema de Pantalla
        self.lbl_t_theme = QLabel(t("lbl_active_theme"))
        self.lbl_t_theme.setStyleSheet("font-weight: 600;")
        c_grid.addWidget(self.lbl_t_theme, 0, 0)
        self.val_theme = QLabel()
        c_grid.addWidget(self.val_theme, 0, 1)

        # Idioma
        self.lbl_t_lang = QLabel(t("lbl_active_lang"))
        self.lbl_t_lang.setStyleSheet("font-weight: 600;")
        c_grid.addWidget(self.lbl_t_lang, 1, 0)
        self.val_lang = QLabel()
        c_grid.addWidget(self.val_lang, 1, 1)

        # Tamaño de Fuente
        self.lbl_t_font_size = QLabel(t("lbl_active_font_size"))
        self.lbl_t_font_size.setStyleSheet("font-weight: 600;")
        c_grid.addWidget(self.lbl_t_font_size, 2, 0)
        self.val_font_size = QLabel()
        c_grid.addWidget(self.val_font_size, 2, 1)

        # Color de Botones
        self.lbl_t_btn_color = QLabel(t("lbl_active_button_color"))
        self.lbl_t_btn_color.setStyleSheet("font-weight: 600;")
        c_grid.addWidget(self.lbl_t_btn_color, 3, 0)
        
        btn_color_box = QHBoxLayout()
        self.swatch_btn_color = QLabel()
        self.swatch_btn_color.setFixedSize(28, 20)
        self.val_btn_color = QLabel()
        btn_color_box.addWidget(self.swatch_btn_color)
        btn_color_box.addWidget(self.val_btn_color)
        btn_color_box.addStretch()
        c_grid.addLayout(btn_color_box, 3, 1)

        # Color de Barra Lateral
        self.lbl_t_sidebar_color = QLabel(t("lbl_active_sidebar_color"))
        self.lbl_t_sidebar_color.setStyleSheet("font-weight: 600;")
        c_grid.addWidget(self.lbl_t_sidebar_color, 4, 0)

        sidebar_color_box = QHBoxLayout()
        self.swatch_sidebar_color = QLabel()
        self.swatch_sidebar_color.setFixedSize(28, 20)
        self.val_sidebar_color = QLabel()
        sidebar_color_box.addWidget(self.swatch_sidebar_color)
        sidebar_color_box.addWidget(self.val_sidebar_color)
        sidebar_color_box.addStretch()
        c_grid.addLayout(sidebar_color_box, 4, 1)

        # Color de Letra
        self.lbl_t_font_color = QLabel(t("lbl_active_font_color"))
        self.lbl_t_font_color.setStyleSheet("font-weight: 600;")
        c_grid.addWidget(self.lbl_t_font_color, 5, 0)

        font_color_box = QHBoxLayout()
        self.swatch_font_color = QLabel()
        self.swatch_font_color.setFixedSize(28, 20)
        self.val_font_color = QLabel()
        font_color_box.addWidget(self.swatch_font_color)
        font_color_box.addWidget(self.val_font_color)
        font_color_box.addStretch()
        c_grid.addLayout(font_color_box, 5, 1)

        c_layout.addLayout(c_grid)
        c_layout.addStretch()

        grid_top.addWidget(self.customization_card, 0, 1)
        grid_top.setColumnStretch(0, 4)
        grid_top.setColumnStretch(1, 5)

        self.main_layout.addLayout(grid_top)

        # 3. Laboratorio de Componentes en Vivo (Live Sample Components)
        self.samples_card = QFrame()
        self.samples_card.setProperty("class", "card-alt")
        s_layout = QVBoxLayout(self.samples_card)
        s_layout.setSpacing(14)

        self.samples_title = QLabel(t("profile_samples_title"))
        self.samples_title.setProperty("class", "heading-2")
        s_layout.addWidget(self.samples_title)

        self.sample_text_desc = QLabel(t("lbl_sample_text"))
        self.sample_text_desc.setWordWrap(True)
        s_layout.addWidget(self.sample_text_desc)

        # Botones de demostración en vivo
        demo_btn_layout = QHBoxLayout()
        demo_btn_layout.setSpacing(12)

        self.sample_btn_primary = QPushButton(t("lbl_sample_button_primary"))
        demo_btn_layout.addWidget(self.sample_btn_primary)

        self.sample_btn_secondary = QPushButton(t("lbl_sample_button_secondary"))
        self.sample_btn_secondary.setProperty("class", "btn-secondary")
        demo_btn_layout.addWidget(self.sample_btn_secondary)

        self.sample_badge = QLabel(t("status_customized"))
        self.sample_badge.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.sample_badge.setProperty("class", "badge")
        demo_btn_layout.addWidget(self.sample_badge)

        demo_btn_layout.addStretch()
        s_layout.addLayout(demo_btn_layout)

        self.main_layout.addWidget(self.samples_card)
        self.main_layout.addStretch()

        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(0, 0, 0, 0)
        scroll.setWidget(content_widget)
        outer_layout.addWidget(scroll)

    def refresh_profile(self):
        """Carga y refresca todos los datos y personalizaciones desde config_manager."""
        cfg = self.config_manager.config

        # 1. Datos del usuario
        username = cfg.get("nombre_usuario", "Fernando")
        role = cfg.get("rol_usuario", "Administrador")
        bio = cfg.get("biografia", "Usuario del Sistema de Personalización")
        photo_path = cfg.get("foto_perfil", "")

        self.name_label.setText(username)
        self.role_badge.setText(role)
        self.bio_label.setText(bio)

        # Avatar
        self._load_avatar(photo_path, username)

        # 2. Resumen de personalización
        theme = cfg.get("tema_interfaz", "oscuro")
        if theme == "oscuro":
            self.val_theme.setText(t("theme_dark_desc"))
        else:
            self.val_theme.setText(t("theme_light_desc"))

        lang = cfg.get("idioma", "es")
        self.val_lang.setText(t("lang_spanish") if lang == "es" else t("lang_english"))

        font_size = cfg.get("tamaño_fuente", 11)
        self.val_font_size.setText(f"{font_size} pt")

        btn_color = cfg.get("color_botones", "#2563eb")
        self.val_btn_color.setText(btn_color)
        self._set_swatch(self.swatch_btn_color, btn_color)

        sidebar_color = cfg.get("color_barra_menu", "#1e293b")
        self.val_sidebar_color.setText(sidebar_color)
        self._set_swatch(self.swatch_sidebar_color, sidebar_color)

        font_color = cfg.get("color_letra", "#f8fafc")
        self.val_font_color.setText(font_color)
        self._set_swatch(self.swatch_font_color, font_color)

        # Actualizar insignias y muestras
        btn_is_dark = is_color_dark(btn_color)
        btn_text_col = "#ffffff" if btn_is_dark else "#0f172a"
        self.role_badge.setStyleSheet(
            f"background-color: {btn_color}; color: {btn_text_col}; "
            f"border-radius: 12px; padding: 4px 14px; font-weight: 600; font-size: 9pt;"
        )

    def _set_swatch(self, label: QLabel, hex_color: str):
        label.setStyleSheet(
            f"background-color: {hex_color}; border: 1px solid #94a3b8; border-radius: 4px;"
        )

    def _load_avatar(self, photo_path: str, username: str):
        size = 104
        pixmap = QPixmap(size, size)
        pixmap.fill(Qt.GlobalColor.transparent)

        loaded = False
        if photo_path and os.path.exists(photo_path):
            src_img = QPixmap(photo_path)
            if not src_img.isNull():
                src_img = src_img.scaled(
                    size, size,
                    Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                    Qt.TransformationMode.SmoothTransformation
                )
                painter = QPainter(pixmap)
                painter.setRenderHint(QPainter.RenderHint.Antialiasing)
                path = QPainterPath()
                path.addEllipse(0, 0, size, size)
                painter.setClipPath(path)
                painter.drawPixmap(0, 0, src_img)
                painter.end()
                loaded = True

        if not loaded:
            btn_color = self.config_manager.get("color_botones", "#2563eb")
            painter = QPainter(pixmap)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            painter.setBrush(QColor(btn_color))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawEllipse(0, 0, size, size)

            initial = (username[0] if username else "U").upper()
            btn_is_dark = is_color_dark(btn_color)
            painter.setPen(QColor("#ffffff" if btn_is_dark else "#0f172a"))
            font = QFont("Segoe UI", 36, QFont.Weight.Bold)
            painter.setFont(font)
            painter.drawText(pixmap.rect(), Qt.AlignmentFlag.AlignCenter, initial)
            painter.end()

        self.avatar_label.setPixmap(pixmap)

    def update_language_texts(self):
        """Actualiza todos los textos estáticos según el idioma activo."""
        self.title_lbl.setText(t("profile_title"))
        self.subtitle_lbl.setText(t("profile_subtitle"))
        self.user_card_title.setText(t("profile_card_title"))
        self.customization_title.setText(t("profile_customization_title"))
        self.lbl_t_theme.setText(t("lbl_active_theme"))
        self.lbl_t_lang.setText(t("lbl_active_lang"))
        self.lbl_t_font_size.setText(t("lbl_active_font_size"))
        self.lbl_t_btn_color.setText(t("lbl_active_button_color"))
        self.lbl_t_sidebar_color.setText(t("lbl_active_sidebar_color"))
        self.lbl_t_font_color.setText(t("lbl_active_font_color"))
        self.samples_title.setText(t("profile_samples_title"))
        self.sample_text_desc.setText(t("lbl_sample_text"))
        self.sample_btn_primary.setText(t("lbl_sample_button_primary"))
        self.sample_btn_secondary.setText(t("lbl_sample_button_secondary"))
        self.sample_badge.setText(t("status_customized"))
        self.btn_edit_profile.setText(t("btn_go_to_settings"))
        self.refresh_profile()
