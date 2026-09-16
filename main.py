# -*- coding: utf-8 -*-
"""
Punto de entrada principal del Sistema de Gestión de Tiempos y Archivos CSV.
Manejo global de excepciones para prevenir tracebacks no capturados y garantizar estabilidad.
"""

import sys
import os
import traceback
from PyQt6.QtWidgets import QApplication, QMessageBox
from PyQt6.QtCore import Qt

# Asegurar que la ruta base esté en sys.path
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
if PROJECT_DIR not in sys.path:
    sys.path.insert(0, PROJECT_DIR)

from core.config_manager import ConfigManager
from core.storage_manager import StorageManager
from ui.main_window import MainWindow

def global_exception_hook(exctype, value, tb):
    """
    
    Capturador global de contingencias no controladas.
    Muestra un diálogo amigable al usuario en lugar de dejar caer la aplicación con un traceback en consola.
    """
    err_msg = "".join(traceback.format_exception(exctype, value, tb))
    print("Capturada excepción no controlada:", err_msg, file=sys.stderr)
    
    if QApplication.instance():
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Icon.Critical)
        msg_box.setWindowTitle("Aviso del Sistema - Error Controlado")
        msg_box.setText(
            "Ha ocurrido un error inesperado en la ejecución del sistema.\n"
            "La aplicación ha protegido los archivos mediante el sistema de respaldos .bak."
        )
        msg_box.setDetailedText(err_msg)
        msg_box.exec()
    else:
        sys.__excepthook__(exctype, value, tb)

def main():
    # Instalar hook global de excepciones
    sys.excepthook = global_exception_hook

    # Configuración de renderizado de alta densidad (High-DPI)
    if hasattr(Qt.HighDpiScaleFactorRoundingPolicy, "PassThrough"):
        QApplication.setHighDpiScaleFactorRoundingPolicy(
            Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
        )

    app = QApplication(sys.argv)
    app.setApplicationName("Sistema de Control de Horarios y Archivos CSV")
    app.setOrganizationName("SistemaArchivos")

    # Inicialización de administradores del sistema
    config_mgr = ConfigManager(base_dir=PROJECT_DIR)
    storage_mgr = StorageManager(base_dir=PROJECT_DIR)

    # Ventana principal
    window = MainWindow(config_manager=config_mgr, storage_manager=storage_mgr)
    window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
