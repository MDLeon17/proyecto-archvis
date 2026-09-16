# -*- coding: utf-8 -*-
"""
Generador dinámico de estilos QSS para temas Claro y Oscuro.
Calcula automáticamente el contraste de la tipografía y de la barra lateral
para evitar textos invisibles (ej. letras blancas sobre fondos claros).
"""

from PyQt6.QtGui import QColor

def is_color_dark(hex_str: str) -> bool:
    """Calcula si un color es oscuro utilizando luminancia relativa."""
    try:
        c = QColor(hex_str)
        if not c.isValid():
            return True
        luminance = 0.299 * c.red() + 0.587 * c.green() + 0.114 * c.blue()
        return luminance < 140
    except Exception:
        return True

def generate_stylesheet(theme: str = "oscuro", font_size: int = 11, sidebar_color: str = "", font_color: str = "") -> str:
    is_dark = (theme.lower() == "oscuro")

    # 1. Paleta de colores para el área de contenido principal
    if is_dark:
        bg_main = "#0f172a"
        bg_card = "#1e293b"
        bg_card_alt = "#273549"
        border_color = "#334155"
        input_bg = "#0f172a"
        input_border = "#475569"
        hover_bg = "#334155"
        table_row_alt = "#162032"
        table_selected = "#2563eb"
        text_secondary = "#94a3b8"

        # Tipografía en modo oscuro: si font_color es oscuro, forzar blanco para contraste
        if font_color and not is_color_dark(font_color):
            text_primary = font_color
        else:
            text_primary = "#f8fafc"
    else:
        bg_main = "#f8fafc"
        bg_card = "#ffffff"
        bg_card_alt = "#f1f5f9"
        border_color = "#cbd5e1"
        input_bg = "#ffffff"
        input_border = "#94a3b8"
        hover_bg = "#e2e8f0"
        table_row_alt = "#f1f5f9"
        table_selected = "#2563eb"
        text_secondary = "#475569"

        # Tipografía en modo claro: si font_color es claro o blanco, forzar oscuro para contraste
        if font_color and is_color_dark(font_color):
            text_primary = font_color
        else:
            text_primary = "#0f172a"

    # 2. Contraste de la barra lateral (Sidebar)
    if is_dark:
        # En modo oscuro: el fondo de la barra lateral debe ser oscuro.
        # Si no se configuró o es un color claro (remanente de modo claro), usar #1e293b.
        if not sidebar_color or not is_color_dark(sidebar_color):
            s_bg = "#1e293b"
        else:
            s_bg = sidebar_color

        # En modo oscuro, la tipografía del sidebar SIEMPRE debe ser blanca y nítida
        sidebar_text = "#ffffff"
        sidebar_text_muted = "rgba(255, 255, 255, 0.70)"
        sidebar_hover = "rgba(255, 255, 255, 0.15)"
        sidebar_active = "rgba(255, 255, 255, 0.28)"
        sidebar_border = "#334155"
        sidebar_accent = "#38bdf8"
    else:
        # En modo claro: el fondo de la barra lateral debe ser claro.
        # Si no se configuró o es un color oscuro (remanente de modo oscuro), usar #f1f5f9.
        if not sidebar_color or is_color_dark(sidebar_color):
            s_bg = "#f1f5f9"
        else:
            s_bg = sidebar_color

        # En modo claro, la tipografía del sidebar SIEMPRE debe ser oscura y nítida
        sidebar_text = "#0f172a"
        sidebar_text_muted = "rgba(15, 23, 42, 0.70)"
        sidebar_hover = "rgba(0, 0, 0, 0.08)"
        sidebar_active = "rgba(0, 0, 0, 0.16)"
        sidebar_border = "#cbd5e1"
        sidebar_accent = "#2563eb"

    qss = f"""
    * {{
        font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
        font-size: {font_size}pt;
        color: {text_primary};
    }}

    QMainWindow, QDialog {{
        background-color: {bg_main};
    }}

    QWidget#CentralWidget {{
        background-color: {bg_main};
    }}

    /* Barra Lateral (Sidebar) con contraste dinámico */
    QWidget#SidebarWidget {{
        background-color: {s_bg};
        border-right: 1px solid {sidebar_border};
    }}

    QWidget#SidebarWidget QLabel {{
        color: {sidebar_text};
    }}

    QWidget#SidebarWidget QLabel#SidebarUsername, QLabel#SidebarUsername {{
        color: {sidebar_text};
        font-weight: bold;
    }}

    QWidget#SidebarWidget QLabel#SidebarVersion, QLabel#SidebarVersion {{
        color: {sidebar_text_muted};
        font-size: 8.5pt;
    }}

    QWidget#SidebarWidget QPushButton#SidebarNavBtn, QPushButton#SidebarNavBtn {{
        background-color: transparent;
        color: {sidebar_text};
        text-align: left;
        padding: 10px 16px;
        border: none;
        border-radius: 8px;
        font-weight: 500;
        font-size: {font_size + 0.5}pt;
    }}

    QWidget#SidebarWidget QPushButton#SidebarNavBtn:hover, QPushButton#SidebarNavBtn:hover {{
        background-color: {sidebar_hover};
        color: {sidebar_text};
    }}

    QWidget#SidebarWidget QPushButton#SidebarNavBtn:checked, QPushButton#SidebarNavBtn:checked,
    QWidget#SidebarWidget QPushButton#SidebarNavBtn[active="true"], QPushButton#SidebarNavBtn[active="true"] {{
        background-color: {sidebar_active};
        color: {sidebar_text};
        font-weight: bold;
        border-left: 4px solid {sidebar_accent};
    }}

    /* Tarjetas / Contenedores */
    QFrame.card {{
        background-color: {bg_card};
        border: 1px solid {border_color};
        border-radius: 12px;
        padding: 16px;
    }}

    QFrame.card-alt {{
        background-color: {bg_card_alt};
        border: 1px solid {border_color};
        border-radius: 10px;
        padding: 12px;
    }}

    /* Controles de Entrada */
    QLineEdit, QComboBox, QSpinBox, QDateEdit, QTimeEdit, QTextEdit {{
        background-color: {input_bg};
        border: 1.5px solid {input_border};
        border-radius: 6px;
        padding: 8px 10px;
        color: {text_primary};
        selection-background-color: #2563eb;
    }}

    QLineEdit:focus, QComboBox:focus, QSpinBox:focus, QDateEdit:focus, QTimeEdit:focus, QTextEdit:focus {{
        border: 1.5px solid #3b82f6;
    }}

    QComboBox::drop-down, QDateEdit::drop-down, QTimeEdit::drop-down {{
        subcontrol-origin: padding;
        subcontrol-position: top right;
        width: 25px;
        border-left-width: 0px;
    }}

    /* Botones Estándar */
    QPushButton {{
        background-color: #2563eb;
        color: #ffffff;
        border: none;
        border-radius: 6px;
        padding: 8px 16px;
        font-weight: 600;
    }}

    QPushButton:hover {{
        background-color: #1d4ed8;
    }}

    QPushButton:pressed {{
        background-color: #1e40af;
    }}

    QPushButton:disabled {{
        background-color: #64748b;
        color: #cbd5e1;
    }}

    /* Variantes de Botones */
    QPushButton.btn-success {{
        background-color: #059669;
        color: #ffffff;
    }}
    QPushButton.btn-success:hover {{
        background-color: #047857;
    }}

    QPushButton.btn-danger {{
        background-color: #dc2626;
        color: #ffffff;
    }}
    QPushButton.btn-danger:hover {{
        background-color: #b91c1c;
    }}

    QPushButton.btn-warning {{
        background-color: #d97706;
        color: #ffffff;
    }}
    QPushButton.btn-warning:hover {{
        background-color: #b45309;
    }}

    QPushButton.btn-secondary {{
        background-color: {hover_bg};
        color: {text_primary};
        border: 1px solid {input_border};
    }}
    QPushButton.btn-secondary:hover {{
        background-color: {input_border};
    }}

    /* Tablas */
    QTableWidget {{
        background-color: {bg_card};
        alternate-background-color: {table_row_alt};
        gridline-color: {border_color};
        border: 1px solid {border_color};
        border-radius: 8px;
        color: {text_primary};
        selection-background-color: {table_selected};
        selection-color: #ffffff;
    }}

    QHeaderView::section {{
        background-color: {bg_card_alt};
        color: {text_secondary};
        font-weight: 600;
        padding: 8px;
        border: none;
        border-bottom: 2px solid {border_color};
    }}

    /* Scrollbars */
    QScrollBar:vertical {{
        background: {bg_main};
        width: 10px;
        margin: 0px;
    }}
    QScrollBar::handle:vertical {{
        background: #64748b;
        min-height: 20px;
        border-radius: 5px;
    }}
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
        height: 0px;
    }}

    /* Etiquetas de Texto */
    QLabel.heading-1 {{
        font-size: {font_size + 6}pt;
        font-weight: bold;
        color: {text_primary};
    }}

    QLabel.heading-2 {{
        font-size: {font_size + 3}pt;
        font-weight: bold;
        color: {text_primary};
    }}

    QLabel.subtitle {{
        font-size: {font_size - 0.5}pt;
        color: {text_secondary};
    }}
    """
    return qss
