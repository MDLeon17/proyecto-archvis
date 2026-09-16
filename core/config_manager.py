# -*- coding: utf-8 -*-
"""
ConfigManager: Administrador seguro de configuración con atomic write,
respaldo .bak previo, manejo de errores robusto y codificación UTF-8.
"""

import os
import json
import shutil
from typing import Dict, Any, Tuple, Optional

DEFAULT_CONFIG: Dict[str, Any] = {
    "nombre_usuario": "Operador",
    "tema_interfaz": "oscuro",      # 'claro' o 'oscuro'
    "idioma": "es",                 # 'es' o 'en'
    "tamaño_fuente": 11,            # número entero
    "color_barra_menu": "#1e293b",   # Color de la barra lateral/menú
    "color_letra": "#f8fafc",        # Color de letra general
    "foto_perfil": ""                # Ruta a archivo de imagen
}

class ConfigManager:
    """
    Gestiona la carga, guardado atómico, respaldo y restauración de la configuración.
    """

    def __init__(self, base_dir: Optional[str] = None, config_name: str = "config.json"):
        if base_dir is None:
            self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        else:
            self.base_dir = base_dir

        self.config_file = os.path.join(self.base_dir, config_name)
        self.temp_file = os.path.join(self.base_dir, config_name.replace(".json", ".tmp"))
        self.backup_file = os.path.join(self.base_dir, config_name.replace(".json", ".bak"))
        self._current_config: Dict[str, Any] = self.load_config()

    @property
    def config(self) -> Dict[str, Any]:
        return self._current_config

    def get(self, key: str, default: Any = None) -> Any:
        return self._current_config.get(key, default)

    def set(self, key: str, value: Any) -> None:
        self._current_config[key] = value

    def load_config(self) -> Dict[str, Any]:
        """
        Carga la configuración desde el archivo UTF-8.
        Si no existe, si está corrupto o sin permisos, degrada a DEFAULT_CONFIG sin excepciones.
        """
        if not os.path.exists(self.config_file):
            cfg = dict(DEFAULT_CONFIG)
            try:
                self._write_safe(self.config_file, cfg, create_backup=False)
            except Exception:
                pass
            return cfg

        try:
            with open(self.config_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                if not isinstance(data, dict):
                    raise ValueError("El contenido no es un diccionario válido.")
                
                merged = dict(DEFAULT_CONFIG)
                merged.update(data)
                
                try:
                    merged["tamaño_fuente"] = int(merged.get("tamaño_fuente", 11))
                except (ValueError, TypeError):
                    merged["tamaño_fuente"] = 11

                if merged.get("tema_interfaz") not in ("claro", "oscuro"):
                    merged["tema_interfaz"] = "oscuro"

                if merged.get("idioma") not in ("es", "en"):
                    merged["idioma"] = "es"

                return merged

        except (json.JSONDecodeError, ValueError):
            if os.path.exists(self.backup_file):
                try:
                    with open(self.backup_file, "r", encoding="utf-8") as f_bak:
                        bak_data = json.load(f_bak)
                        if isinstance(bak_data, dict):
                            merged = dict(DEFAULT_CONFIG)
                            merged.update(bak_data)
                            return merged
                except Exception:
                    pass
            return dict(DEFAULT_CONFIG)

        except PermissionError:
            return dict(DEFAULT_CONFIG)

        except Exception:
            return dict(DEFAULT_CONFIG)

    def save_config(self, new_config: Optional[Dict[str, Any]] = None) -> Tuple[bool, str]:
        """
        Guarda la configuración usando escritura segura y respaldo .bak.
        """
        if new_config is not None:
            self._current_config = dict(DEFAULT_CONFIG)
            self._current_config.update(new_config)

        try:
            self._write_safe(self.config_file, self._current_config, create_backup=True)
            return True, "Configuración guardada exitosamente."
        except PermissionError as e:
            return False, f"Error de permisos al escribir en el disco: {str(e)}"
        except Exception as e:
            return False, f"Error al guardar la configuración: {str(e)}"

    def _write_safe(self, target_path: str, data: Dict[str, Any], create_backup: bool = True) -> None:
        """
        Rutina interna de escritura atómica con respaldo previo.
        """
        if create_backup and os.path.exists(target_path):
            try:
                shutil.copy2(target_path, self.backup_file)
            except Exception:
                pass

        with open(self.temp_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
            f.flush()
            os.fsync(f.fileno())

        os.replace(self.temp_file, target_path)

    def restore_backup(self) -> Tuple[bool, str]:
        """
        Restaura la configuración desde config.bak si existe y es válida.
        """
        if not os.path.exists(self.backup_file):
            return False, "No se encontró ningún archivo de respaldo (.bak) para restaurar."

        try:
            with open(self.backup_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                if not isinstance(data, dict):
                    return False, "El archivo de respaldo está corrupto o no tiene formato válido."

            self._write_safe(self.config_file, data, create_backup=False)
            self._current_config = self.load_config()
            return True, "Configuración restaurada exitosamente desde la copia .bak."
        except PermissionError as e:
            return False, f"Error de permisos al restaurar backup: {str(e)}"
        except Exception as e:
            return False, f"Error al procesar el archivo de respaldo: {str(e)}"

    def has_backup(self) -> bool:
        return os.path.exists(self.backup_file) and os.path.getsize(self.backup_file) > 0

    def get_backup_info(self) -> Dict[str, Any]:
        if not self.has_backup():
            return {"exists": False, "date": "", "size": 0}
        try:
            import datetime
            mtime = os.path.getmtime(self.backup_file)
            size = os.path.getsize(self.backup_file)
            dt_str = datetime.datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M:%S")
            return {"exists": True, "date": dt_str, "size": size}
        except Exception:
            return {"exists": False, "date": "", "size": 0}

    def reset_to_defaults(self) -> Tuple[bool, str]:
        """Restablece a los valores por defecto guardando respaldo .bak."""
        return self.save_config(dict(DEFAULT_CONFIG))
