# -*- coding: utf-8 -*-
"""
DeleteView: Eliminación de un dato con advertencia obligatoria de descuento de tiempo
y respaldo automático previo en .bak. Sin emojis.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QTableWidget, QTableWidgetItem, QHeaderView,
    QMessageBox
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QColor

from core.i18n import t

class DeleteView(QWidget):
    record_deleted_signal = pyqtSignal()

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
        main_layout.setSpacing(18)

        # Header Card
        header_card = QFrame()
        header_card.setProperty("class", "card")
        h_layout = QVBoxLayout(header_card)

        self.title_lbl = QLabel(t("delete_title"))
        self.title_lbl.setProperty("class", "heading-1")
        h_layout.addWidget(self.title_lbl)

        self.subtitle_lbl = QLabel(t("delete_subtitle"))
        self.subtitle_lbl.setProperty("class", "subtitle")
        h_layout.addWidget(self.subtitle_lbl)
        main_layout.addWidget(header_card)

        # Warning Card
        warn_card = QFrame()
        warn_card.setStyleSheet("background-color: #7f1d1d; border: 1.5px solid #ef4444; border-radius: 10px; padding: 14px;")
        w_layout = QVBoxLayout(warn_card)
        
        self.warn_header = QLabel(t("delete_warning_header"))
        self.warn_header.setStyleSheet("color: #fecaca; font-weight: bold; font-size: 11pt;")
        w_layout.addWidget(self.warn_header)

        self.warn_body = QLabel(t("delete_warning_body"))
        self.warn_body.setStyleSheet("color: #fee2e2; font-size: 9.5pt;")
        self.warn_body.setWordWrap(True)
        w_layout.addWidget(self.warn_body)

        main_layout.addWidget(warn_card)

        # Instructions Label
        self.lbl_instruction = QLabel("Seleccione de la siguiente lista el registro que desea eliminar:")
        self.lbl_instruction.setStyleSheet("font-weight: 600; color: #64748b;")
        main_layout.addWidget(self.lbl_instruction)

        # Table Widget
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            t("col_id"), t("col_user"), t("col_date"),
            t("col_start"), t("col_end"), t("col_duration"),
            t("col_status")
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.table.setAlternatingRowColors(True)
        self.table.verticalHeader().setVisible(False)
        self.table.itemSelectionChanged.connect(self._on_selection_changed)
        main_layout.addWidget(self.table)

        # Selected Record Preview & Action Card
        action_card = QFrame()
        action_card.setProperty("class", "card")
        act_layout = QHBoxLayout(action_card)
        act_layout.setContentsMargins(12, 12, 12, 12)

        self.lbl_selected_summary = QLabel("Ningún registro seleccionado.")
        self.lbl_selected_summary.setStyleSheet("font-weight: 600;")
        act_layout.addWidget(self.lbl_selected_summary, stretch=2)

        self.btn_delete = QPushButton(t("btn_confirm_delete"))
        self.btn_delete.setProperty("class", "btn-danger")
        self.btn_delete.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_delete.setEnabled(False)
        self.btn_delete.clicked.connect(self.prompt_delete_record)
        act_layout.addWidget(self.btn_delete)

        main_layout.addWidget(action_card)

    def reload_data(self):
        records, _ = self.storage_manager.load_records()
        self.all_records = records
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

            dur_item = QTableWidgetItem(r.get("duracion_horas", "0.00") + " h")
            dur_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            dur_item.setForeground(QColor("#dc2626"))

            status_item = QTableWidgetItem(r.get("estado", ""))
            status_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

            for col_idx, item in enumerate([
                id_item, user_item, date_item, start_item,
                end_item, dur_item, status_item
            ]):
                self.table.setItem(row_idx, col_idx, item)

        self.btn_delete.setEnabled(False)
        self.lbl_selected_summary.setText("Ningún registro seleccionado.")

    def select_record_by_id(self, record_id: int):
        self.reload_data()
        for row in range(self.table.rowCount()):
            item = self.table.item(row, 0)
            if item and item.data(Qt.ItemDataRole.UserRole) == record_id:
                self.table.selectRow(row)
                break

    def _on_selection_changed(self):
        row = self.table.currentRow()
        if row < 0:
            self.btn_delete.setEnabled(False)
            self.lbl_selected_summary.setText("Ningún registro seleccionado.")
            return

        item = self.table.item(row, 0)
        if item:
            rec_id = item.data(Qt.ItemDataRole.UserRole)
            record = self.storage_manager.get_record_by_id(rec_id)
            if record:
                self.btn_delete.setEnabled(True)
                self.lbl_selected_summary.setText(
                    f"Seleccionado: Registro #{rec_id} — {record.get('usuario')} | {record.get('fecha')} | "
                    f"{record.get('estado')} ({record.get('duracion_horas')} horas)"
                )

    def prompt_delete_record(self):
        row = self.table.currentRow()
        if row < 0:
            return

        item = self.table.item(row, 0)
        rec_id = item.data(Qt.ItemDataRole.UserRole)
        record = self.storage_manager.get_record_by_id(rec_id)
        if not record:
            return

        horas = record.get("duracion_horas", "0.00")
        estado = record.get("estado", "")

        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Icon.Warning)
        msg_box.setWindowTitle(t("delete_confirm_title"))
        
        warning_text = (
            f"ATENCIÓN: ESTE TIEMPO SE LE DESCONTARÁ\n\n"
            f"Está a punto de eliminar el registro #{rec_id} ({horas} horas en estado '{estado}').\n\n"
            f"Si elimina este registro de tiempo, ese tiempo se le descontará de su jornada laboral registrada.\n\n"
            f"El sistema guardará una copia de seguridad automática (.bak) antes de eliminar.\n\n"
            f"Desea continuar?"
        )
        msg_box.setText(warning_text)
        btn_confirm = msg_box.addButton("Sí, descontar y eliminar", QMessageBox.ButtonRole.YesRole)
        btn_cancel = msg_box.addButton("Cancelar", QMessageBox.ButtonRole.RejectRole)
        msg_box.setDefaultButton(btn_cancel)

        msg_box.exec()

        if msg_box.clickedButton() == btn_confirm:
            ok, err = self.storage_manager.delete_record(rec_id)
            if ok:
                succ = t("record_deleted_msg", id=rec_id)
                QMessageBox.information(
                    self, t("msg_success"),
                    f"{succ}\n\nEl tiempo ({horas} h) ha sido descontado. Se generó respaldo .bak de recuperación."
                )
                self.record_deleted_signal.emit()
                self.reload_data()
            else:
                QMessageBox.critical(self, t("msg_error"), f"No se pudo eliminar el registro: {err}")

    def update_language_texts(self):
        self.title_lbl.setText(t("delete_title"))
        self.subtitle_lbl.setText(t("delete_subtitle"))
        self.warn_header.setText(t("delete_warning_header"))
        self.warn_body.setText(t("delete_warning_body"))
        self.btn_delete.setText(t("btn_confirm_delete"))
        self.table.setHorizontalHeaderLabels([
            t("col_id"), t("col_user"), t("col_date"),
            t("col_start"), t("col_end"), t("col_duration"),
            t("col_status")
        ])
