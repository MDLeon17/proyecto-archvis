# -*- coding: utf-8 -*-
"""
AddView: Formulario para agregar un registro de tiempo manualmente sin emojis.
"""

import datetime
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QLineEdit, QComboBox, QDateEdit, QTimeEdit,
    QTextEdit, QMessageBox, QGridLayout
)
from PyQt6.QtCore import Qt, QDate, QTime, pyqtSignal

from core.i18n import t

class AddView(QWidget):
    record_added_signal = pyqtSignal()

    def __init__(self, storage_manager, config_manager, parent=None):
        super().__init__(parent)
        self.storage_manager = storage_manager
        self.config_manager = config_manager
        self._init_ui()

    def _init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(24, 24, 24, 24)
        main_layout.setSpacing(20)

        # Header Card
        header_card = QFrame()
        header_card.setProperty("class", "card")
        h_layout = QVBoxLayout(header_card)

        self.title_lbl = QLabel(t("add_title"))
        self.title_lbl.setProperty("class", "heading-1")
        h_layout.addWidget(self.title_lbl)

        self.subtitle_lbl = QLabel(t("add_subtitle"))
        self.subtitle_lbl.setProperty("class", "subtitle")
        h_layout.addWidget(self.subtitle_lbl)
        main_layout.addWidget(header_card)

        # Form Card
        form_card = QFrame()
        form_card.setProperty("class", "card")
        f_layout = QVBoxLayout(form_card)
        f_layout.setSpacing(16)

        grid = QGridLayout()
        grid.setSpacing(14)

        # Usuario
        self.lbl_user = QLabel(t("lbl_user"))
        grid.addWidget(self.lbl_user, 0, 0)
        self.input_user = QLineEdit()
        self.input_user.setText(self.config_manager.get("nombre_usuario", "Operador"))
        grid.addWidget(self.input_user, 0, 1)

        # Fecha
        self.lbl_date = QLabel(t("lbl_date"))
        grid.addWidget(self.lbl_date, 0, 2)
        self.input_date = QDateEdit()
        self.input_date.setCalendarPopup(True)
        self.input_date.setDate(QDate.currentDate())
        self.input_date.setDisplayFormat("yyyy-MM-dd")
        grid.addWidget(self.input_date, 0, 3)

        # Hora Inicio
        self.lbl_start = QLabel(t("lbl_start_time"))
        grid.addWidget(self.lbl_start, 1, 0)
        self.input_start = QTimeEdit()
        self.input_start.setDisplayFormat("HH:mm:ss")
        self.input_start.setTime(QTime(8, 0, 0))
        self.input_start.timeChanged.connect(self._recalculate_duration)
        grid.addWidget(self.input_start, 1, 1)

        # Hora Fin
        self.lbl_end = QLabel(t("lbl_end_time"))
        grid.addWidget(self.lbl_end, 1, 2)
        self.input_end = QTimeEdit()
        self.input_end.setDisplayFormat("HH:mm:ss")
        self.input_end.setTime(QTime(12, 0, 0))
        self.input_end.timeChanged.connect(self._recalculate_duration)
        grid.addWidget(self.input_end, 1, 3)

        # Estado
        self.lbl_status = QLabel(t("lbl_status"))
        grid.addWidget(self.lbl_status, 2, 0)
        self.combo_status = QComboBox()
        self.combo_status.addItems([
            "Ready", "Lunch", "Break", "Meeting", "Training", "Clock In", "Clock Out"
        ])
        grid.addWidget(self.combo_status, 2, 1)

        # Duración Calculada
        self.lbl_dur_calc = QLabel(t("lbl_duration_calc"))
        grid.addWidget(self.lbl_dur_calc, 2, 2)
        self.val_duration = QLabel("4.00 horas")
        self.val_duration.setStyleSheet("color: #059669; font-weight: bold; font-size: 12pt;")
        grid.addWidget(self.val_duration, 2, 3)

        f_layout.addLayout(grid)

        # Notas
        self.lbl_notes = QLabel(t("lbl_notes"))
        f_layout.addWidget(self.lbl_notes)
        self.input_notes = QTextEdit()
        self.input_notes.setPlaceholderText("Comentarios u observaciones sobre este registro de tiempo...")
        self.input_notes.setMaximumHeight(80)
        f_layout.addWidget(self.input_notes)

        # Botones
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        self.btn_clear = QPushButton(t("btn_clear_fields"))
        self.btn_clear.setProperty("class", "btn-secondary")
        self.btn_clear.clicked.connect(self.clear_form)
        btn_layout.addWidget(self.btn_clear)

        self.btn_save = QPushButton(t("btn_save_new"))
        self.btn_save.setProperty("class", "btn-success")
        self.btn_save.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_save.clicked.connect(self.save_record)
        btn_layout.addWidget(self.btn_save)

        f_layout.addLayout(btn_layout)
        main_layout.addWidget(form_card)

        # Feedback Banner
        self.feedback_banner = QLabel("")
        self.feedback_banner.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.feedback_banner.setStyleSheet("color: #059669; font-weight: bold; font-size: 11pt;")
        main_layout.addWidget(self.feedback_banner)

        main_layout.addStretch()
        self._recalculate_duration()

    def _recalculate_duration(self):
        t1 = self.input_start.time().toString("HH:mm:ss")
        t2 = self.input_end.time().toString("HH:mm:ss")
        hours = self.storage_manager.calculate_duration(t1, t2)
        self.val_duration.setText(f"{hours} horas")

    def save_record(self):
        user = self.input_user.text().strip()
        if not user:
            QMessageBox.warning(self, t("msg_warning"), "El nombre de usuario no puede estar vacío.")
            return

        date_str = self.input_date.date().toString("yyyy-MM-dd")
        start_str = self.input_start.time().toString("HH:mm:ss")
        end_str = self.input_end.time().toString("HH:mm:ss")
        status = self.combo_status.currentText()
        notes = self.input_notes.toPlainText().strip()
        dur = self.storage_manager.calculate_duration(start_str, end_str)

        new_record = {
            "usuario": user,
            "fecha": date_str,
            "hora_inicio": start_str,
            "hora_fin": end_str,
            "duracion_horas": dur,
            "estado": status,
            "notas": notes
        }

        ok, msg, rec_id = self.storage_manager.add_record(new_record)
        if ok:
            success_msg = t("record_added_msg", id=rec_id)
            self.feedback_banner.setText(success_msg)
            QMessageBox.information(self, t("msg_success"), f"{success_msg}\n{t('msg_saved_success')}")
            self.record_added_signal.emit()
            self.clear_form()
        else:
            QMessageBox.critical(self, t("msg_error"), f"Error al guardar: {msg}")

    def clear_form(self):
        self.input_user.setText(self.config_manager.get("nombre_usuario", "Operador"))
        self.input_date.setDate(QDate.currentDate())
        self.input_start.setTime(QTime(8, 0, 0))
        self.input_end.setTime(QTime(12, 0, 0))
        self.combo_status.setCurrentIndex(0)
        self.input_notes.clear()
        self._recalculate_duration()

    def update_language_texts(self):
        self.title_lbl.setText(t("add_title"))
        self.subtitle_lbl.setText(t("add_subtitle"))
        self.lbl_user.setText(t("lbl_user"))
        self.lbl_date.setText(t("lbl_date"))
        self.lbl_start.setText(t("lbl_start_time"))
        self.lbl_end.setText(t("lbl_end_time"))
        self.lbl_status.setText(t("lbl_status"))
        self.lbl_dur_calc.setText(t("lbl_duration_calc"))
        self.lbl_notes.setText(t("lbl_notes"))
        self.btn_clear.setText(t("btn_clear_fields"))
        self.btn_save.setText(t("btn_save_new"))
