# -*- coding: utf-8 -*-
"""
ClockView: Panel de marcado de jornada (Clock In/Out) y cambio de estados en tiempo real.
Sin emojis.
"""

import datetime
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QTextEdit, QMessageBox, QGridLayout
)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QFont

from core.i18n import t

class ClockView(QWidget):
    state_changed_signal = pyqtSignal(str)
    records_updated_signal = pyqtSignal()

    def __init__(self, storage_manager, config_manager, parent=None):
        super().__init__(parent)
        self.storage_manager = storage_manager
        self.config_manager = config_manager
        
        self.current_state = "status_offline"
        self.state_start_time = None
        self.active_session_notes = ""

        self._init_ui()

        self.clock_timer = QTimer(self)
        self.clock_timer.timeout.connect(self._update_clock)
        self.clock_timer.start(1000)

    def _init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(24, 24, 24, 24)
        main_layout.setSpacing(20)

        # Header Card
        header_card = QFrame()
        header_card.setProperty("class", "card")
        h_layout = QVBoxLayout(header_card)
        
        self.title_lbl = QLabel(t("clock_title"))
        self.title_lbl.setProperty("class", "heading-1")
        h_layout.addWidget(self.title_lbl)

        self.subtitle_lbl = QLabel(t("clock_subtitle"))
        self.subtitle_lbl.setProperty("class", "subtitle")
        h_layout.addWidget(self.subtitle_lbl)
        main_layout.addWidget(header_card)

        # Dashboard Grid: Reloj y Estado Actual
        dash_layout = QHBoxLayout()
        dash_layout.setSpacing(20)

        # Reloj Card
        clock_card = QFrame()
        clock_card.setProperty("class", "card")
        c_layout = QVBoxLayout(clock_card)
        c_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.lbl_clock_header = QLabel(t("current_time"))
        self.lbl_clock_header.setProperty("class", "subtitle")
        c_layout.addWidget(self.lbl_clock_header)

        self.time_display = QLabel("00:00:00")
        t_font = QFont("Consolas", 32, QFont.Weight.Bold)
        self.time_display.setFont(t_font)
        self.time_display.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.time_display.setStyleSheet("color: #2563eb; padding: 10px;")
        c_layout.addWidget(self.time_display)

        self.date_display = QLabel("YYYY-MM-DD")
        self.date_display.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.date_display.setStyleSheet("color: #64748b; font-weight: 500;")
        c_layout.addWidget(self.date_display)
        dash_layout.addWidget(clock_card)

        # Estado Actual Card
        state_card = QFrame()
        state_card.setProperty("class", "card")
        s_layout = QVBoxLayout(state_card)
        s_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.lbl_state_header = QLabel(t("current_state"))
        self.lbl_state_header.setProperty("class", "subtitle")
        s_layout.addWidget(self.lbl_state_header)

        self.state_chip = QLabel(t("status_offline"))
        self.state_chip.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.state_chip.setStyleSheet(
            "background-color: #64748b; color: #ffffff; border-radius: 12px; "
            "padding: 8px 24px; font-weight: bold; font-size: 15pt;"
        )
        s_layout.addWidget(self.state_chip)

        self.lbl_time_in_state = QLabel(t("time_in_state") + " 00:00:00")
        self.lbl_time_in_state.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_time_in_state.setStyleSheet("color: #64748b; font-size: 11pt; font-weight: 600; margin-top: 6px;")
        s_layout.addWidget(self.lbl_time_in_state)

        dash_layout.addWidget(state_card)
        main_layout.addLayout(dash_layout)

        # Acciones de Estado Card
        actions_card = QFrame()
        actions_card.setProperty("class", "card")
        act_layout = QVBoxLayout(actions_card)
        act_layout.setSpacing(14)

        act_title = QLabel("Acciones de Control de Estado")
        act_title.setProperty("class", "heading-2")
        act_layout.addWidget(act_title)

        grid = QGridLayout()
        grid.setSpacing(12)

        self.btn_clock_in = QPushButton(t("btn_clock_in"))
        self.btn_clock_in.setProperty("class", "btn-success")
        self.btn_clock_in.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_clock_in.clicked.connect(lambda: self.switch_state("Clock In"))
        grid.addWidget(self.btn_clock_in, 0, 0)

        self.btn_ready = QPushButton(t("btn_ready"))
        self.btn_ready.setProperty("class", "btn-success")
        self.btn_ready.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_ready.clicked.connect(lambda: self.switch_state("Ready"))
        grid.addWidget(self.btn_ready, 0, 1)

        self.btn_lunch = QPushButton(t("btn_lunch"))
        self.btn_lunch.setProperty("class", "btn-warning")
        self.btn_lunch.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_lunch.clicked.connect(lambda: self.switch_state("Lunch"))
        grid.addWidget(self.btn_lunch, 0, 2)

        self.btn_break = QPushButton(t("btn_break"))
        self.btn_break.setStyleSheet("background-color: #0891b2; color: #ffffff;")
        self.btn_break.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_break.clicked.connect(lambda: self.switch_state("Break"))
        grid.addWidget(self.btn_break, 1, 0)

        self.btn_meeting = QPushButton(t("btn_meeting"))
        self.btn_meeting.setStyleSheet("background-color: #7c3aed; color: #ffffff;")
        self.btn_meeting.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_meeting.clicked.connect(lambda: self.switch_state("Meeting"))
        grid.addWidget(self.btn_meeting, 1, 1)

        self.btn_training = QPushButton(t("btn_training"))
        self.btn_training.setStyleSheet("background-color: #4f46e5; color: #ffffff;")
        self.btn_training.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_training.clicked.connect(lambda: self.switch_state("Training"))
        grid.addWidget(self.btn_training, 1, 2)

        self.btn_clock_out = QPushButton(t("btn_clock_out"))
        self.btn_clock_out.setProperty("class", "btn-danger")
        self.btn_clock_out.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_clock_out.clicked.connect(lambda: self.switch_state("Clock Out"))
        grid.addWidget(self.btn_clock_out, 2, 0, 1, 3)

        act_layout.addLayout(grid)

        # Notes
        self.notes_input = QTextEdit()
        self.notes_input.setPlaceholderText(t("notes_placeholder"))
        self.notes_input.setMaximumHeight(60)
        act_layout.addWidget(self.notes_input)

        main_layout.addWidget(actions_card)

        # Feedback banner
        self.feedback_banner = QLabel("")
        self.feedback_banner.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.feedback_banner.setStyleSheet("color: #059669; font-weight: bold;")
        main_layout.addWidget(self.feedback_banner)

        main_layout.addStretch()
        self._update_clock()

    def _update_clock(self):
        now = datetime.datetime.now()
        self.time_display.setText(now.strftime("%H:%M:%S"))
        self.date_display.setText(now.strftime("%Y-%m-%d (%A)"))

        if self.state_start_time and self.current_state != "status_offline":
            elapsed = now - self.state_start_time
            total_sec = int(elapsed.total_seconds())
            hours = total_sec // 3600
            minutes = (total_sec % 3600) // 60
            seconds = total_sec % 60
            self.lbl_time_in_state.setText(
                f"{t('time_in_state')} {hours:02d}:{minutes:02d}:{seconds:02d}"
            )
        else:
            self.lbl_time_in_state.setText(t("time_in_state") + " 00:00:00")

    def switch_state(self, new_state: str):
        now = datetime.datetime.now()
        user_name = self.config_manager.get("nombre_usuario", "Operador")
        notes = self.notes_input.toPlainText().strip()

        if self.current_state != "status_offline" and self.state_start_time is not None:
            hora_inicio = self.state_start_time.strftime("%H:%M:%S")
            hora_fin = now.strftime("%H:%M:%S")
            fecha = self.state_start_time.strftime("%Y-%m-%d")
            
            dur_horas = self.storage_manager.calculate_duration(hora_inicio, hora_fin)
            
            rec = {
                "usuario": user_name,
                "fecha": fecha,
                "hora_inicio": hora_inicio,
                "hora_fin": hora_fin,
                "duracion_horas": dur_horas,
                "estado": self.current_state,
                "notas": notes if notes else f"Sesión {self.current_state}"
            }
            ok, msg, rec_id = self.storage_manager.add_record(rec)
            if ok:
                self.records_updated_signal.emit()
                self.feedback_banner.setText(
                    f"Sesión previa ({self.current_state}) guardada en CSV (#{rec_id}, {dur_horas} h). Respaldo .bak actualizado."
                )
            else:
                QMessageBox.critical(self, t("msg_error"), f"No se pudo guardar el registro: {msg}")

        if new_state == "Clock Out":
            self.current_state = "status_offline"
            self.state_start_time = None
            self.state_chip.setText(t("status_clock_out"))
            self.state_chip.setStyleSheet(
                "background-color: #dc2626; color: #ffffff; border-radius: 12px; "
                "padding: 8px 24px; font-weight: bold; font-size: 15pt;"
            )
            self.state_changed_signal.emit("status_offline")
        else:
            self.current_state = new_state
            self.state_start_time = now
            colors = {
                "Clock In": ("#059669", t("status_clock_in")),
                "Ready": ("#059669", t("status_ready")),
                "Lunch": ("#d97706", t("status_lunch")),
                "Break": ("#0891b2", t("status_break")),
                "Meeting": ("#7c3aed", t("status_meeting")),
                "Training": ("#4f46e5", t("status_training")),
            }
            bg_col, title_txt = colors.get(new_state, ("#2563eb", new_state))
            self.state_chip.setText(title_txt)
            self.state_chip.setStyleSheet(
                f"background-color: {bg_col}; color: #ffffff; border-radius: 12px; "
                f"padding: 8px 24px; font-weight: bold; font-size: 15pt;"
            )
            self.state_changed_signal.emit(new_state)

        self.notes_input.clear()

    def update_language_texts(self):
        self.title_lbl.setText(t("clock_title"))
        self.subtitle_lbl.setText(t("clock_subtitle"))
        self.lbl_clock_header.setText(t("current_time"))
        self.lbl_state_header.setText(t("current_state"))
        self.btn_clock_in.setText(t("btn_clock_in"))
        self.btn_ready.setText(t("btn_ready"))
        self.btn_lunch.setText(t("btn_lunch"))
        self.btn_break.setText(t("btn_break"))
        self.btn_meeting.setText(t("btn_meeting"))
        self.btn_training.setText(t("btn_training"))
        self.btn_clock_out.setText(t("btn_clock_out"))
        self.notes_input.setPlaceholderText(t("notes_placeholder"))
