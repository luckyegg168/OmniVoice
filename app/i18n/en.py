"""English translations."""

EN_TRANSLATIONS: dict[str, str] = {
    # App
    "app_title": "OmniVoice TTS",
    "app_subtitle": "Multi-engine Multilingual Text-to-Speech",

    # Navigation
    "nav_tts": "Text to Speech",
    "nav_clone": "Voice Clone",
    "nav_batch": "Batch Processing",
    "nav_ssml": "SSML Editor",
    "nav_history": "History",
    "nav_settings": "Settings",
    "nav_about": "About",

    # TTS Page
    "input_text": "Input Text",
    "input_placeholder": "Enter text to convert to speech...",
    "engine_label": "Engine",
    "voice_label": "Voice",
    "language_label": "Language",
    "speed_label": "Speed",
    "pitch_label": "Pitch",
    "volume_label": "Volume",
    "generate_btn": "🎙️ Generate",
    "preview_btn": "▶️ Preview",
    "download_btn": "⬇️ Download",
    "generating": "Generating speech...",
    "generate_success": "Speech generated successfully!",
    "generate_error": "Speech generation failed",
    "char_count": "Characters",
    "word_count": "Words",
    "est_duration": "Est. Duration",

    # Voice Clone
    "clone_title": "Voice Cloning",
    "clone_desc": "Upload 3-10 second reference audio to clone voice style",
    "ref_audio": "Reference Audio",
    "ref_text": "Reference Text (optional)",
    "target_text": "Target Text",
    "upload_audio": "Upload Audio",

    # Batch
    "batch_title": "Batch Conversion",
    "batch_desc": "Import TXT or SRT files for batch conversion",
    "upload_file": "Upload File",
    "start_batch": "Start Batch",
    "batch_progress": "Progress",
    "download_all": "Download All",

    # SSML
    "ssml_title": "SSML Editor",
    "ssml_desc": "Use SSML tags for fine-grained speech control",
    "ssml_preview": "Preview",
    "insert_tag": "Insert Tag",

    # History
    "history_title": "History",
    "history_empty": "No history records",
    "search": "Search",
    "delete": "Delete",
    "favorite": "Favorite",
    "unfavorite": "Unfavorite",
    "replay": "Replay",
    "clear_history": "Clear History",

    # Settings
    "settings_title": "Settings",
    "locale_label": "Language",
    "theme_label": "Theme",
    "theme_dark": "Dark",
    "theme_light": "Light",
    "default_engine_label": "Default Engine",
    "default_voice_label": "Default Voice",
    "output_dir_label": "Output Directory",
    "export_settings": "Export Settings",
    "import_settings": "Import Settings",
    "save_settings": "Save",
    "settings_saved": "Settings saved",

    # About
    "about_title": "About OmniVoice",
    "version": "Version",
    "engine_status": "Engine Status",
    "available": "Available",
    "unavailable": "Unavailable",
    "usage_guide": "Usage Guide",
    "license_info": "License",

    # Common
    "confirm": "Confirm",
    "cancel": "Cancel",
    "close": "Close",
    "loading": "Loading...",
    "error": "Error",
    "success": "Success",
    "warning": "Warning",
    "no_data": "No data",
    "text_too_long": "Text exceeds length limit",
    "text_empty": "Please enter text",

    # Non-verbal symbols
    "symbols_title": "Non-verbal Symbols",
    "insert_symbol": "Insert Symbol",

    # Pronunciation
    "pronunciation_title": "Pronunciation Correction",
    "pinyin_label": "Pinyin (Chinese)",
    "cmu_label": "CMU Phoneme (English)",

    # Queue
    "queue_title": "Task Queue",
    "queue_empty": "Queue empty",
    "queue_pending": "Pending",
    "queue_processing": "Processing",
    "queue_completed": "Completed",

    # Notifications
    "task_complete": "Task completed",
    "task_failed": "Task failed",

    # Voice presets
    "presets_title": "Voice Presets",
    "preset_news": "News Anchor",
    "preset_story": "Story Reader",
    "preset_assistant": "Smart Assistant",
    "preset_child": "Children's Book",

    # Keyboard shortcuts
    "shortcuts_title": "Keyboard Shortcuts",
    "shortcut_generate": "Ctrl+Enter: Generate",
    "shortcut_play": "Space: Play/Pause",

    # Additional page keys
    "tts_title": "Text to Speech",
    "clone_description": "Upload 3-10 second reference audio to clone voice style with OmniVoice",
    "upload_ref_audio": "Upload Reference Audio",
    "upload_label": "Choose audio file",
    "upload_success": "Upload successful",
    "upload_ref_first": "Please upload reference audio first",
    "clone_target_text": "Target Text",
    "clone_placeholder": "Enter text to speak with cloned voice...",
    "clone_btn": "Clone Voice",
    "clone_success": "Voice cloned successfully",
    "omnivoice_unavailable": "OmniVoice engine unavailable (torch required)",
    "engine_unavailable": "Selected engine is unavailable",
    "batch_input": "Input Text",
    "batch_input_placeholder": "Enter a line of text...",
    "add_btn": "Add",
    "batch_upload_file": "Upload TXT file",
    "batch_file_loaded": "File loaded",
    "items": "items",
    "batch_queue": "Processing Queue",
    "clear_all_btn": "Clear All",
    "batch_start": "Start Batch",
    "batch_empty": "Queue is empty, add items first",
    "batch_complete": "Batch conversion complete",
    "ssml_description": "Use SSML tags for fine-grained speech synthesis control",
    "ssml_templates": "SSML Templates",
    "ssml_editor_label": "SSML Editor",
    "ssml_generate": "Generate Speech",
    "ssml_empty": "Please enter SSML content",
    "search_label": "Search",
    "search_placeholder": "Enter keyword to search...",
    "all_engines": "All Engines",
    "filter_engine": "Filter Engine",
    "search_btn": "Search",
    "language_settings": "Language Settings",
    "default_settings": "Default Settings",
    "general_settings": "General Settings",
    "auto_play": "Auto Play",
    "save_history": "Save History",
    "save_settings_btn": "Save Settings",
    "export_settings_btn": "Export Settings",
    "settings_exported": "Settings exported",
    "import_settings_label": "Import settings JSON file",
    "settings_imported": "Settings imported",
    "license": "License",
    "features": "Features",
    "feature_multi_engine": "Multi-engine support (Edge-TTS, gTTS, OmniVoice)",
    "feature_voice_clone": "Voice cloning (zero-shot voice copy)",
    "feature_batch": "Batch processing (multi-text queue conversion)",
    "feature_ssml": "SSML editor (fine-grained speech control)",
    "feature_history": "History (search, favorite, replay)",
    "feature_i18n": "Multi-language UI (zh-TW/EN/JA)",
    "feature_dark_mode": "Dark/Light theme toggle",
    "feature_export_import": "Settings export/import",
    "feature_audio_preview": "Real-time audio preview",
    "feature_text_stats": "Text statistics & duration estimate",
    "tech_stack": "Tech Stack",
    "usage_guide_content": (
        "### Quick Start\n\n"
        "1. Enter text in the text box\n"
        "2. Select engine and voice\n"
        "3. Adjust speed, pitch, volume\n"
        "4. Click 'Generate Speech'\n"
        "5. Preview and download audio"
    ),
}
