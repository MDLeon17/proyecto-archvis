# -*- coding: utf-8 -*-
"""
ReadView: Consulta y lectura del archivo CSV sin emojis.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QLineEdit, QComboBox, QTableWidget, QTableWidgetItem,
    QHeaderView, QMessageBox, QDialog, QFormLayout
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QColor

from core.i18n import t

class RecordDetailDialog(QDialog):
    def __init__(self, record_data, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Detalle del Registro #{record_data.get('id', '')}")
        self.setMinimumWidth(460)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(14)

        title = QLabel(f"Detalle Completo • Registro #{record_data.get('id', '')}")
        title.setProperty("class", "heading-2")
        layout.addWidget(title)

        form_frame = QFrame()
        form_frame.setProperty("class", "card")
        form = QFormLayout(form_frame)
        form.setSpacing(10)

        for key, label in [
            ("id", "ID:"),
            ("usuario", t("col_user") + ":"),
            ("fecha", t("col_date") + ":"),
            ("hora_inicio", t("col_start") + ":"),
            ("hora_fin", t("col_end") + ":"),
            ("duracion_horas", t("col_duration") + ":"),
            ("estado", t("col_status") + ":"),
            ("notas", t("col_notes") + ":")
        ]:
            val_lbl = QLabel(str(record_data.get(key, "")))
            val_lbl.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
            if key == "estado":
                val_lbl.setStyleSheet("font-weight: bold; color: #0284c7;")
            elif key == "duracion_horas":
                val_lbl.setStyleSheet("font-weight: bold; color: #059669;")
            form.addRow(QLabel(f"<b>{label}</b>"), val_lbl)

        layout.addWidget(form_frame)

        btn_close = QPushButton("Cerrar")
        btn_close.clicked.connect(self.accept)
        layout.addWidget(btn_close)

class ReadView(QWidget):
    edit_record_requested = pyqtSignal(int)
    delete_record_requested = pyqtSignal(int)

    def __init__(self, storage_manager, config_manager, parent=None):
        super().__init__(parent)
        self.storage_manager = storage_manager
        self.config_manager = config_manager
        self.all_records = []
        self._init_ui()
        self.reload_data()

    def _init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(24, 24, 24, 24)
        main_layout.setSpacing(16)

        # Header Card
        header_card = QFrame()
        header_card.setProperty("class", "card")
        h_layout = QVBoxLayout(header_card)

        self.title_lbl = QLabel(t("read_title"))
        self.title_lbl.setProperty("class", "heading-1")
        h_layout.addWidget(self.title_lbl)

        self.subtitle_lbl = QLabel(t("read_subtitle"))
        self.subtitle_lbl.setProperty("class", "subtitle")
        h_layout.addWidget(self.subtitle_lbl)
        main_layout.addWidget(header_card)

        # Stats Cards Layout
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(16)

        self.card_total = self._create_stat_card(t("total_records"), "0", "#2563eb")
        self.card_hours = self._create_stat_card(t("total_hours"), "0.00 h", "#059669")
        self.card_ready = self._create_stat_card("Ready", "0.00 h", "#0d9488")
        self.card_lunch = self._create_stat_card("Lunch", "0.00 h", "#d97706")
        self.card_break = self._create_stat_card("Break", "0.00 h", "#0891b2")

        stats_layout.addWidget(self.card_total)
        stats_layout.addWidget(self.card_hours)
        stats_layout.addWidget(self.card_ready)
        stats_layout.addWidget(self.card_lunch)
        stats_layout.addWidget(self.card_break)
        main_layout.addLayout(stats_layout)

        # Filter Card
        filter_card = QFrame()
        filter_card.setProperty("class", "card")
        f_layout = QHBoxLayout(filter_card)
        f_layout.setSpacing(12)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText(t("search_placeholder"))
        self.search_input.textChanged.connect(self.apply_filter)
        f_layout.addWidget(self.search_input, stretch=2)

        self.status_filter_combo = QComboBox()
        self.status_filter_combo.addItem(t("filter_all_status"), "all")
        for st in ["Ready", "Lunch", "Break", "Meeting", "Training", "Clock In", "Clock Out"]:
            self.status_filter_combo.addItem(st, st)
        self.status_filter_combo.currentIndexChanged.connect(self.apply_filter)
        f_layout.addWidget(self.status_filter_combo, stretch=1)

        self.btn_refresh = QPushButton(t("btn_refresh"))
        self.btn_refresh.setProperty("class", "btn-secondary")
        self.btn_refresh.clicked.connect(self.reload_data)
        f_layout.addWidget(self.btn_refresh)

        main_layout.addWidget(filter_card)

        # Table Widget
        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels([
            t("col_id"), t("col_user"), t("col_date"),
            t("col_start"), t("col_end"), t("col_duration"),
            t("col_status"), t("col_notes")
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.table.setAlternatingRowColors(True)
        self.table.verticalHeader().setVisible(False)
        self.table.doubleClicked.connect(self.view_detail)
        main_layout.addWidget(self.table)

        # Bottom Actions Card
        bottom_card = QFrame()
        bottom_card.setProperty("class", "card-alt")
        b_layout = QHBoxLayout(bottom_card)
        b_layout.setContentsMargins(8, 8, 8, 8)

        self.lbl_selected_info = QLabel("Seleccione una fila para realizar acciones específicas.")
        self.lbl_selected_info.setStyleSheet("color: #64748b;")
        b_layout.addWidget(self.lbl_selected_info)
        b_layout.addStretch()

        self.btn_view_detail = QPushButton(t("btn_view_detail"))
        self.btn_view_detail.setProperty("class", "btn-secondary")
        self.btn_view_detail.clicked.connect(self.view_detail)
        b_layout.addWidget(self.btn_view_detail)

        self.btn_edit_selected = QPushButton(t("btn_go_edit"))
        self.btn_edit_selected.clicked.connect(self._on_edit_clicked)
        b_layout.addWidget(self.btn_edit_selected)

        self.btn_delete_selected = QPushButton(t("nav_delete"))
        self.btn_delete_selected.setProperty("class", "btn-danger")
        self.btn_delete_selected.clicked.connect(self._on_delete_clicked)
        b_layout.addWidget(self.btn_delete_selected)

        main_layout.addWidget(bottom_card)

    def _create_stat_card(self, title: str, initial_value: str, color_hex: str) -> QFrame:
        card = QFrame()
        card.setProperty("class", "card")
        layout = QVBoxLayout(card)
        layout.setContentsMargins(12, 10, 12, 10)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title_lbl = QLabel(title)
        title_lbl.setStyleSheet("color: #64748b; font-size: 8.5pt; font-weight: 600;")
        layout.addWidget(title_lbl)

        val_lbl = QLabel(initial_value)
        val_lbl.setStyleSheet(f"color: {color_hex}; font-size: 14pt; font-weight: bold;")
        layout.addWidget(val_lbl)
        card.value_label = val_lbl
        card.title_label = title_lbl
        return card

    def reload_data(self):
        records, err = self.storage_manager.load_records()
        if err:
            QMessageBox.warning(self, t("msg_warning"), err)
        self.all_records = records
        self.apply_filter()
        self._update_stats()

    def _update_stats(self):
        total_rec = len(self.all_records)
        total_hours = 0.0
        ready_hours = 0.0
        lunch_hours = 0.0
        break_hours = 0.0

        for r in self.all_records:
            try:
                dur = float(r.get("duracion_horas", 0.0))
            except ValueError:
                dur = 0.0

            total_hours += dur
            st = str(r.get("estado", "")).lower()
            if "ready" in st:
                ready_hours += dur
            elif "lunch" in st:
                lunch_hours += dur
            elif "break" in st:
                break_hours += dur

        self.card_total.value_label.setText(str(total_rec))
        self.card_hours.value_label.setText(f"{total_hours:.2f} h")
        self.card_ready.value_label.setText(f"{ready_hours:.2f} h")
        self.card_lunch.value_label.setText(f"{lunch_hours:.2f} h")
        self.card_break.value_label.setText(f"{break_hours:.2f} h")

    def apply_filter(self):
        query = self.search_input.text().strip().lower()
        selected_status = self.status_filter_combo.currentData()

        filtered = []
        for r in self.all_records:
            if selected_status != "all" and r.get("estado", "") != selected_status:
                continue

            if query:
                match_user = query in str(r.get("usuario", "")).lower()
                match_status = query in str(r.get("estado", "")).lower()
                match_notes = query in str(r.get("notas", "")).lower()
                match_date = query in str(r.get("fecha", "")).lower()
                if not (match_user or match_status or match_notes or match_date):
                    continue

            filtered.append(r)

        self._populate_table(filtered)

    def _populate_table(self, records):
        self.table.setRowCount(len(records))
        for row_idx, r in enumerate(records):
            id_item = QTableWidgetItem(str(r.get("id", "")))
            id_item.setData(Qt.ItemDataRole.UserRole, r.get("id"))
            id_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

            user_item = QTableWidgetItem(r.get("usuario", ""))
            date_item = QTableWidgetItem(r.get("fecha", ""))
            date_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

            start_item = QTableWidgetItem(r.get("hora_inicio", ""))
            start_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

            end_item = QTableWidgetItem(r.get("hora_fin", ""))
            end_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

            dur_item = QTableWidgetItem(r.get("duracion_horas", "0.00"))
            dur_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            dur_item.setForeground(QColor("#059669"))

            status_item = QTableWidgetItem(r.get("estado", ""))
            status_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            
            st_lower = str(r.get("estado", "")).lower()
            if "ready" in st_lower or "clock in" in st_lower:
                status_item.setForeground(QColor("#059669"))
            elif "lunch" in st_lower:
                status_item.setForeground(QColor("#d97706"))
            elif "break" in st_lower:
                status_item.setForeground(QColor("#0891b2"))
            elif "clock out" in st_lower:
                status_item.setForeground(QColor("#dc2626"))

            notes_item = QTableWidgetItem(r.get("notas", ""))

            for col_idx, item in enumerate([
                id_item, user_item, date_item, start_item,
                end_item, dur_item, status_item, notes_item
            ]):
                self.table.setItem(row_idx, col_idx, item)

    def get_selected_record_id(self):
        row = self.table.currentRow()
        if row < 0:
            return None
        item = self.table.item(row, 0)
        if item:
            return item.data(Qt.ItemDataRole.UserRole)
        return None

    def view_detail(self):
        rec_id = self.get_selected_record_id()
        if rec_id is None:
            QMessageBox.information(self, t("msg_info"), "Por favor, seleccione un registro de la tabla.")
            return
        record = self.storage_manager.get_record_by_id(rec_id)
        if record:
            dlg = RecordDetailDialog(record, self)
            dlg.exec()

    def _on_edit_clicked(self):
        rec_id = self.get_selected_record_id()
        if rec_id is None:
            QMessageBox.information(self, t("msg_info"), "Por favor, seleccione el registro que desea editar.")
            return
        self.edit_record_requested.emit(rec_id)

    def _on_delete_clicked(self):
        rec_id = self.get_selected_record_id()
        if rec_id is None:
            QMessageBox.information(self, t("msg_info"), "Por favor, seleccione el registro que desea eliminar.")
            return
        self.delete_record_requested.emit(rec_id)

    def update_language_texts(self):
        self.title_lbl.setText(t("read_title"))
        self.subtitle_lbl.setText(t("read_subtitle"))
        self.search_input.setPlaceholderText(t("search_placeholder"))
        self.btn_refresh.setText(t("btn_refresh"))
        self.btn_view_detail.setText(t("btn_view_detail"))
        self.btn_edit_selected.setText(t("btn_go_edit"))
        self.btn_delete_selected.setText(t("nav_delete"))
        self.card_total.title_label.setText(t("total_records"))
        self.card_hours.title_label.setText(t("total_hours"))
        self.table.setHorizontalHeaderLabels([
            t("col_id"), t("col_user"), t("col_date"),
            t("col_start"), t("col_end"), t("col_duration"),
            t("col_status"), t("col_notes")
        ])
