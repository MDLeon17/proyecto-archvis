# -*- coding: utf-8 -*-
"""
Módulo de internacionalización (i18n) para la aplicación.
Soporta Español ('es' / 'es-ES') e Inglés ('en' / 'en-US').
Sin emoticonos / emojis.
"""

TRANSLATIONS = {
    'es': {
        'app_title': 'Sistema de Control de Horarios y Archivos CSV',
        'nav_clock': 'Control de Tiempo',
        'nav_read': 'Consultar Registros',
        'nav_add': 'Agregar Registro',
        'nav_edit': 'Editar Registro',
        'nav_delete': 'Eliminar Registro',
        'nav_settings': 'Configuración',
        'nav_backup': 'Copias de Seguridad (.bak)',
        
        # Estados
        'status_ready': 'En Puesto (Ready)',
        'status_lunch': 'Almuerzo (Lunch)',
        'status_break': 'Descanso (Break)',
        'status_meeting': 'Reunión',
        'status_training': 'Capacitación',
        'status_clock_in': 'Entrada (Clock In)',
        'status_clock_out': 'Salida (Clock Out)',
        'status_unknown': 'Desconocido',
        'status_offline': 'Fuera de turno',
        
        # Clock View
        'clock_title': 'Registro de Jornada y Estados en Tiempo Real',
        'clock_subtitle': 'Registre su ingreso (Clock In), cambie de estado (Ready, Lunch, Break...) y marque su salida',
        'current_time': 'Hora Actual:',
        'current_state': 'Estado Actual:',
        'time_in_state': 'Tiempo acumulado en este estado:',
        'btn_clock_in': 'Marcar Entrada (Clock In)',
        'btn_ready': 'Listo / En Puesto (Ready)',
        'btn_lunch': 'Almuerzo (Lunch)',
        'btn_break': 'Descanso (Break)',
        'btn_meeting': 'Reunión (Meeting)',
        'btn_training': 'Capacitación (Training)',
        'btn_clock_out': 'Marcar Salida (Clock Out)',
        'notes_placeholder': 'Observaciones o notas para este estado (opcional)...',
        'state_switched_msg': 'Estado cambiado a {status}. Se registró el lapso anterior exitosamente.',
        
        # Read View
        'read_title': 'Consulta y Lectura del Archivo CSV',
        'read_subtitle': 'Explore el archivo completo o inspeccione los datos de un registro específico',
        'search_placeholder': 'Buscar por usuario, estado o notas...',
        'filter_all_status': 'Todos los estados',
        'btn_refresh': 'Refrescar Datos',
        'btn_view_detail': 'Ver Detalle del Registro',
        'btn_go_edit': 'Editar Registro Seleccionado',
        'total_records': 'Total de registros:',
        'total_hours': 'Horas totales acumuladas:',
        'col_id': 'ID',
        'col_user': 'Usuario',
        'col_date': 'Fecha',
        'col_start': 'Hora Inicio',
        'col_end': 'Hora Fin',
        'col_duration': 'Duración (h)',
        'col_status': 'Estado',
        'col_notes': 'Notas / Observaciones',
        
        # Add View
        'add_title': 'Agregar Registro Manual al Archivo CSV',
        'add_subtitle': 'Incorpore un nuevo bloque de tiempo con escritura segura y respaldo automático',
        'lbl_user': 'Nombre de Usuario:',
        'lbl_date': 'Fecha:',
        'lbl_start_time': 'Hora de Inicio:',
        'lbl_end_time': 'Hora de Finalización:',
        'lbl_status': 'Estado de la Actividad:',
        'lbl_notes': 'Notas / Observaciones:',
        'lbl_duration_calc': 'Duración calculada:',
        'btn_save_new': 'Guardar Nuevo Registro',
        'btn_clear_fields': 'Limpiar Formulario',
        'record_added_msg': 'Registro #{id} guardado con éxito. Respaldo .bak generado.',
        
        # Edit View
        'edit_title': 'Edición de un Registro en Concreto',
        'edit_subtitle': 'Modifique datos específicos (ej. corregir tiempo de Lunch a Ready si se marcó por error)',
        'select_record_prompt': 'Seleccione el registro que desea modificar:',
        'btn_load_record': 'Cargar Datos del Registro',
        'btn_save_changes': 'Guardar Modificaciones en CSV',
        'btn_cancel_edit': 'Cancelar',
        'edit_help_text': 'Ejemplo práctico: Si un colaborador estuvo 3 horas en Lunch pero en realidad estuvo 3 horas en Ready, cambie el campo "Estado" a Ready y pulse Guardar.',
        'record_updated_msg': 'Registro #{id} actualizado con éxito. Respaldo .bak creado.',
        
        # Delete View
        'delete_title': 'Eliminar un Registro de Tiempo',
        'delete_subtitle': 'Eliminación segura con advertencia de descuento de jornada y copia de seguridad .bak previa',
        'delete_warning_header': 'ADVERTENCIA DE DESCUENTO DE TIEMPO',
        'delete_warning_body': 'Atención: Si elimina este registro de tiempo, ese tiempo se le descontará de su jornada laboral registrada. Antes de borrarlo, el sistema creará una copia de seguridad (.bak) para permitir recuperación.',
        'btn_confirm_delete': 'Eliminar Registro Seleccionado',
        'delete_confirm_title': 'Confirmación de Descuento de Horas',
        'delete_confirm_msg': 'Está seguro de eliminar el registro #{id}?\n\nATENCIÓN: Si elimina este registro de tiempo, ese tiempo se le descontará de su jornada laboral.',
        'record_deleted_msg': 'Registro #{id} eliminado. Copia de seguridad .bak actualizada.',
        
        # Settings View
        'settings_title': 'Configuración del Sistema (Settings)',
        'settings_subtitle': 'Preferencias de usuario, aspecto visual, colores y seguridad de persistencia',
        'cfg_username': 'Nombre de usuario:',
        'cfg_theme': 'Tema de interfaz:',
        'theme_light': 'Claro',
        'theme_dark': 'Oscuro',
        'cfg_language': 'Idioma:',
        'cfg_font_size': 'Tamaño de fuente:',
        'cfg_sidebar_color': 'Color de la barra de menú / lateral:',
        'cfg_font_color': 'Color de letra general:',
        'cfg_profile_photo': 'Foto de perfil:',
        'btn_pick_color': 'Elegir Color...',
        'btn_pick_photo': 'Seleccionar Foto...',
        'btn_remove_photo': 'Quitar Foto',
        'btn_save_settings': 'Guardar Configuración (Escritura Segura)',
        'btn_restore_settings_bak': 'Restaurar Configuración Previa (.bak)',
        'btn_reset_defaults': 'Restablecer Valores por Defecto',
        
        # Backup / Restore
        'backup_title': 'Gestión de Copias de Seguridad (.bak)',
        'backup_subtitle': 'Restaure el archivo de datos CSV o el de configuración a la versión anterior',
        'csv_backup_status': 'Estado de copia de seguridad de registros (.bak):',
        'cfg_backup_status': 'Estado de copia de seguridad de configuración (.bak):',
        'btn_restore_csv_bak': 'Restaurar Registros desde .bak',
        'btn_restore_config_bak': 'Restaurar Configuración desde .bak',
        'btn_create_manual_bak': 'Crear Copia de Seguridad Inmediata',
        'backup_available': 'Disponible (Última mod: {date}, Tamaño: {size} bytes)',
        'backup_not_available': 'No existe copia de respaldo (.bak) aún',
        
        # Mensajes Generales
        'msg_success': 'Operación Exitosa',
        'msg_error': 'Error en la Operación',
        'msg_warning': 'Advertencia',
        'msg_info': 'Información',
        'msg_saved_success': 'Datos guardados correctamente con escritura segura (.tmp -> renombre) y respaldo .bak.',
        'msg_restore_success': 'Restauración completada con éxito desde la copia .bak.',
        'msg_restore_confirm': 'Desea restaurar el archivo desde la última copia de seguridad (.bak)? Se sobrescribirá el estado actual con la versión guardada previamente.',
        'file_filter_images': 'Imágenes (*.png *.jpg *.jpeg *.bmp *.ico *.webp)',
        'file_filter_all': 'Todos los archivos (*.*)',
        'error_file_missing': 'El archivo no existe. Se han cargado los valores por defecto sin interrupción.',
        'error_file_corrupt': 'El archivo estaba corrupto o tenía formato inválido. Se mantuvo la estabilidad del sistema.',
        'error_file_permission': 'Error de permisos al intentar acceder o escribir en el archivo.'
    },
    'en': {
        'app_title': 'Time Tracking & CSV File Management System',
        'nav_clock': 'Time Clock',
        'nav_read': 'View Records',
        'nav_add': 'Add Record',
        'nav_edit': 'Edit Record',
        'nav_delete': 'Delete Record',
        'nav_settings': 'Settings',
        'nav_backup': 'Backups (.bak)',
        
        # States
        'status_ready': 'Ready / Working',
        'status_lunch': 'Lunch',
        'status_break': 'Break',
        'status_meeting': 'Meeting',
        'status_training': 'Training',
        'status_clock_in': 'Clock In',
        'status_clock_out': 'Clock Out',
        'status_unknown': 'Unknown',
        'status_offline': 'Off Shift',
        
        # Clock View
        'clock_title': 'Real-Time Work Shift & Status Tracking',
        'clock_subtitle': 'Record your clock-in, switch between work states (Ready, Lunch, Break...) and clock-out',
        'current_time': 'Current Time:',
        'current_state': 'Current State:',
        'time_in_state': 'Accumulated time in this state:',
        'btn_clock_in': 'Clock In',
        'btn_ready': 'Ready / Working',
        'btn_lunch': 'Lunch',
        'btn_break': 'Break',
        'btn_meeting': 'Meeting',
        'btn_training': 'Training',
        'btn_clock_out': 'Clock Out',
        'notes_placeholder': 'Optional notes or observations for this state...',
        'state_switched_msg': 'Status changed to {status}. Previous session saved successfully.',
        
        # Read View
        'read_title': 'Query & Inspect CSV File Records',
        'read_subtitle': 'Explore the entire CSV file or inspect specific record details',
        'search_placeholder': 'Search by user, status, notes...',
        'filter_all_status': 'All statuses',
        'btn_refresh': 'Refresh Data',
        'btn_view_detail': 'View Record Details',
        'btn_go_edit': 'Edit Selected Record',
        'total_records': 'Total records:',
        'total_hours': 'Total accumulated hours:',
        'col_id': 'ID',
        'col_user': 'User',
        'col_date': 'Date',
        'col_start': 'Start Time',
        'col_end': 'End Time',
        'col_duration': 'Duration (h)',
        'col_status': 'Status',
        'col_notes': 'Notes / Remarks',
        
        # Add View
        'add_title': 'Add Manual Record to CSV File',
        'add_subtitle': 'Insert a new time block with safe atomic writing and automatic .bak backup',
        'lbl_user': 'Username:',
        'lbl_date': 'Date:',
        'lbl_start_time': 'Start Time:',
        'lbl_end_time': 'End Time:',
        'lbl_status': 'Activity / Status:',
        'lbl_notes': 'Notes / Remarks:',
        'lbl_duration_calc': 'Calculated Duration:',
        'btn_save_new': 'Save New Record',
        'btn_clear_fields': 'Clear Form',
        'record_added_msg': 'Record #{id} saved successfully. .bak backup generated.',
        
        # Edit View
        'edit_title': 'Edit Specific Time Record',
        'edit_subtitle': 'Modify specific data (e.g. correct logged Lunch time to Ready if registered mistakenly)',
        'select_record_prompt': 'Select the record you want to modify:',
        'btn_load_record': 'Load Record Data',
        'btn_save_changes': 'Save Modifications to CSV',
        'btn_cancel_edit': 'Cancel',
        'edit_help_text': 'Practical example: If an employee was in Lunch for 3 hours mistakenly when they were actually Ready, change the Status to Ready and click Save.',
        'record_updated_msg': 'Record #{id} updated successfully. .bak backup created.',
        
        # Delete View
        'delete_title': 'Delete a Time Record',
        'delete_subtitle': 'Safe deletion with shift deduction warning and prior .bak backup',
        'delete_warning_header': 'TIME DEDUCTION WARNING',
        'delete_warning_body': 'Attention: If you delete this time record, that time will be deducted from your logged work shift. Before deleting, the system creates an automatic .bak backup for safety.',
        'btn_confirm_delete': 'Delete Selected Record',
        'delete_confirm_title': 'Shift Hours Deduction Confirmation',
        'delete_confirm_msg': 'Are you sure you want to delete record #{id}?\n\nWARNING: If you delete this time record, that time will be deducted from your work shift.',
        'record_deleted_msg': 'Record #{id} deleted. .bak backup updated.',
        
        # Settings View
        'settings_title': 'System Settings',
        'settings_subtitle': 'User preferences, visual theme, colors, and persistence safety',
        'cfg_username': 'Username:',
        'cfg_theme': 'UI Theme:',
        'theme_light': 'Light',
        'theme_dark': 'Dark',
        'cfg_language': 'Language:',
        'cfg_font_size': 'Font size:',
        'cfg_sidebar_color': 'Menu / Sidebar color:',
        'cfg_font_color': 'Main font color:',
        'cfg_profile_photo': 'Profile photo:',
        'btn_pick_color': 'Pick Color...',
        'btn_pick_photo': 'Select Photo...',
        'btn_remove_photo': 'Remove Photo',
        'btn_save_settings': 'Save Settings (Safe Atomic Write)',
        'btn_restore_settings_bak': 'Restore Previous Settings (.bak)',
        'btn_reset_defaults': 'Reset to Defaults',
        
        # Backup / Restore
        'backup_title': 'Backup Management (.bak)',
        'backup_subtitle': 'Roll back CSV data or configuration to the previous state',
        'csv_backup_status': 'CSV records backup status (.bak):',
        'cfg_backup_status': 'Settings backup status (.bak):',
        'btn_restore_csv_bak': 'Restore Records from .bak',
        'btn_restore_config_bak': 'Restore Settings from .bak',
        'btn_create_manual_bak': 'Create Immediate Backup',
        'backup_available': 'Available (Last modified: {date}, Size: {size} bytes)',
        'backup_not_available': 'No backup file (.bak) found yet',
        
        # General Messages
        'msg_success': 'Success',
        'msg_error': 'Operation Error',
        'msg_warning': 'Warning',
        'msg_info': 'Information',
        'msg_saved_success': 'Data successfully saved with safe atomic writing (.tmp -> rename) and .bak backup.',
        'msg_restore_success': 'Restoration completed successfully from .bak backup.',
        'msg_restore_confirm': 'Are you sure you want to restore the file from the latest backup (.bak)? The current state will be overwritten by the previous version.',
        'file_filter_images': 'Images (*.png *.jpg *.jpeg *.bmp *.ico *.webp)',
        'file_filter_all': 'All files (*.*)',
        'error_file_missing': 'The file does not exist. Default values loaded seamlessly.',
        'error_file_corrupt': 'The file was corrupted or had invalid format. System stability maintained.',
        'error_file_permission': 'Permission error when attempting to read or write file.'
    }
}

class I18n:
    _current_lang = 'es'

    @classmethod
    def set_language(cls, lang_code: str):
        if lang_code in ('en', 'en-US', 'en-GB'):
            cls._current_lang = 'en'
        else:
            cls._current_lang = 'es'

    @classmethod
    def get_language(cls) -> str:
        return cls._current_lang

    @classmethod
    def t(cls, key: str, **kwargs) -> str:
        lang_dict = TRANSLATIONS.get(cls._current_lang, TRANSLATIONS['es'])
        text = lang_dict.get(key, TRANSLATIONS['es'].get(key, key))
        if kwargs:
            try:
                return text.format(**kwargs)
            except Exception:
                return text
        return text

t = I18n.t
