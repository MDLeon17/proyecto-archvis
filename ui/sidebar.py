# -*- coding: utf-8 -*-
"""
SidebarWidget: Panel lateral de navegación con avatar de usuario,
nombre, rol y únicamente los 2 botones solicitados: Perfil y Configuración.
Sin emojis.
"""

import os
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton,
    QFrame, QButtonGroup
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QPixmap, QPainter, QPainterPath, QColor, QFont

from core.i18n import t
from ui.style import is_color_dark

class SidebarWidget(QWidget):
    navigation_requested = pyqtSignal(int)

    def __init__(self, config_manager, parent=None):
        super().__init__(parent)
        self.config_manager = config_manager
        self.setObjectName("SidebarWidget")
        self.setFixedWidth(240)
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 24, 16, 24)
        layout.setSpacing(14)

        # Profile Frame
        profile_frame = QFrame()
        profile_frame.setObjectName("ProfileFrame")
        p_layout = QVBoxLayout(profile_frame)
        p_layout.setContentsMargins(0, 0, 0, 10)
        p_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        p_layout.setSpacing(10)

        # Avatar Label
        self.avatar_label = QLabel()
        self.avatar_label.setFixedSize(76, 76)
        self.avatar_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        p_layout.addWidget(self.avatar_label)

        # Username Label
        self.username_label = QLabel()
        self.username_label.setObjectName("SidebarUsername")
        self.username_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        u_font = QFont("Segoe UI", 12, QFont.Weight.Bold)
        self.username_label.setFont(u_font)
        p_layout.addWidget(self.username_label)

        # Role Badge
        self.role_badge = QLabel()
        self.role_badge.setAlignment(Qt.AlignmentFlag.AlignCenter)
        p_layout.addWidget(self.role_badge)

        self.update_user_info()
        layout.addWidget(profile_frame)

        # Separator Line
        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet("background-color: rgba(128, 128, 128, 0.25); max-height: 1px;")
        layout.addWidget(sep)

        # Navigation Buttons (Únicamente Perfil y Configuración)
        self.btn_group = QButtonGroup(self)
        self.btn_group.setExclusive(True)

        self.btn_profile = QPushButton(t("nav_profile"))
        self.btn_profile.setObjectName("SidebarNavBtn")
        self.btn_profile.setCheckable(True)
        self.btn_profile.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_group.addButton(self.btn_profile, 0)
        layout.addWidget(self.btn_profile)

        self.btn_settings = QPushButton(t("nav_settings"))
        self.btn_settings.setObjectName("SidebarNavBtn")
        self.btn_settings.setCheckable(True)
        self.btn_settings.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_group.addButton(self.btn_settings, 1)
        layout.addWidget(self.btn_settings)

        self.btn_group.idClicked.connect(self._on_nav_clicked)
        self.btn_profile.setChecked(True)

        layout.addStretch()

        # Version label
        self.version_label = QLabel(t("sidebar_version"))
        self.version_label.setObjectName("SidebarVersion")
        self.version_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.version_label)

    def _on_nav_clicked(self, page_index: int):
        self.navigation_requested.emit(page_index)

    def set_active_page(self, page_index: int):
        btn = self.btn_group.button(page_index)
        if btn:
            btn.setChecked(True)

    def update_avatar(self):
        photo_path = self.config_manager.get("foto_perfil", "")
        btn_color = self.config_manager.get("color_botones", "#2563eb")
        size = 72
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
            painter = QPainter(pixmap)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            painter.setBrush(QColor(btn_color))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawEllipse(0, 0, size, size)

            username = self.config_manager.get("nombre_usuario", "Fernando")
            initial = (username[0] if username else "F").upper()
            btn_is_dark = is_color_dark(btn_color)
            painter.setPen(QColor("#ffffff" if btn_is_dark else "#0f172a"))
            font = QFont("Segoe UI", 24, QFont.Weight.Bold)
            painter.setFont(font)
            painter.drawText(pixmap.rect(), Qt.AlignmentFlag.AlignCenter, initial)
            painter.end()

        self.avatar_label.setPixmap(pixmap)

    def update_user_info(self):
        username = self.config_manager.get("nombre_usuario", "Fernando")
        role = self.config_manager.get("rol_usuario", "Administrador")
        btn_color = self.config_manager.get("color_botones", "#2563eb")

        self.username_label.setText(username)
        self.role_badge.setText(role)
        
        btn_is_dark = is_color_dark(btn_color)
        text_col = "#ffffff" if btn_is_dark else "#0f172a"
        self.role_badge.setStyleSheet(
            f"background-color: {btn_color}; color: {text_col}; border-radius: 10px; "
            f"padding: 3px 12px; font-weight: 600; font-size: 8.5pt;"
        )
        self.update_avatar()

    def update_language_texts(self):
        self.btn_profile.setText(t("nav_profile"))
        self.btn_settings.setText(t("nav_settings"))
        self.version_label.setText(t("sidebar_version"))
        self.update_user_info()
