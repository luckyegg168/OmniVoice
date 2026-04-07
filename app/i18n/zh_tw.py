"""Traditional Chinese (zh-TW) translations."""

ZH_TW_TRANSLATIONS: dict[str, str] = {
    # App
    "app_title": "OmniVoice 語音生成",
    "app_subtitle": "多引擎多國語系文字轉語音",

    # Navigation
    "nav_tts": "語音生成",
    "nav_clone": "語音克隆",
    "nav_batch": "批次處理",
    "nav_ssml": "SSML 編輯",
    "nav_history": "歷史紀錄",
    "nav_settings": "設定",
    "nav_about": "關於",

    # TTS Page
    "input_text": "輸入文字",
    "input_placeholder": "在此輸入要轉換為語音的文字...",
    "engine_label": "引擎",
    "voice_label": "語音",
    "language_label": "語言",
    "speed_label": "速度",
    "pitch_label": "音調",
    "volume_label": "音量",
    "generate_btn": "🎙️ 生成語音",
    "preview_btn": "▶️ 預覽播放",
    "download_btn": "⬇️ 下載音檔",
    "generating": "語音生成中...",
    "generate_success": "語音生成成功！",
    "generate_error": "語音生成失敗",
    "char_count": "字數",
    "word_count": "詞數",
    "est_duration": "預估時長",

    # Voice Clone
    "clone_title": "語音克隆",
    "clone_desc": "上傳 3-10 秒參考音檔，克隆語音風格",
    "ref_audio": "參考音檔",
    "ref_text": "參考文字（選填）",
    "target_text": "目標文字",
    "upload_audio": "上傳音檔",

    # Batch
    "batch_title": "批次語音轉換",
    "batch_desc": "匯入 TXT 或 SRT 檔案進行批次轉換",
    "upload_file": "上傳檔案",
    "start_batch": "開始批次轉換",
    "batch_progress": "轉換進度",
    "download_all": "全部下載",

    # SSML
    "ssml_title": "SSML 編輯器",
    "ssml_desc": "使用 SSML 標籤精細控制語音合成",
    "ssml_preview": "預覽",
    "insert_tag": "插入標籤",

    # History
    "history_title": "歷史紀錄",
    "history_empty": "暫無歷史紀錄",
    "search": "搜尋",
    "delete": "刪除",
    "favorite": "收藏",
    "unfavorite": "取消收藏",
    "replay": "重播",
    "clear_history": "清除歷史",

    # Settings
    "settings_title": "設定",
    "locale_label": "介面語言",
    "theme_label": "主題",
    "theme_dark": "深色",
    "theme_light": "淺色",
    "default_engine_label": "預設引擎",
    "default_voice_label": "預設語音",
    "output_dir_label": "輸出目錄",
    "export_settings": "匯出設定",
    "import_settings": "匯入設定",
    "save_settings": "儲存設定",
    "settings_saved": "設定已儲存",

    # About
    "about_title": "關於 OmniVoice",
    "version": "版本",
    "engine_status": "引擎狀態",
    "available": "可用",
    "unavailable": "不可用",
    "usage_guide": "使用說明",
    "license_info": "授權資訊",

    # Common
    "confirm": "確認",
    "cancel": "取消",
    "close": "關閉",
    "loading": "載入中...",
    "error": "錯誤",
    "success": "成功",
    "warning": "警告",
    "no_data": "無資料",
    "text_too_long": "文字超過長度限制",
    "text_empty": "請輸入文字",

    # Non-verbal symbols
    "symbols_title": "非語言符號",
    "insert_symbol": "插入符號",

    # Pronunciation
    "pronunciation_title": "發音校正",
    "pinyin_label": "拼音（中文）",
    "cmu_label": "CMU 音標（英文）",

    # Queue
    "queue_title": "任務佇列",
    "queue_empty": "佇列為空",
    "queue_pending": "待處理",
    "queue_processing": "處理中",
    "queue_completed": "已完成",

    # Notifications
    "task_complete": "任務完成",
    "task_failed": "任務失敗",

    # Voice presets
    "presets_title": "語音角色預設",
    "preset_news": "新聞播報",
    "preset_story": "故事朗讀",
    "preset_assistant": "智慧助理",
    "preset_child": "童書朗讀",

    # Keyboard shortcuts
    "shortcuts_title": "鍵盤快捷鍵",
    "shortcut_generate": "Ctrl+Enter: 生成語音",
    "shortcut_play": "Space: 播放/暫停",

    # Additional page keys
    "tts_title": "文字轉語音",
    "clone_description": "上傳 3-10 秒參考音檔，使用 OmniVoice 克隆語音風格",
    "upload_ref_audio": "上傳參考音檔",
    "upload_label": "選擇音檔",
    "upload_success": "上傳成功",
    "upload_ref_first": "請先上傳參考音檔",
    "clone_target_text": "目標文字",
    "clone_placeholder": "在此輸入要使用克隆語音朗讀的文字...",
    "clone_btn": "克隆語音",
    "clone_success": "語音克隆成功",
    "omnivoice_unavailable": "OmniVoice 引擎不可用（需安裝 torch）",
    "engine_unavailable": "所選引擎不可用",
    "batch_input": "輸入文字",
    "batch_input_placeholder": "輸入一行文字...",
    "add_btn": "新增",
    "batch_upload_file": "上傳 TXT 檔案",
    "batch_file_loaded": "檔案已載入",
    "items": "項",
    "batch_queue": "待處理佇列",
    "clear_all_btn": "全部清除",
    "batch_start": "開始批次轉換",
    "batch_empty": "佇列為空，請先新增項目",
    "batch_complete": "批次轉換完成",
    "ssml_description": "使用 SSML 標籤精細控制語音合成參數",
    "ssml_templates": "SSML 模板",
    "ssml_editor_label": "SSML 編輯器",
    "ssml_generate": "生成語音",
    "ssml_empty": "請輸入 SSML 內容",
    "search_label": "搜尋",
    "search_placeholder": "輸入關鍵字搜尋...",
    "all_engines": "所有引擎",
    "filter_engine": "篩選引擎",
    "search_btn": "搜尋",
    "language_settings": "語言設定",
    "default_settings": "預設值設定",
    "general_settings": "一般設定",
    "auto_play": "自動播放",
    "save_history": "儲存歷史紀錄",
    "save_settings_btn": "儲存設定",
    "export_settings_btn": "匯出設定",
    "settings_exported": "設定已匯出",
    "import_settings_label": "匯入設定 JSON 檔案",
    "settings_imported": "設定已匯入",
    "license": "授權",
    "features": "功能特色",
    "feature_multi_engine": "多引擎支援（Edge-TTS、gTTS、OmniVoice）",
    "feature_voice_clone": "語音克隆（零樣本語音複製）",
    "feature_batch": "批次處理（多文字佇列轉換）",
    "feature_ssml": "SSML 編輯器（精細語音控制）",
    "feature_history": "歷史紀錄（搜尋、收藏、重播）",
    "feature_i18n": "多國語系介面（繁中/英文/日文）",
    "feature_dark_mode": "深色/淺色主題切換",
    "feature_export_import": "設定匯出/匯入",
    "feature_audio_preview": "即時語音預覽",
    "feature_text_stats": "文字統計與時長估算",
    "tech_stack": "技術架構",
    "usage_guide_content": (
        "### 快速開始\n\n"
        "1. 在文字框輸入要轉換的文字\n"
        "2. 選擇引擎和語音\n"
        "3. 調整速度、音調、音量\n"
        "4. 點擊「生成語音」\n"
        "5. 預覽並下載音檔"
    ),
}
