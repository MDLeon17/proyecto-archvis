# -*- coding: utf-8 -*-
"""
StorageManager: Administrador del archivo CSV de registros con atomic write,
respaldo .bak previo a cualquier modificación, cálculo de tiempos y manejo
robusto de excepciones y codificación UTF-8.
"""

import os
import csv
import shutil
import datetime
from typing import List, Dict, Any, Tuple, Optional

CSV_COLUMNS = [
    "id",
    "usuario",
    "fecha",
    "hora_inicio",
    "hora_fin",
    "duracion_horas",
    "estado",
    "notas"
]

class StorageManager:
    """
    Gestiona la persistencia de registros en formato CSV.
    Cada acción (agregar, modificar, eliminar, restaurar) genera un respaldo .bak
    y utiliza reemplazo atómico (.tmp -> .csv) para evitar corrupción de datos.
    """

    def __init__(self, base_dir: Optional[str] = None, filename: str = "registros.csv"):
        if base_dir is None:
            self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        else:
            self.base_dir = base_dir

        self.csv_file = os.path.join(self.base_dir, filename)
        self.temp_file = os.path.join(self.base_dir, filename.replace(".csv", ".tmp"))
        self.backup_file = os.path.join(self.base_dir, filename + ".bak")
        self.ensure_file_initialized()

    def ensure_file_initialized(self) -> None:
        """Crea el archivo con cabeceras si no existe."""
        if not os.path.exists(self.csv_file):
            try:
                with open(self.csv_file, "w", encoding="utf-8", newline="") as f:
                    writer = csv.writer(f)
                    writer.writerow(CSV_COLUMNS)
            except Exception:
                pass

    def load_records(self) -> Tuple[List[Dict[str, Any]], Optional[str]]:
        """
        Lee todos los registros desde el archivo CSV con UTF-8.
        Tolera filas corruptas o truncadas omitiéndolas de forma segura sin caerse.
        Retorna (lista_de_registros, error_mensaje_si_hubo).
        """
        self.ensure_file_initialized()
        records: List[Dict[str, Any]] = []
        warning_msg: Optional[str] = None

        try:
            with open(self.csv_file, "r", encoding="utf-8", newline="", errors="replace") as f:
                reader = csv.DictReader(f)
                row_idx = 1
                for row in reader:
                    row_idx += 1
                    if not row or not any(row.values()):
                        continue
                    try:
                        record_id = int(row.get("id", row_idx))
                    except (ValueError, TypeError):
                        record_id = row_idx

                    # Normalizar campos
                    clean_row = {
                        "id": record_id,
                        "usuario": str(row.get("usuario", "")).strip(),
                        "fecha": str(row.get("fecha", "")).strip(),
                        "hora_inicio": str(row.get("hora_inicio", "")).strip(),
                        "hora_fin": str(row.get("hora_fin", "")).strip(),
                        "duracion_horas": str(row.get("duracion_horas", "0.00")).strip(),
                        "estado": str(row.get("estado", "")).strip(),
                        "notas": str(row.get("notas", "")).strip()
                    }
                    records.append(clean_row)
        except PermissionError as e:
            return [], f"Permiso denegado al leer el archivo CSV: {str(e)}"
        except Exception as e:
            return [], f"Error inesperado al leer registros: {str(e)}"

        return records, warning_msg

    def get_record_by_id(self, record_id: int) -> Optional[Dict[str, Any]]:
        """Busca y retorna un registro por su ID único."""
        records, _ = self.load_records()
        for r in records:
            if r["id"] == record_id:
                return dict(r)
        return None

    def get_next_id(self) -> int:
        """Obtiene el siguiente ID autoincremental."""
        records, _ = self.load_records()
        if not records:
            return 1
        return max(r["id"] for r in records) + 1

    def _save_all(self, records: List[Dict[str, Any]], create_backup: bool = True) -> Tuple[bool, str]:
        """
        Escritura atómica de toda la lista de registros en CSV:
        1. Respaldo previo a registros.csv.bak
        2. Escritura a registros.tmp en UTF-8
        3. Flush + Fsync
        4. Reemplazo atómico con os.replace
        """
        try:
            # 1. Respaldo previo
            if create_backup and os.path.exists(self.csv_file):
                try:
                    shutil.copy2(self.csv_file, self.backup_file)
                except Exception:
                    pass

            # 2. Escribir a .tmp
            with open(self.temp_file, "w", encoding="utf-8", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=CSV_COLUMNS)
                writer.writeheader()
                for r in records:
                    row_data = {col: r.get(col, "") for col in CSV_COLUMNS}
                    writer.writerow(row_data)
                f.flush()
                os.fsync(f.fileno())

            # 3. Reemplazo atómico
            os.replace(self.temp_file, self.csv_file)
            return True, "Archivo guardado exitosamente."
        except PermissionError as e:
            return False, f"Permiso denegado al guardar el archivo: {str(e)}"
        except Exception as e:
            return False, f"Error al guardar los registros: {str(e)}"

    def add_record(self, record: Dict[str, Any]) -> Tuple[bool, str, Optional[int]]:
        """
        Agrega un nuevo registro al CSV creando respaldo previo.
        Calcula la duración si no viene dada.
        """
        records, err = self.load_records()
        if err:
            return False, err, None

        rec = dict(record)
        if "id" not in rec or not rec["id"]:
            rec["id"] = self.get_next_id()
        else:
            try:
                rec["id"] = int(rec["id"])
            except ValueError:
                rec["id"] = self.get_next_id()

        # Calcular duración si faltase
        if not rec.get("duracion_horas"):
            rec["duracion_horas"] = self.calculate_duration(
                rec.get("hora_inicio", ""), rec.get("hora_fin", "")
            )

        records.append(rec)
        ok, msg = self._save_all(records, create_backup=True)
        return ok, msg, rec["id"]

    def update_record(self, record_id: int, updated_fields: Dict[str, Any]) -> Tuple[bool, str]:
        """
        Modifica un registro existente por su ID.
        Permite corregir estados (ej. cambiar 3 horas de Lunch a Ready) y recalcula la duración.
        """
        records, err = self.load_records()
        if err:
            return False, err

        found = False
        for i, r in enumerate(records):
            if r["id"] == record_id:
                for k, v in updated_fields.items():
                    if k != "id":
                        r[k] = v
                # Recalcular duración
                r["duracion_horas"] = self.calculate_duration(
                    r.get("hora_inicio", ""), r.get("hora_fin", "")
                )
                records[i] = r
                found = True
                break

        if not found:
            return False, f"No se encontró el registro con ID #{record_id}."

        return self._save_all(records, create_backup=True)

    def delete_record(self, record_id: int) -> Tuple[bool, str]:
        """
        Elimina un registro del archivo CSV creando respaldo previo.
        """
        records, err = self.load_records()
        if err:
            return False, err

        initial_count = len(records)
        records = [r for r in records if r["id"] != record_id]

        if len(records) == initial_count:
            return False, f"No se encontró el registro con ID #{record_id} para eliminar."

        return self._save_all(records, create_backup=True)

    def restore_backup(self) -> Tuple[bool, str]:
        """
        Restaura el archivo CSV desde la última copia de seguridad (.bak).
        """
        if not os.path.exists(self.backup_file):
            return False, "No existe una copia de respaldo (.bak) disponible para restaurar."

        try:
            # Validamos que el archivo .bak tenga al menos contenido legible
            with open(self.backup_file, "r", encoding="utf-8", newline="", errors="replace") as f:
                reader = csv.reader(f)
                header = next(reader, None)
                if not header:
                    return False, "El archivo de respaldo está vacío o corrupto."

            # Escribir temporal y reemplazar
            shutil.copy2(self.backup_file, self.temp_file)
            os.replace(self.temp_file, self.csv_file)
            return True, "Registros restaurados exitosamente desde la copia .bak."
        except PermissionError as e:
            return False, f"Permiso denegado al restaurar copia: {str(e)}"
        except Exception as e:
            return False, f"Error al restaurar copia de seguridad: {str(e)}"

    def create_manual_backup(self) -> Tuple[bool, str]:
        """Crea una copia manual inmediata a .bak."""
        if not os.path.exists(self.csv_file):
            return False, "El archivo CSV no existe aún."
        try:
            shutil.copy2(self.csv_file, self.backup_file)
            return True, "Copia de seguridad manual (.bak) creada exitosamente."
        except Exception as e:
            return False, f"Error al crear copia: {str(e)}"

    def has_backup(self) -> bool:
        return os.path.exists(self.backup_file) and os.path.getsize(self.backup_file) > 0

    def get_backup_info(self) -> Dict[str, Any]:
        if not self.has_backup():
            return {"exists": False, "date": "", "size": 0}
        try:
            mtime = os.path.getmtime(self.backup_file)
            size = os.path.getsize(self.backup_file)
            dt_str = datetime.datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M:%S")
            return {"exists": True, "date": dt_str, "size": size}
        except Exception:
            return {"exists": False, "date": "", "size": 0}

    @staticmethod
    def calculate_duration(start_str: str, end_str: str) -> str:
        """
        Calcula la diferencia en horas decimales (ej. '3.00') entre HH:MM[:SS] y HH:MM[:SS].
        Si end_str está vacío o es inválido, retorna '0.00'.
        """
        if not start_str or not end_str:
            return "0.00"

        fmt_list = ["%H:%M:%S", "%H:%M"]
        t1, t2 = None, None

        for fmt in fmt_list:
            if t1 is None:
                try:
                    t1 = datetime.datetime.strptime(start_str.strip(), fmt)
                except ValueError:
                    pass
            if t2 is None:
                try:
                    t2 = datetime.datetime.strptime(end_str.strip(), fmt)
                except ValueError:
                    pass

        if t1 is None or t2 is None:
            return "0.00"

        diff_seconds = (t2 - t1).total_seconds()
        if diff_seconds < 0:
            # Caso en que cruza la medianoche
            diff_seconds += 24 * 3600

        hours = diff_seconds / 3600.0
        return f"{hours:.2f}"
