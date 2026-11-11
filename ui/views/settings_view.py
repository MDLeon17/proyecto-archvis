# -*- coding: utf-8 -*-
"""
SettingsView: Ventana completa de configuración (Settings).
Permite modificar el tema de pantalla (claro/oscuro), idioma del sistema,
color de botones, color de barra lateral, color de letra, tamaño de fuente,
foto de perfil, datos de usuario y persistencia atómica con respaldo .bak.
"""

import os
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QLineEdit, QComboBox, QSpinBox, QColorDialog,
    QFileDialog, QMessageBox, QGridLayout, QScrollArea
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QColor, QPixmap, QPainter, QPainterPath

from core.i18n import t, I18n
from ui.style import is_color_dark

class SettingsView(QWidget):
    settings_saved_signal = pyqtSignal()
    theme_changed_signal = pyqtSignal()

    def __init__(self, config_manager, parent=None):
        super().__init__(parent)
        self.config_manager = config_manager
        
        cfg = self.config_manager.config
        self.selected_button_color = cfg.get("color_botones", "#2563eb")
        self.selected_sidebar_color = cfg.get("color_barra_menu", "#1e293b")
        self.selected_font_color = cfg.get("color_letra", "#f8fafc")
        self.selected_photo_path = cfg.get("foto_perfil", "")

        self._init_ui()
        self.load_values_to_ui()

    def _init_ui(self):
        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)

        content_widget = QWidget()
        main_layout = QVBoxLayout(content_widget)
        main_layout.setContentsMargins(24, 24, 24, 24)
        main_layout.setSpacing(20)

        # 1. Header Card
        header_card = QFrame()
        header_card.setProperty("class", "card")
        h_layout = QVBoxLayout(header_card)

        self.title_lbl = QLabel(t("settings_title"))
        self.title_lbl.setProperty("class", "heading-1")
        h_layout.addWidget(self.title_lbl)

        self.subtitle_lbl = QLabel(t("settings_subtitle"))
        self.subtitle_lbl.setProperty("class", "subtitle")
        h_layout.addWidget(self.subtitle_lbl)
        main_layout.addWidget(header_card)

        # 2. Section: Profile Information Card
        profile_card = QFrame()
        profile_card.setProperty("class", "card")
        p_card_layout = QVBoxLayout(profile_card)
        p_card_layout.setSpacing(14)

        self.profile_sec_title = QLabel(t("cfg_profile_section"))
        self.profile_sec_title.setProperty("class", "heading-2")
        p_card_layout.addWidget(self.profile_sec_title)

        grid_profile = QGridLayout()
        grid_profile.setSpacing(12)

        # Username
        self.lbl_user = QLabel(t("cfg_username"))
        grid_profile.addWidget(self.lbl_user, 0, 0)
        self.input_username = QLineEdit()
        grid_profile.addWidget(self.input_username, 0, 1, 1, 2)

        # Role
        self.lbl_role = QLabel(t("cfg_user_role"))
        grid_profile.addWidget(self.lbl_role, 1, 0)
        self.input_role = QLineEdit()
        grid_profile.addWidget(self.input_role, 1, 1, 1, 2)

        # Bio
        self.lbl_bio = QLabel(t("cfg_bio"))
        grid_profile.addWidget(self.lbl_bio, 2, 0)
        self.input_bio = QLineEdit()
        grid_profile.addWidget(self.input_bio, 2, 1, 1, 2)

        # Profile Photo
        self.lbl_photo = QLabel(t("cfg_profile_photo"))
        grid_profile.addWidget(self.lbl_photo, 3, 0)

        photo_btn_layout = QHBoxLayout()
        self.btn_pick_photo = QPushButton(t("btn_pick_photo"))
        self.btn_pick_photo.clicked.connect(self._pick_photo)
        photo_btn_layout.addWidget(self.btn_pick_photo)

        self.btn_remove_photo = QPushButton(t("btn_remove_photo"))
        self.btn_remove_photo.setProperty("class", "btn-secondary")
        self.btn_remove_photo.clicked.connect(self._remove_photo)
        photo_btn_layout.addWidget(self.btn_remove_photo)
        grid_profile.addLayout(photo_btn_layout, 3, 1)

        self.preview_photo = QLabel()
        self.preview_photo.setFixedSize(52, 52)
        self.preview_photo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        grid_profile.addWidget(self.preview_photo, 3, 2)

        p_card_layout.addLayout(grid_profile)
        main_layout.addWidget(profile_card)

        # 3. Section: Appearance & Screen Customization Card
        appearance_card = QFrame()
        appearance_card.setProperty("class", "card")
        a_layout = QVBoxLayout(appearance_card)
        a_layout.setSpacing(14)

        self.appearance_sec_title = QLabel(t("cfg_appearance_section"))
        self.appearance_sec_title.setProperty("class", "heading-2")
        a_layout.addWidget(self.appearance_sec_title)

        grid_app = QGridLayout()
        grid_app.setSpacing(14)

        # Modo de Pantalla (Tema Claro / Oscuro)
        self.lbl_theme = QLabel(t("cfg_theme"))
        grid_app.addWidget(self.lbl_theme, 0, 0)
        self.combo_theme = QComboBox()
        self.combo_theme.addItem("Oscuro (Dark Mode)", "oscuro")
        self.combo_theme.addItem("Claro (Light Mode)", "claro")
        self.combo_theme.currentIndexChanged.connect(self._on_theme_combo_changed)
        grid_app.addWidget(self.combo_theme, 0, 1, 1, 2)

        # Idioma del Sistema (es / en)
        self.lbl_lang = QLabel(t("cfg_language"))
        grid_app.addWidget(self.lbl_lang, 1, 0)
        self.combo_lang = QComboBox()
        self.combo_lang.addItem("Español (es)", "es")
        self.combo_lang.addItem("English (en)", "en")
        grid_app.addWidget(self.combo_lang, 1, 1, 1, 2)

        # Tamaño de Fuente
        self.lbl_font_size = QLabel(t("cfg_font_size"))
        grid_app.addWidget(self.lbl_font_size, 2, 0)
        self.spin_font_size = QSpinBox()
        self.spin_font_size.setRange(8, 22)
        self.spin_font_size.setValue(11)
        self.spin_font_size.setSuffix(" pt")
        grid_app.addWidget(self.spin_font_size, 2, 1, 1, 2)

        # Color de Botones (QColorDialog)
        self.lbl_btn_color = QLabel(t("cfg_button_color"))
        grid_app.addWidget(self.lbl_btn_color, 3, 0)

        self.btn_pick_btn_color = QPushButton(t("btn_pick_color"))
        self.btn_pick_btn_color.clicked.connect(self._pick_button_color)
        grid_app.addWidget(self.btn_pick_btn_color, 3, 1)

        self.preview_btn_color = QLabel()
        self.preview_btn_color.setFixedSize(64, 32)
        grid_app.addWidget(self.preview_btn_color, 3, 2)

        # Color de la barra de menú / lateral (QColorDialog)
        self.lbl_sidebar_color = QLabel(t("cfg_sidebar_color"))
        grid_app.addWidget(self.lbl_sidebar_color, 4, 0)

        self.btn_pick_sidebar_color = QPushButton(t("btn_pick_color"))
        self.btn_pick_sidebar_color.clicked.connect(self._pick_sidebar_color)
        grid_app.addWidget(self.btn_pick_sidebar_color, 4, 1)

        self.preview_sidebar_color = QLabel()
        self.preview_sidebar_color.setFixedSize(64, 32)
        grid_app.addWidget(self.preview_sidebar_color, 4, 2)

        # Color de letra / tipografía (QColorDialog)
        self.lbl_font_color = QLabel(t("cfg_font_color"))
        grid_app.addWidget(self.lbl_font_color, 5, 0)

        self.btn_pick_font_color = QPushButton(t("btn_pick_color"))
        self.btn_pick_font_color.clicked.connect(self._pick_font_color)
        grid_app.addWidget(self.btn_pick_font_color, 5, 1)

        self.preview_font_color = QLabel("Aa Bb")
        self.preview_font_color.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.preview_font_color.setFixedSize(64, 32)
        grid_app.addWidget(self.preview_font_color, 5, 2)

        a_layout.addLayout(grid_app)

        # Persistence info box
        info_box = QFrame()
        info_box.setProperty("class", "card-alt")
        ib_layout = QVBoxLayout(info_box)
        self.persistence_info_lbl = QLabel(t("cfg_persistence_info"))
        self.persistence_info_lbl.setStyleSheet("color: #64748b; font-size: 8.5pt;")
        self.persistence_info_lbl.setWordWrap(True)
        ib_layout.addWidget(self.persistence_info_lbl)
        a_layout.addWidget(info_box)

        # Action Buttons Layout
        btn_layout = QHBoxLayout()
        self.btn_reset_defaults = QPushButton(t("btn_reset_defaults"))
        self.btn_reset_defaults.setProperty("class", "btn-secondary")
        self.btn_reset_defaults.clicked.connect(self.reset_defaults)
        btn_layout.addWidget(self.btn_reset_defaults)

        self.btn_restore_bak = QPushButton(t("btn_restore_settings_bak"))
        self.btn_restore_bak.setProperty("class", "btn-secondary")
        self.btn_restore_bak.clicked.connect(self.restore_backup)
        btn_layout.addWidget(self.btn_restore_bak)

        btn_layout.addStretch()

        self.btn_save = QPushButton(t("btn_save_settings"))
        self.btn_save.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_save.clicked.connect(self.save_settings)
        btn_layout.addWidget(self.btn_save)

        a_layout.addLayout(btn_layout)
        main_layout.addWidget(appearance_card)

        # Feedback Banner
        self.feedback_banner = QLabel("")
        self.feedback_banner.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.feedback_banner.setStyleSheet("color: #059669; font-weight: bold; font-size: 11pt;")
        main_layout.addWidget(self.feedback_banner)

        main_layout.addStretch()

        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(0, 0, 0, 0)
        scroll.setWidget(content_widget)
        outer_layout.addWidget(scroll)

    def _on_theme_combo_changed(self, index):
        """Al cambiar el tema en el combobox, sugerir y actualizar la tipografía adecuada."""
        theme = self.combo_theme.currentData()
        if theme == "claro":
            self.selected_font_color = "#0f172a"
            if is_color_dark(self.selected_sidebar_color):
                self.selected_sidebar_color = "#f1f5f9"
        else:
            self.selected_font_color = "#f8fafc"
            if not is_color_dark(self.selected_sidebar_color):
                self.selected_sidebar_color = "#1e293b"

        self._update_color_preview(self.preview_btn_color, self.selected_button_color)
        self._update_color_preview(self.preview_sidebar_color, self.selected_sidebar_color)
        self._update_font_color_preview(self.selected_font_color)

    def load_values_to_ui(self):
        cfg = self.config_manager.config
        self.input_username.setText(cfg.get("nombre_usuario", "Fernando"))
        self.input_role.setText(cfg.get("rol_usuario", "Administrador"))
        self.input_bio.setText(cfg.get("biografia", "Usuario del Sistema de Personalización"))

        self.combo_theme.blockSignals(True)
        idx_theme = self.combo_theme.findData(cfg.get("tema_interfaz", "oscuro"))
        if idx_theme >= 0:
            self.combo_theme.setCurrentIndex(idx_theme)
        self.combo_theme.blockSignals(False)

        idx_lang = self.combo_lang.findData(cfg.get("idioma", "es"))
        if idx_lang >= 0:
            self.combo_lang.setCurrentIndex(idx_lang)

        self.spin_font_size.setValue(int(cfg.get("tamaño_fuente", 11)))

        self.selected_button_color = cfg.get("color_botones", "#2563eb")
        self.selected_sidebar_color = cfg.get("color_barra_menu", "#1e293b")
        self.selected_font_color = cfg.get("color_letra", "#f8fafc")

        theme = cfg.get("tema_interfaz", "oscuro")
        if theme == "claro":
            if not is_color_dark(self.selected_font_color):
                self.selected_font_color = "#0f172a"
            if is_color_dark(self.selected_sidebar_color):
                self.selected_sidebar_color = "#f1f5f9"
        else:
            if is_color_dark(self.selected_font_color):
                self.selected_font_color = "#f8fafc"
            if not is_color_dark(self.selected_sidebar_color):
                self.selected_sidebar_color = "#1e293b"

        self._update_color_preview(self.preview_btn_color, self.selected_button_color)
        self._update_color_preview(self.preview_sidebar_color, self.selected_sidebar_color)
        self._update_font_color_preview(self.selected_font_color)

        self.selected_photo_path = cfg.get("foto_perfil", "")
        self._update_photo_preview()

    def _update_color_preview(self, label: QLabel, hex_color: str):
        label.setStyleSheet(
            f"background-color: {hex_color}; border: 1px solid #94a3b8; border-radius: 6px;"
        )

    def _update_font_color_preview(self, hex_color: str):
        self.preview_font_color.setStyleSheet(
            f"color: {hex_color}; background-color: rgba(128, 128, 128, 0.2); border: 1px solid #94a3b8; "
            f"border-radius: 6px; font-weight: bold;"
        )

    def _update_photo_preview(self):
        size = 48
        pixmap = QPixmap(size, size)
        pixmap.fill(Qt.GlobalColor.transparent)

        loaded = False
        if self.selected_photo_path and os.path.exists(self.selected_photo_path):
            src_img = QPixmap(self.selected_photo_path)
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
            painter.setBrush(QColor(self.selected_button_color))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawEllipse(0, 0, size, size)
            painter.end()

        self.preview_photo.setPixmap(pixmap)

    def _pick_button_color(self):
        initial = QColor(self.selected_button_color)
        color = QColorDialog.getColor(initial, self, "Seleccionar Color de Botones")
        if color.isValid():
            self.selected_button_color = color.name()
            self._update_color_preview(self.preview_btn_color, self.selected_button_color)
            self._update_photo_preview()

    def _pick_sidebar_color(self):
        initial = QColor(self.selected_sidebar_color)
        color = QColorDialog.getColor(initial, self, "Seleccionar Color de la Barra Lateral")
        if color.isValid():
            self.selected_sidebar_color = color.name()
            self._update_color_preview(self.preview_sidebar_color, self.selected_sidebar_color)

    def _pick_font_color(self):
        initial = QColor(self.selected_font_color)
        color = QColorDialog.getColor(initial, self, "Seleccionar Color de Letra")
        if color.isValid():
            self.selected_font_color = color.name()
            self._update_font_color_preview(self.selected_font_color)

    def _pick_photo(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Seleccionar Foto de Perfil", "", t("file_filter_images")
        )
        if path:
            self.selected_photo_path = path
            self._update_photo_preview()

    def _remove_photo(self):
        self.selected_photo_path = ""
        self._update_photo_preview()

    def save_settings(self):
        username = self.input_username.text().strip()
        if not username:
            username = "Fernando"

        role = self.input_role.text().strip()
        if not role:
            role = "Administrador"

        bio = self.input_bio.text().strip()

        theme = self.combo_theme.currentData()
        lang = self.combo_lang.currentData()
        font_size = self.spin_font_size.value()

        # Validación de contraste según tema
        if theme == "claro":
            if not is_color_dark(self.selected_font_color):
                self.selected_font_color = "#0f172a"
            if is_color_dark(self.selected_sidebar_color):
                self.selected_sidebar_color = "#f1f5f9"
        else:
            if is_color_dark(self.selected_font_color):
                self.selected_font_color = "#f8fafc"
            if not is_color_dark(self.selected_sidebar_color):
                self.selected_sidebar_color = "#1e293b"

        new_config = {
            "nombre_usuario": username,
            "rol_usuario": role,
            "biografia": bio,
            "tema_interfaz": theme,
            "idioma": lang,
            "tamaño_fuente": font_size,
            "color_botones": self.selected_button_color,
            "color_barra_menu": self.selected_sidebar_color,
            "color_letra": self.selected_font_color,
            "foto_perfil": self.selected_photo_path
        }

        ok, msg = self.config_manager.save_config(new_config)
        if ok:
            I18n.set_language(lang)
            self.feedback_banner.setText(t("msg_saved_success"))
            QMessageBox.information(
                self, t("msg_success"),
                f"{t('msg_saved_success')}\nArchivo 'config.json' actualizado y copia 'config.bak' preservada."
            )
            self.settings_saved_signal.emit()
            self.theme_changed_signal.emit()
        else:
            QMessageBox.critical(self, t("msg_error"), msg)

    def restore_backup(self):
        confirm = QMessageBox.question(
            self, t("msg_warning"), t("msg_restore_confirm"),
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if confirm == QMessageBox.StandardButton.Yes:
            ok, msg = self.config_manager.restore_backup()
            if ok:
                I18n.set_language(self.config_manager.get("idioma", "es"))
                self.load_values_to_ui()
                QMessageBox.information(self, t("msg_success"), t("msg_restore_success"))
                self.settings_saved_signal.emit()
                self.theme_changed_signal.emit()
            else:
                QMessageBox.warning(self, t("msg_error"), msg)

    def reset_defaults(self):
        confirm = QMessageBox.question(
            self, t("msg_warning"), t("msg_reset_confirm"),
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if confirm == QMessageBox.StandardButton.Yes:
            ok, msg = self.config_manager.reset_to_defaults()
            if ok:
                I18n.set_language("es")
                self.load_values_to_ui()
                QMessageBox.information(self, t("msg_success"), "Configuración restablecida por defecto.")
                self.settings_saved_signal.emit()
                self.theme_changed_signal.emit()
            else:
                QMessageBox.warning(self, t("msg_error"), msg)

    def update_language_texts(self):
        self.title_lbl.setText(t("settings_title"))
        self.subtitle_lbl.setText(t("settings_subtitle"))
        self.profile_sec_title.setText(t("cfg_profile_section"))
        self.appearance_sec_title.setText(t("cfg_appearance_section"))
        self.lbl_user.setText(t("cfg_username"))
        self.lbl_role.setText(t("cfg_user_role"))
        self.lbl_bio.setText(t("cfg_bio"))
        self.lbl_photo.setText(t("cfg_profile_photo"))
        self.btn_pick_photo.setText(t("btn_pick_photo"))
        self.btn_remove_photo.setText(t("btn_remove_photo"))
        self.lbl_theme.setText(t("cfg_theme"))
        self.lbl_lang.setText(t("cfg_language"))
        self.lbl_font_size.setText(t("cfg_font_size"))
        self.lbl_btn_color.setText(t("cfg_button_color"))
        self.lbl_sidebar_color.setText(t("cfg_sidebar_color"))
        self.lbl_font_color.setText(t("cfg_font_color"))
        self.btn_pick_btn_color.setText(t("btn_pick_color"))
        self.btn_pick_sidebar_color.setText(t("btn_pick_color"))
        self.btn_pick_font_color.setText(t("btn_pick_color"))
        self.persistence_info_lbl.setText(t("cfg_persistence_info"))
        self.btn_reset_defaults.setText(t("btn_reset_defaults"))
        self.btn_restore_bak.setText(t("btn_restore_settings_bak"))
        self.btn_save.setText(t("btn_save_settings"))
