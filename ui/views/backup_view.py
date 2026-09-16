# -*- coding: utf-8 -*-
"""
BackupView: Panel centralizado para auditar y restaurar copias de seguridad (.bak).
Sin emojis.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QMessageBox
)
from PyQt6.QtCore import Qt, pyqtSignal

from core.i18n import t

class BackupView(QWidget):
    records_restored_signal = pyqtSignal()
    settings_restored_signal = pyqtSignal()

    def __init__(self, storage_manager, config_manager, parent=None):
        super().__init__(parent)
        self.storage_manager = storage_manager
        self.config_manager = config_manager
        self._init_ui()
        self.refresh_status()

    def _init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(24, 24, 24, 24)
        main_layout.setSpacing(20)

        # Header Card
        header_card = QFrame()
        header_card.setProperty("class", "card")
        h_layout = QVBoxLayout(header_card)

        self.title_lbl = QLabel(t("backup_title"))
        self.title_lbl.setProperty("class", "heading-1")
        h_layout.addWidget(self.title_lbl)

        self.subtitle_lbl = QLabel(t("backup_subtitle"))
        self.subtitle_lbl.setProperty("class", "subtitle")
        h_layout.addWidget(self.subtitle_lbl)
        main_layout.addWidget(header_card)

        # 1. Respaldo de Registros CSV Card
        csv_card = QFrame()
        csv_card.setProperty("class", "card")
        c_layout = QVBoxLayout(csv_card)
        c_layout.setSpacing(12)

        csv_title = QLabel("Registros Laborales (registros.csv.bak)")
        csv_title.setProperty("class", "heading-2")
        c_layout.addWidget(csv_title)

        self.lbl_csv_status = QLabel("")
        c_layout.addWidget(self.lbl_csv_status)

        csv_btns = QHBoxLayout()
        self.btn_restore_csv = QPushButton(t("btn_restore_csv_bak"))
        self.btn_restore_csv.setProperty("class", "btn-warning")
        self.btn_restore_csv.clicked.connect(self.restore_csv_backup)
        csv_btns.addWidget(self.btn_restore_csv)

        self.btn_manual_csv_bak = QPushButton(t("btn_create_manual_bak"))
        self.btn_manual_csv_bak.setProperty("class", "btn-secondary")
        self.btn_manual_csv_bak.clicked.connect(self.create_manual_csv_backup)
        csv_btns.addWidget(self.btn_manual_csv_bak)

        csv_btns.addStretch()
        c_layout.addLayout(csv_btns)
        main_layout.addWidget(csv_card)

        # 2. Respaldo de Configuración Card
        cfg_card = QFrame()
        cfg_card.setProperty("class", "card")
        cfg_layout = QVBoxLayout(cfg_card)
        cfg_layout.setSpacing(12)

        cfg_title = QLabel("Archivo de Configuración (config.bak)")
        cfg_title.setProperty("class", "heading-2")
        cfg_layout.addWidget(cfg_title)

        self.lbl_cfg_status = QLabel("")
        cfg_layout.addWidget(self.lbl_cfg_status)

        cfg_btns = QHBoxLayout()
        self.btn_restore_cfg = QPushButton(t("btn_restore_config_bak"))
        self.btn_restore_cfg.setProperty("class", "btn-warning")
        self.btn_restore_cfg.clicked.connect(self.restore_config_backup)
        cfg_btns.addWidget(self.btn_restore_cfg)

        cfg_btns.addStretch()
        cfg_layout.addLayout(cfg_btns)
        main_layout.addWidget(cfg_card)

        # Explanatory Card
        expl_card = QFrame()
        expl_card.setProperty("class", "card-alt")
        e_layout = QVBoxLayout(expl_card)
        expl_lbl = QLabel(
            "<b>Información sobre el sistema de copias .bak:</b><br>"
            "Cada vez que agrega, edita, cambia de estado o elimina un registro en el archivo CSV, "
            "o cuando modifica las opciones de configuración, el sistema realiza automáticamente una copia "
            "del archivo anterior con extensión <code>.bak</code> antes de aplicar los cambios de manera atómica. "
            "Esto le garantiza que siempre podrá revertir a la versión previa si se equivoca."
        )
        expl_lbl.setStyleSheet("color: #64748b; font-size: 9pt;")
        expl_lbl.setWordWrap(True)
        e_layout.addWidget(expl_lbl)
        main_layout.addWidget(expl_card)

        main_layout.addStretch()

    def refresh_status(self):
        csv_info = self.storage_manager.get_backup_info()
        if csv_info["exists"]:
            self.lbl_csv_status.setText(
                t("backup_available", date=csv_info["date"], size=csv_info["size"])
            )
            self.lbl_csv_status.setStyleSheet("color: #059669; font-weight: 500;")
            self.btn_restore_csv.setEnabled(True)
        else:
            self.lbl_csv_status.setText(t("backup_not_available"))
            self.lbl_csv_status.setStyleSheet("color: #64748b;")
            self.btn_restore_csv.setEnabled(False)

        cfg_info = self.config_manager.get_backup_info()
        if cfg_info["exists"]:
            self.lbl_cfg_status.setText(
                t("backup_available", date=cfg_info["date"], size=cfg_info["size"])
            )
            self.lbl_cfg_status.setStyleSheet("color: #059669; font-weight: 500;")
            self.btn_restore_cfg.setEnabled(True)
        else:
            self.lbl_cfg_status.setText(t("backup_not_available"))
            self.lbl_cfg_status.setStyleSheet("color: #64748b;")
            self.btn_restore_cfg.setEnabled(False)

    def restore_csv_backup(self):
        confirm = QMessageBox.question(
            self, t("msg_warning"),
            t("msg_restore_confirm") + "\n\nSe restaurará el archivo registros.csv a su versión .bak previa.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if confirm == QMessageBox.StandardButton.Yes:
            ok, msg = self.storage_manager.restore_backup()
            if ok:
                QMessageBox.information(self, t("msg_success"), t("msg_restore_success"))
                self.records_restored_signal.emit()
                self.refresh_status()
            else:
                QMessageBox.critical(self, t("msg_error"), msg)

    def create_manual_csv_backup(self):
        ok, msg = self.storage_manager.create_manual_backup()
        if ok:
            QMessageBox.information(self, t("msg_success"), msg)
            self.refresh_status()
        else:
            QMessageBox.warning(self, t("msg_error"), msg)

    def restore_config_backup(self):
        confirm = QMessageBox.question(
            self, t("msg_warning"),
            t("msg_restore_confirm") + "\n\nSe restaurará el archivo config.json a su versión .bak previa.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if confirm == QMessageBox.StandardButton.Yes:
            ok, msg = self.config_manager.restore_backup()
            if ok:
                QMessageBox.information(self, t("msg_success"), t("msg_restore_success"))
                self.settings_restored_signal.emit()
                self.refresh_status()
            else:
                QMessageBox.critical(self, t("msg_error"), msg)

    def update_language_texts(self):
        self.title_lbl.setText(t("backup_title"))
        self.subtitle_lbl.setText(t("backup_subtitle"))
        self.btn_restore_csv.setText(t("btn_restore_csv_bak"))
        self.btn_manual_csv_bak.setText(t("btn_create_manual_bak"))
        self.btn_restore_cfg.setText(t("btn_restore_config_bak"))
        self.refresh_status()
