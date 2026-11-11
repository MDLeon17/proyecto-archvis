# -*- coding: utf-8 -*-
"""
Módulo de internacionalización (i18n) para el Sistema de Perfil y Personalización.
Soporta Español ('es' / 'es-ES') e Inglés ('en' / 'en-US').
Sin emoticonos / emojis.
"""

TRANSLATIONS = {
    'es': {
        'app_title': 'Sistema de Perfil y Configuración de Pantalla',
        'nav_profile': 'Perfil',
        'nav_settings': 'Configuración',
        
        # Estados / Insignias
        'status_active': 'Activo',
        'status_customized': 'Personalizado',
        'status_user': 'Usuario',
        
        # Profile View
        'profile_title': 'Perfil de Usuario',
        'profile_subtitle': 'Visualización en tiempo real de su perfil y la personalización aplicada en Configuración',
        'profile_card_title': 'Identidad de Usuario',
        'profile_customization_title': 'Personalización Activa del Sistema',
        'lbl_active_theme': 'Tema de Pantalla:',
        'lbl_active_lang': 'Idioma del Sistema:',
        'lbl_active_font_size': 'Tamaño de Fuente:',
        'lbl_active_button_color': 'Color de Botones:',
        'lbl_active_sidebar_color': 'Color de Barra Lateral:',
        'lbl_active_font_color': 'Color de Letra:',
        'profile_samples_title': 'Vista Previa de Componentes con Estilos Activos',
        'lbl_sample_button_primary': 'Botón Principal',
        'lbl_sample_button_secondary': 'Botón Secundario',
        'lbl_sample_card': 'Tarjeta de Demostración Visual',
        'lbl_sample_text': 'Este texto y los elementos inferiores demuestran en vivo la tipografía, tamaño y colores seleccionados en Configuración.',
        'btn_go_to_settings': 'Personalizar en Configuración',
        'lang_spanish': 'Español',
        'lang_english': 'English (Inglés)',
        'theme_light_desc': 'Modo Claro (Fondo Claro, Texto Oscuro)',
        'theme_dark_desc': 'Modo Oscuro (Fondo Oscuro, Texto Claro)',
        
        # Settings View
        'settings_title': 'Configuración del Sistema',
        'settings_subtitle': 'Personalice el tema visual, colores de botones y pantalla, tipografía, idioma y foto de perfil',
        'cfg_profile_section': 'Datos del Perfil',
        'cfg_appearance_section': 'Personalización de Pantalla y Colores',
        'cfg_username': 'Nombre de usuario:',
        'cfg_user_role': 'Rol / Puesto:',
        'cfg_bio': 'Biografía / Descripción:',
        'cfg_theme': 'Modo de Pantalla:',
        'theme_light': 'Modo Claro',
        'theme_dark': 'Modo Oscuro',
        'cfg_language': 'Idioma del Sistema:',
        'cfg_font_size': 'Tamaño de Fuente:',
        'cfg_button_color': 'Color de Botones:',
        'cfg_sidebar_color': 'Color de Barra Lateral / Menú:',
        'cfg_font_color': 'Color de Letra / Tipografía:',
        'cfg_profile_photo': 'Foto de Perfil:',
        'btn_pick_color': 'Elegir Color...',
        'btn_pick_photo': 'Seleccionar Foto...',
        'btn_remove_photo': 'Quitar Foto',
        'btn_save_settings': 'Guardar Configuración',
        'btn_restore_settings_bak': 'Restaurar Copia Previa (.bak)',
        'btn_reset_defaults': 'Restablecer Valores por Defecto',
        'cfg_persistence_info': 'La configuración se almacena con persistencia atómica segura en config.json y se conserva un respaldo automático en config.bak.',
        
        # Mensajes Generales
        'msg_success': 'Operación Exitosa',
        'msg_error': 'Error en la Operación',
        'msg_warning': 'Advertencia',
        'msg_info': 'Información',
        'msg_saved_success': 'Configuración guardada exitosamente. Los cambios se han reflejado en toda la interfaz.',
        'msg_restore_success': 'Configuración restaurada exitosamente desde la copia previa .bak.',
        'msg_restore_confirm': '¿Desea restaurar la configuración anterior desde el respaldo (.bak)? Se sobreescribirá la configuración actual con la última guardada.',
        'msg_reset_confirm': '¿Desea restablecer todas las configuraciones a sus valores predeterminados?',
        'file_filter_images': 'Imágenes (*.png *.jpg *.jpeg *.bmp *.ico *.webp)',
        'file_filter_all': 'Todos los archivos (*.*)',
        'sidebar_version': 'Sistema de Personalización v2.0'
    },
    'en': {
        'app_title': 'Profile & Screen Customization System',
        'nav_profile': 'Profile',
        'nav_settings': 'Settings',
        
        # States / Badges
        'status_active': 'Active',
        'status_customized': 'Customized',
        'status_user': 'User',
        
        # Profile View
        'profile_title': 'User Profile',
        'profile_subtitle': 'Real-time view of your profile and customizations configured in Settings',
        'profile_card_title': 'User Identity',
        'profile_customization_title': 'Active System Customization',
        'lbl_active_theme': 'Screen Theme:',
        'lbl_active_lang': 'System Language:',
        'lbl_active_font_size': 'Font Size:',
        'lbl_active_button_color': 'Button Color:',
        'lbl_active_sidebar_color': 'Sidebar Color:',
        'lbl_active_font_color': 'Font Color:',
        'profile_samples_title': 'Live Component Preview with Active Styles',
        'lbl_sample_button_primary': 'Primary Button',
        'lbl_sample_button_secondary': 'Secondary Button',
        'lbl_sample_card': 'Visual Demonstration Card',
        'lbl_sample_text': 'This sample text and the elements below demonstrate the font, size, and colors selected in Settings.',
        'btn_go_to_settings': 'Customize in Settings',
        'lang_spanish': 'Español (Spanish)',
        'lang_english': 'English',
        'theme_light_desc': 'Light Mode (Light background, Dark text)',
        'theme_dark_desc': 'Dark Mode (Dark background, Light text)',
        
        # Settings View
        'settings_title': 'System Settings',
        'settings_subtitle': 'Customize visual theme, button and screen colors, typography, language, and profile photo',
        'cfg_profile_section': 'Profile Details',
        'cfg_appearance_section': 'Screen & Color Customization',
        'cfg_username': 'Username:',
        'cfg_user_role': 'Role / Title:',
        'cfg_bio': 'Bio / Description:',
        'cfg_theme': 'Screen Mode:',
        'theme_light': 'Light Mode',
        'theme_dark': 'Dark Mode',
        'cfg_language': 'System Language:',
        'cfg_font_size': 'Font Size:',
        'cfg_button_color': 'Button Color:',
        'cfg_sidebar_color': 'Sidebar / Menu Color:',
        'cfg_font_color': 'Font / Text Color:',
        'cfg_profile_photo': 'Profile Photo:',
        'btn_pick_color': 'Pick Color...',
        'btn_pick_photo': 'Select Photo...',
        'btn_remove_photo': 'Remove Photo',
        'btn_save_settings': 'Save Settings',
        'btn_restore_settings_bak': 'Restore Previous Backup (.bak)',
        'btn_reset_defaults': 'Reset to Defaults',
        'cfg_persistence_info': 'Settings are saved with safe atomic persistence in config.json with an automatic backup preserved in config.bak.',
        
        # General Messages
        'msg_success': 'Operation Successful',
        'msg_error': 'Operation Error',
        'msg_warning': 'Warning',
        'msg_info': 'Information',
        'msg_saved_success': 'Settings successfully saved. Changes are now reflected across the entire interface.',
        'msg_restore_success': 'Settings successfully restored from previous .bak backup.',
        'msg_restore_confirm': 'Do you want to restore previous settings from backup (.bak)? Current settings will be replaced by the last saved state.',
        'msg_reset_confirm': 'Do you want to reset all settings to defaults?',
        'file_filter_images': 'Images (*.png *.jpg *.jpeg *.bmp *.ico *.webp)',
        'file_filter_all': 'All files (*.*)',
        'sidebar_version': 'Customization System v2.0'
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
