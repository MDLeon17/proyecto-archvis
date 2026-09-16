# -*- coding: utf-8 -*-
"""
SidebarWidget: Panel lateral de navegación con avatar de usuario,
estado actual en tiempo real y botones de acceso sin emoticonos.
"""

import os
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton,
    QFrame, QButtonGroup
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QPixmap, QPainter, QPainterPath, QColor, QFont

from core.i18n import t

class SidebarWidget(QWidget):
    navigation_requested = pyqtSignal(int)

    def __init__(self, config_manager, parent=None):
        super().__init__(parent)
        self.config_manager = config_manager
        self.setObjectName("SidebarWidget")
        self.setFixedWidth(250)
        self.current_state_text = "status_offline"
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(14, 20, 14, 20)
        layout.setSpacing(12)

        # Profile Frame
        profile_frame = QFrame()
        profile_frame.setObjectName("ProfileFrame")
        p_layout = QVBoxLayout(profile_frame)
        p_layout.setContentsMargins(0, 0, 0, 10)
        p_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        p_layout.setSpacing(8)

        # Avatar Label
        self.avatar_label = QLabel()
        self.avatar_label.setFixedSize(76, 76)
        self.avatar_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.update_avatar()
        p_layout.addWidget(self.avatar_label)

        # Username Label
        self.username_label = QLabel()
        self.username_label.setObjectName("SidebarUsername")
        self.username_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        u_font = QFont()
        u_font.setBold(True)
        u_font.setPointSize(12)
        self.username_label.setFont(u_font)
        p_layout.addWidget(self.username_label)

        # State Badge
        self.state_badge = QLabel()
        self.state_badge.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.state_badge.setStyleSheet(
            "background-color: #475569; color: #ffffff; border-radius: 10px; "
            "padding: 4px 12px; font-weight: 600; font-size: 9pt;"
        )
        p_layout.addWidget(self.state_badge)
        self.update_user_info()

        layout.addWidget(profile_frame)

        # Separator Line
        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet("background-color: rgba(128, 128, 128, 0.25); max-height: 1px;")
        layout.addWidget(sep)

        # Navigation Buttons (Sin emojis)
        self.btn_group = QButtonGroup(self)
        self.btn_group.setExclusive(True)

        self.nav_buttons = []
        nav_items = [
            (0, t("nav_clock"), "nav_clock"),
            (1, t("nav_read"), "nav_read"),
            (2, t("nav_add"), "nav_add"),
            (3, t("nav_edit"), "nav_edit"),
            (4, t("nav_delete"), "nav_delete"),
            (5, t("nav_settings"), "nav_settings"),
            (6, t("nav_backup"), "nav_backup"),
        ]

        for index, text, key in nav_items:
            btn = QPushButton(text)
            btn.setObjectName("SidebarNavBtn")
            btn.setCheckable(True)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setProperty("key", key)
            self.btn_group.addButton(btn, index)
            layout.addWidget(btn)
            self.nav_buttons.append(btn)

        self.btn_group.idClicked.connect(self._on_nav_clicked)
        if self.nav_buttons:
            self.nav_buttons[0].setChecked(True)

        layout.addStretch()

        # Version label
        self.version_label = QLabel("v2.0 • UTF-8 Safe CSV")
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
        size = 72
        pixmap = QPixmap(size, size)
        pixmap.fill(Qt.GlobalColor.transparent)

        loaded = False
        if photo_path and os.path.exists(photo_path):
            src_img = QPixmap(photo_path)
            if not src_img.isNull():
                src_img = src_img.scaled(size, size, Qt.AspectRatioMode.KeepAspectRatioByExpanding, Qt.TransformationMode.SmoothTransformation)
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
            painter.setBrush(QColor("#2563eb"))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawEllipse(0, 0, size, size)
            
            username = self.config_manager.get("nombre_usuario", "U")
            initial = (username[0] if username else "U").upper()
            painter.setPen(QColor("#ffffff"))
            font = QFont("Segoe UI", 24, QFont.Weight.Bold)
            painter.setFont(font)
            painter.drawText(pixmap.rect(), Qt.AlignmentFlag.AlignCenter, initial)
            painter.end()

        self.avatar_label.setPixmap(pixmap)

    def update_user_info(self):
        username = self.config_manager.get("nombre_usuario", "Operador")
        self.username_label.setText(username)
        self.set_current_state(self.current_state_text)
        self.update_avatar()

    def set_current_state(self, state_text: str):
        self.current_state_text = state_text
        state_colors = {
            "Ready": ("#059669", t("status_ready")),
            "Lunch": ("#d97706", t("status_lunch")),
            "Break": ("#0891b2", t("status_break")),
            "Meeting": ("#7c3aed", t("status_meeting")),
            "Training": ("#4f46e5", t("status_training")),
            "Clock In": ("#059669", t("status_clock_in")),
            "Clock Out": ("#dc2626", t("status_clock_out")),
            "status_offline": ("#64748b", t("status_offline"))
        }
        color, display = state_colors.get(state_text, ("#64748b", state_text))
        self.state_badge.setText(display)
        self.state_badge.setStyleSheet(
            f"background-color: {color}; color: #ffffff; border-radius: 10px; "
            f"padding: 4px 12px; font-weight: 600; font-size: 8.5pt;"
        )

    def update_language_texts(self):
        nav_titles = [
            t("nav_clock"),
            t("nav_read"),
            t("nav_add"),
            t("nav_edit"),
            t("nav_delete"),
            t("nav_settings"),
            t("nav_backup"),
        ]
        for i, btn in enumerate(self.nav_buttons):
            if i < len(nav_titles):
                btn.setText(nav_titles[i])
        self.set_current_state(self.current_state_text)
