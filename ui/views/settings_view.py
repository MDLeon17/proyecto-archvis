# -*- coding: utf-8 -*-
"""
SettingsView: Ventana completa de configuración (Settings).
Asegura que al cambiar de Claro a Oscuro (o viceversa) se adapte automáticamente
el color de la tipografía y de la barra lateral para máxima legibilidad.
Sin emojis.
"""

import os
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QLineEdit, QComboBox, QSpinBox, QColorDialog,
    QFileDialog, QMessageBox, QGridLayout
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
        self.selected_sidebar_color = self.config_manager.get("color_barra_menu", "#1e293b")
        self.selected_font_color = self.config_manager.get("color_letra", "#f8fafc")
        self.selected_photo_path = self.config_manager.get("foto_perfil", "")

        self._init_ui()
        self.load_values_to_ui()

    def _init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(24, 24, 24, 24)
        main_layout.setSpacing(20)

        # Header Card
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

        # Settings Form Card
        form_card = QFrame()
        form_card.setProperty("class", "card")
        f_layout = QVBoxLayout(form_card)
        f_layout.setSpacing(16)

        grid = QGridLayout()
        grid.setSpacing(14)

        # 1. Nombre de Usuario
        self.lbl_user = QLabel(t("cfg_username"))
        grid.addWidget(self.lbl_user, 0, 0)
        self.input_username = QLineEdit()
        grid.addWidget(self.input_username, 0, 1, 1, 2)

        # 2. Tema de Interfaz (claro/oscuro)
        self.lbl_theme = QLabel(t("cfg_theme"))
        grid.addWidget(self.lbl_theme, 1, 0)
        self.combo_theme = QComboBox()
        self.combo_theme.addItem("Oscuro (Dark)", "oscuro")
        self.combo_theme.addItem("Claro (Light)", "claro")
        self.combo_theme.currentIndexChanged.connect(self._on_theme_combo_changed)
        grid.addWidget(self.combo_theme, 1, 1, 1, 2)

        # 3. Idioma (es / en)
        self.lbl_lang = QLabel(t("cfg_language"))
        grid.addWidget(self.lbl_lang, 2, 0)
        self.combo_lang = QComboBox()
        self.combo_lang.addItem("Español (es / es-ES)", "es")
        self.combo_lang.addItem("English (en / en-US)", "en")
        grid.addWidget(self.combo_lang, 2, 1, 1, 2)

        # 4. Tamaño de Fuente
        self.lbl_font_size = QLabel(t("cfg_font_size"))
        grid.addWidget(self.lbl_font_size, 3, 0)
        self.spin_font_size = QSpinBox()
        self.spin_font_size.setRange(8, 22)
        self.spin_font_size.setValue(11)
        self.spin_font_size.setSuffix(" pt")
        grid.addWidget(self.spin_font_size, 3, 1, 1, 2)

        # 5. Color de la barra de menú / lateral (QColorDialog)
        self.lbl_sidebar_color = QLabel(t("cfg_sidebar_color"))
        grid.addWidget(self.lbl_sidebar_color, 4, 0)
        
        self.btn_pick_sidebar_color = QPushButton(t("btn_pick_color"))
        self.btn_pick_sidebar_color.clicked.connect(self._pick_sidebar_color)
        grid.addWidget(self.btn_pick_sidebar_color, 4, 1)

        self.preview_sidebar_color = QLabel()
        self.preview_sidebar_color.setFixedSize(60, 32)
        grid.addWidget(self.preview_sidebar_color, 4, 2)

        # 6. Color de letra (QColorDialog)
        self.lbl_font_color = QLabel(t("cfg_font_color"))
        grid.addWidget(self.lbl_font_color, 5, 0)

        self.btn_pick_font_color = QPushButton(t("btn_pick_color"))
        self.btn_pick_font_color.clicked.connect(self._pick_font_color)
        grid.addWidget(self.btn_pick_font_color, 5, 1)

        self.preview_font_color = QLabel("Aa Bb")
        self.preview_font_color.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.preview_font_color.setFixedSize(60, 32)
        grid.addWidget(self.preview_font_color, 5, 2)

        # 7. Foto de Perfil (QFileDialog)
        self.lbl_photo = QLabel(t("cfg_profile_photo"))
        grid.addWidget(self.lbl_photo, 6, 0)

        photo_btn_layout = QHBoxLayout()
        self.btn_pick_photo = QPushButton(t("btn_pick_photo"))
        self.btn_pick_photo.clicked.connect(self._pick_photo)
        photo_btn_layout.addWidget(self.btn_pick_photo)

        self.btn_remove_photo = QPushButton(t("btn_remove_photo"))
        self.btn_remove_photo.setProperty("class", "btn-secondary")
        self.btn_remove_photo.clicked.connect(self._remove_photo)
        photo_btn_layout.addWidget(self.btn_remove_photo)
        grid.addLayout(photo_btn_layout, 6, 1)

        self.preview_photo = QLabel()
        self.preview_photo.setFixedSize(48, 48)
        self.preview_photo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        grid.addWidget(self.preview_photo, 6, 2)

        f_layout.addLayout(grid)

        # Info Box
        info_box = QFrame()
        info_box.setProperty("class", "card-alt")
        ib_layout = QVBoxLayout(info_box)
        ib_info = QLabel(
            "<b>Mecanismo de Persistencia Segura:</b> Al guardar, se genera un archivo temporal "
            "<code>config.tmp</code> y una copia previa de respaldo <code>config.bak</code> en UTF-8. "
            "El sistema ajusta el contraste de tipografía automáticamente según el modo seleccionado."
        )
        ib_info.setStyleSheet("color: #64748b; font-size: 8.5pt;")
        ib_info.setWordWrap(True)
        ib_layout.addWidget(ib_info)
        f_layout.addWidget(info_box)

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
        self.btn_save.setProperty("class", "btn-success")
        self.btn_save.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_save.clicked.connect(self.save_settings)
        btn_layout.addWidget(self.btn_save)

        f_layout.addLayout(btn_layout)
        main_layout.addWidget(form_card)

        # Feedback Banner
        self.feedback_banner = QLabel("")
        self.feedback_banner.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.feedback_banner.setStyleSheet("color: #059669; font-weight: bold; font-size: 11pt;")
        main_layout.addWidget(self.feedback_banner)

        main_layout.addStretch()

    def _on_theme_combo_changed(self, index):
        """Al cambiar el tema en el combobox, sugerir y actualizar la tipografía adecuada."""
        theme = self.combo_theme.currentData()
        if theme == "claro":
            # Si el usuario cambia a modo claro, la tipografía debe ser oscura para poder leerse
            self.selected_font_color = "#0f172a"
            # Si la barra lateral es oscura, cambiarla al fondo claro estándar para legibilidad
            if is_color_dark(self.selected_sidebar_color):
                self.selected_sidebar_color = "#f1f5f9"
        else:
            # En modo oscuro, la tipografía debe ser clara
            self.selected_font_color = "#f8fafc"
            # Si la barra lateral es clara, cambiarla al fondo oscuro estándar para legibilidad
            if not is_color_dark(self.selected_sidebar_color):
                self.selected_sidebar_color = "#1e293b"

        self._update_color_preview(self.preview_sidebar_color, self.selected_sidebar_color)
        self._update_font_color_preview(self.selected_font_color)

    def load_values_to_ui(self):
        cfg = self.config_manager.config
        self.input_username.setText(cfg.get("nombre_usuario", "Operador"))
        
        # Bloquear señales temporalmente al cargar
        self.combo_theme.blockSignals(True)
        idx_theme = self.combo_theme.findData(cfg.get("tema_interfaz", "oscuro"))
        if idx_theme >= 0:
            self.combo_theme.setCurrentIndex(idx_theme)
        self.combo_theme.blockSignals(False)

        idx_lang = self.combo_lang.findData(cfg.get("idioma", "es"))
        if idx_lang >= 0:
            self.combo_lang.setCurrentIndex(idx_lang)

        self.spin_font_size.setValue(int(cfg.get("tamaño_fuente", 11)))

        self.selected_sidebar_color = cfg.get("color_barra_menu", "#1e293b")
        self.selected_font_color = cfg.get("color_letra", "#f8fafc")
        
        # Validar consistencia de color tipográfico y barra lateral con el tema cargado
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
        size = 44
        pixmap = QPixmap(size, size)
        pixmap.fill(Qt.GlobalColor.transparent)

        loaded = False
        if self.selected_photo_path and os.path.exists(self.selected_photo_path):
            src_img = QPixmap(self.selected_photo_path)
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
            painter.setBrush(QColor("#64748b"))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawEllipse(0, 0, size, size)
            painter.end()

        self.preview_photo.setPixmap(pixmap)

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
            username = "Operador"

        theme = self.combo_theme.currentData()
        lang = self.combo_lang.currentData()
        font_size = self.spin_font_size.value()

        # Asegurar contraste de tipografía y barra lateral según el tema antes de persistir
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
            "tema_interfaz": theme,
            "idioma": lang,
            "tamaño_fuente": font_size,
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
                f"{t('msg_saved_success')}\nArchivo 'config.json' actualizado y 'config.bak' preservado."
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
            self, t("msg_warning"),
            "Desea restablecer todas las configuraciones a sus valores originales?",
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
        self.lbl_user.setText(t("cfg_username"))
        self.lbl_theme.setText(t("cfg_theme"))
        self.lbl_lang.setText(t("cfg_language"))
        self.lbl_font_size.setText(t("cfg_font_size"))
        self.lbl_sidebar_color.setText(t("cfg_sidebar_color"))
        self.lbl_font_color.setText(t("cfg_font_color"))
        self.lbl_photo.setText(t("cfg_profile_photo"))
        self.btn_pick_sidebar_color.setText(t("btn_pick_color"))
        self.btn_pick_font_color.setText(t("btn_pick_color"))
        self.btn_pick_photo.setText(t("btn_pick_photo"))
        self.btn_remove_photo.setText(t("btn_remove_photo"))
        self.btn_reset_defaults.setText(t("btn_reset_defaults"))
        self.btn_restore_bak.setText(t("btn_restore_settings_bak"))
        self.btn_save.setText(t("btn_save_settings"))
