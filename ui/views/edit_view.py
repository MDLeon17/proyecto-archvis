# -*- coding: utf-8 -*-
"""
EditView: Edición de un dato en concreto en el archivo CSV sin emojis.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QLineEdit, QComboBox, QDateEdit, QTimeEdit,
    QTextEdit, QMessageBox, QGridLayout
)
from PyQt6.QtCore import Qt, QDate, QTime, pyqtSignal

from core.i18n import t

class EditView(QWidget):
    record_updated_signal = pyqtSignal()

    def __init__(self, storage_manager, config_manager, parent=None):
        super().__init__(parent)
        self.storage_manager = storage_manager
        self.config_manager = config_manager
        self.current_record_id = None
        self._init_ui()
        self.reload_records_selector()

    def _init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(24, 24, 24, 24)
        main_layout.setSpacing(20)

        # Header Card
        header_card = QFrame()
        header_card.setProperty("class", "card")
        h_layout = QVBoxLayout(header_card)

        self.title_lbl = QLabel(t("edit_title"))
        self.title_lbl.setProperty("class", "heading-1")
        h_layout.addWidget(self.title_lbl)

        self.subtitle_lbl = QLabel(t("edit_subtitle"))
        self.subtitle_lbl.setProperty("class", "subtitle")
        h_layout.addWidget(self.subtitle_lbl)
        main_layout.addWidget(header_card)

        # Tip Card
        tip_card = QFrame()
        tip_card.setStyleSheet("background-color: #1e3a8a; border-radius: 8px; padding: 12px;")
        t_layout = QHBoxLayout(tip_card)
        self.tip_lbl = QLabel("Nota: " + t("edit_help_text"))
        self.tip_lbl.setStyleSheet("color: #bfdbfe; font-size: 9.5pt;")
        self.tip_lbl.setWordWrap(True)
        t_layout.addWidget(self.tip_lbl)
        main_layout.addWidget(tip_card)

        # Selection Bar Card
        sel_card = QFrame()
        sel_card.setProperty("class", "card")
        s_layout = QHBoxLayout(sel_card)
        s_layout.setSpacing(12)

        self.lbl_select_prompt = QLabel(t("select_record_prompt"))
        self.lbl_select_prompt.setStyleSheet("font-weight: 600;")
        s_layout.addWidget(self.lbl_select_prompt)

        self.combo_records = QComboBox()
        self.combo_records.currentIndexChanged.connect(self._on_record_selection_changed)
        s_layout.addWidget(self.combo_records, stretch=2)

        self.btn_refresh_list = QPushButton("Refrescar")
        self.btn_refresh_list.setProperty("class", "btn-secondary")
        self.btn_refresh_list.clicked.connect(self.reload_records_selector)
        s_layout.addWidget(self.btn_refresh_list)

        main_layout.addWidget(sel_card)

        # Form Card
        self.form_card = QFrame()
        self.form_card.setProperty("class", "card")
        f_layout = QVBoxLayout(self.form_card)
        f_layout.setSpacing(16)

        grid = QGridLayout()
        grid.setSpacing(14)

        # ID
        grid.addWidget(QLabel("<b>ID:</b>"), 0, 0)
        self.input_id = QLineEdit()
        self.input_id.setReadOnly(True)
        self.input_id.setStyleSheet("background-color: rgba(128, 128, 128, 0.1);")
        grid.addWidget(self.input_id, 0, 1)

        # Usuario
        grid.addWidget(QLabel("<b>" + t("col_user") + ":</b>"), 0, 2)
        self.input_user = QLineEdit()
        grid.addWidget(self.input_user, 0, 3)

        # Fecha
        grid.addWidget(QLabel("<b>" + t("col_date") + ":</b>"), 1, 0)
        self.input_date = QDateEdit()
        self.input_date.setCalendarPopup(True)
        self.input_date.setDisplayFormat("yyyy-MM-dd")
        grid.addWidget(self.input_date, 1, 1)

        # Estado
        grid.addWidget(QLabel("<b>" + t("col_status") + ":</b>"), 1, 2)
        self.combo_status = QComboBox()
        self.combo_status.addItems([
            "Ready", "Lunch", "Break", "Meeting", "Training", "Clock In", "Clock Out"
        ])
        self.combo_status.setStyleSheet("font-weight: bold;")
        grid.addWidget(self.combo_status, 1, 3)

        # Hora Inicio
        grid.addWidget(QLabel("<b>" + t("col_start") + ":</b>"), 2, 0)
        self.input_start = QTimeEdit()
        self.input_start.setDisplayFormat("HH:mm:ss")
        self.input_start.timeChanged.connect(self._recalculate_duration)
        grid.addWidget(self.input_start, 2, 1)

        # Hora Fin
        grid.addWidget(QLabel("<b>" + t("col_end") + ":</b>"), 2, 2)
        self.input_end = QTimeEdit()
        self.input_end.setDisplayFormat("HH:mm:ss")
        self.input_end.timeChanged.connect(self._recalculate_duration)
        grid.addWidget(self.input_end, 2, 3)

        # Duración Calculada
        grid.addWidget(QLabel("<b>" + t("col_duration") + ":</b>"), 3, 0)
        self.val_duration = QLabel("0.00 horas")
        self.val_duration.setStyleSheet("color: #059669; font-weight: bold; font-size: 13pt;")
        grid.addWidget(self.val_duration, 3, 1)

        f_layout.addLayout(grid)

        # Notas
        f_layout.addWidget(QLabel("<b>" + t("col_notes") + ":</b>"))
        self.input_notes = QTextEdit()
        self.input_notes.setMaximumHeight(80)
        f_layout.addWidget(self.input_notes)

        # Action Buttons
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        self.btn_cancel = QPushButton(t("btn_cancel_edit"))
        self.btn_cancel.setProperty("class", "btn-secondary")
        self.btn_cancel.clicked.connect(self._revert_current_record)
        btn_layout.addWidget(self.btn_cancel)

        self.btn_save = QPushButton(t("btn_save_changes"))
        self.btn_save.setProperty("class", "btn-success")
        self.btn_save.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_save.clicked.connect(self.save_modifications)
        btn_layout.addWidget(self.btn_save)

        f_layout.addLayout(btn_layout)
        main_layout.addWidget(self.form_card)

        # Feedback Banner
        self.feedback_banner = QLabel("")
        self.feedback_banner.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.feedback_banner.setStyleSheet("color: #059669; font-weight: bold; font-size: 11pt;")
        main_layout.addWidget(self.feedback_banner)

        main_layout.addStretch()

    def reload_records_selector(self, target_id=None):
        self.combo_records.blockSignals(True)
        self.combo_records.clear()

        records, _ = self.storage_manager.load_records()
        if not records:
            self.combo_records.addItem("No hay registros en el archivo CSV", None)
            self.form_card.setEnabled(False)
            self.combo_records.blockSignals(False)
            return

        self.form_card.setEnabled(True)
        selected_idx = 0
        for idx, r in enumerate(records):
            rec_id = r.get("id")
            display_text = (
                f"#{rec_id} • {r.get('usuario')} • {r.get('fecha')} • "
                f"{r.get('estado')} ({r.get('duracion_horas')}h)"
            )
            self.combo_records.addItem(display_text, rec_id)
            if target_id is not None and rec_id == target_id:
                selected_idx = idx

        self.combo_records.blockSignals(False)
        self.combo_records.setCurrentIndex(selected_idx)
        self._load_selected_record(self.combo_records.currentData())

    def _on_record_selection_changed(self, index):
        rec_id = self.combo_records.currentData()
        if rec_id is not None:
            self._load_selected_record(rec_id)

    def load_record_by_id(self, record_id: int):
        self.reload_records_selector(target_id=record_id)

    def _load_selected_record(self, record_id):
        if record_id is None:
            return
        r = self.storage_manager.get_record_by_id(record_id)
        if not r:
            return

        self.current_record_id = record_id
        self.input_id.setText(str(r.get("id", "")))
        self.input_user.setText(r.get("usuario", ""))

        date_obj = QDate.fromString(r.get("fecha", ""), "yyyy-MM-dd")
        if date_obj.isValid():
            self.input_date.setDate(date_obj)

        t_start = QTime.fromString(r.get("hora_inicio", ""), "HH:mm:ss")
        if not t_start.isValid():
            t_start = QTime.fromString(r.get("hora_inicio", ""), "HH:mm")
        if t_start.isValid():
            self.input_start.setTime(t_start)

        t_end = QTime.fromString(r.get("hora_fin", ""), "HH:mm:ss")
        if not t_end.isValid():
            t_end = QTime.fromString(r.get("hora_fin", ""), "HH:mm")
        if t_end.isValid():
            self.input_end.setTime(t_end)

        idx = self.combo_status.findText(r.get("estado", ""))
        if idx >= 0:
            self.combo_status.setCurrentIndex(idx)
        else:
            self.combo_status.setEditText(r.get("estado", ""))

        self.input_notes.setText(r.get("notas", ""))
        self._recalculate_duration()
        self.feedback_banner.setText("")

    def _recalculate_duration(self):
        t1 = self.input_start.time().toString("HH:mm:ss")
        t2 = self.input_end.time().toString("HH:mm:ss")
        hours = self.storage_manager.calculate_duration(t1, t2)
        self.val_duration.setText(f"{hours} horas")

    def _revert_current_record(self):
        if self.current_record_id:
            self._load_selected_record(self.current_record_id)

    def save_modifications(self):
        if self.current_record_id is None:
            QMessageBox.warning(self, t("msg_warning"), "No hay un registro cargado para editar.")
            return

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

        updated_data = {
            "usuario": user,
            "fecha": date_str,
            "hora_inicio": start_str,
            "hora_fin": end_str,
            "duracion_horas": dur,
            "estado": status,
            "notas": notes
        }

        ok, msg = self.storage_manager.update_record(self.current_record_id, updated_data)
        if ok:
            succ = t("record_updated_msg", id=self.current_record_id)
            self.feedback_banner.setText(succ)
            QMessageBox.information(self, t("msg_success"), f"{succ}\n{t('msg_saved_success')}")
            self.record_updated_signal.emit()
            self.reload_records_selector(target_id=self.current_record_id)
        else:
            QMessageBox.critical(self, t("msg_error"), f"Error al modificar registro: {msg}")

    def update_language_texts(self):
        self.title_lbl.setText(t("edit_title"))
        self.subtitle_lbl.setText(t("edit_subtitle"))
        self.tip_lbl.setText("Nota: " + t("edit_help_text"))
        self.lbl_select_prompt.setText(t("select_record_prompt"))
        self.btn_cancel.setText(t("btn_cancel_edit"))
        self.btn_save.setText(t("btn_save_changes"))
