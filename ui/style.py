# -*- coding: utf-8 -*-
"""
Generador dinámico de estilos QSS para temas Claro y Oscuro.
Permite personalizar el color de botones, color de barra lateral,
color de letra y tamaño de fuente con contraste garantizado.
"""

from PyQt6.QtGui import QColor

def is_color_dark(hex_str: str) -> bool:
    """Calcula si un color es oscuro utilizando luminancia relativa estándar."""
    try:
        c = QColor(hex_str)
        if not c.isValid():
            return True
        luminance = 0.299 * c.red() + 0.587 * c.green() + 0.114 * c.blue()
        return luminance < 140
    except Exception:
        return True

def adjust_brightness(hex_str: str, factor: float) -> str:
    """Ajusta el brillo de un color hexadecimal por un factor multiplicador."""
    try:
        c = QColor(hex_str)
        if not c.isValid():
            return hex_str
        r = min(255, max(0, int(c.red() * factor)))
        g = min(255, max(0, int(c.green() * factor)))
        b = min(255, max(0, int(c.blue() * factor)))
        return QColor(r, g, b).name()
    except Exception:
        return hex_str

def generate_stylesheet(
    theme: str = "oscuro",
    font_size: int = 11,
    sidebar_color: str = "",
    font_color: str = "",
    button_color: str = "#2563eb"
) -> str:
    is_dark = (theme.lower() == "oscuro")

    # 1. Normalizar color de botones
    if not button_color or not QColor(button_color).isValid():
        button_color = "#2563eb"

    btn_is_dark = is_color_dark(button_color)
    btn_text = "#ffffff" if btn_is_dark else "#0f172a"
    btn_hover = adjust_brightness(button_color, 0.88 if btn_is_dark else 1.12)
    btn_pressed = adjust_brightness(button_color, 0.75 if btn_is_dark else 1.25)

    # 2. Paleta de colores para el área de contenido principal
    if is_dark:
        bg_main = "#0f172a"
        bg_card = "#1e293b"
        bg_card_alt = "#273549"
        border_color = "#334155"
        input_bg = "#0f172a"
        input_border = "#475569"
        hover_bg = "#334155"
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
        text_secondary = "#64748b"

        # Tipografía en modo claro: si font_color es claro o blanco, forzar oscuro para contraste
        if font_color and is_color_dark(font_color):
            text_primary = font_color
        else:
            text_primary = "#0f172a"

    # 3. Contraste de la barra lateral (Sidebar)
    if is_dark:
        if not sidebar_color or not is_color_dark(sidebar_color):
            s_bg = "#1e293b"
        else:
            s_bg = sidebar_color

        sidebar_text = "#ffffff"
        sidebar_text_muted = "rgba(255, 255, 255, 0.70)"
        sidebar_hover = "rgba(255, 255, 255, 0.12)"
        sidebar_active = "rgba(255, 255, 255, 0.22)"
        sidebar_border = "#334155"
        sidebar_accent = button_color
    else:
        if not sidebar_color or is_color_dark(sidebar_color):
            s_bg = "#f1f5f9"
        else:
            s_bg = sidebar_color

        sidebar_text = "#0f172a"
        sidebar_text_muted = "rgba(15, 23, 42, 0.70)"
        sidebar_hover = "rgba(0, 0, 0, 0.08)"
        sidebar_active = "rgba(0, 0, 0, 0.16)"
        sidebar_border = "#cbd5e1"
        sidebar_accent = button_color

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
        padding: 12px 18px;
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

    /* Tarjetas y Paneles */
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
        padding: 14px;
    }}

    /* Controles de Entrada */
    QLineEdit, QComboBox, QSpinBox, QTextEdit {{
        background-color: {input_bg};
        border: 1.5px solid {input_border};
        border-radius: 8px;
        padding: 8px 12px;
        color: {text_primary};
        selection-background-color: {button_color};
    }}

    QLineEdit:focus, QComboBox:focus, QSpinBox:focus, QTextEdit:focus {{
        border: 1.5px solid {button_color};
    }}

    QComboBox::drop-down {{
        subcontrol-origin: padding;
        subcontrol-position: top right;
        width: 25px;
        border-left-width: 0px;
    }}

    /* Botones Estándar - Personalizados con Color de Botones */
    QPushButton {{
        background-color: {button_color};
        color: {btn_text};
        border: none;
        border-radius: 8px;
        padding: 9px 18px;
        font-weight: 600;
    }}

    QPushButton:hover {{
        background-color: {btn_hover};
    }}

    QPushButton:pressed {{
        background-color: {btn_pressed};
    }}

    QPushButton:disabled {{
        background-color: #64748b;
        color: #cbd5e1;
    }}

    /* Variantes de Botones */
    QPushButton.btn-secondary {{
        background-color: {hover_bg};
        color: {text_primary};
        border: 1px solid {input_border};
    }}
    QPushButton.btn-secondary:hover {{
        background-color: {input_border};
    }}

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

    /* Tipografía y Títulos */
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

    QLabel.badge {{
        background-color: {button_color};
        color: {btn_text};
        border-radius: 12px;
        padding: 4px 12px;
        font-weight: 600;
        font-size: {font_size - 1}pt;
    }}
    """
    return qss
