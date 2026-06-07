# OmniVoice TTS — Agent Guide

## Project Overview

Multi-engine TTS web app built with NiceGUI. Supports Edge-TTS, gTTS, and OmniVoice (voice cloning) engines. Features batch processing, SSML editing, history management, and 5-language i18n.

## Architecture

```
app/
├── main.py              # App entry point, engine init, page routing
├── config.py            # App configuration & constants
├── core/                # TTS engine implementations
│   ├── tts_engine.py        # Abstract base (TTSOption, format helpers)
│   ├── edge_tts_engine.py   # Microsoft Edge-TTS
│   ├── gtts_engine.py       # Google gTTS
│   └── omnivoice_engine.py  # OmniVoice voice clone
├── pages/               # UI pages
│   ├── tts_page.py          # Text-to-speech main page
│   ├── voice_clone_page.py  # Voice cloning
│   ├── batch_page.py        # Batch conversion
│   ├── ssml_page.py         # SSML editor
│   ├── history_page.py      # History & favorites
│   ├── settings_page.py     # Settings (locale, theme, defaults)
│   └── about_page.py        # About & engine status
├── components/          # Reusable UI components
│   ├── audio_player.py     # Audio playback
│   ├── text_stats.py       # Character/word/duration stats
│   ├── theme_toggle.py     # Dark/light theme switch
│   └── voice_selector.py   # Engine+voice picker
├── i18n/                # Translations (5 locales)
│   ├── translations.py     # Registry & t() helper
│   ├── zh_tw.py, zh_cn.py, en.py, ja.py, ko.py
├── models/              # Pydantic data models
│   └── tts_request.py, tts_result.py, voice_info.py, history_record.py
└── storage/             # JSON file persistence
    └── json_io.py, history_storage.py
```

## Key Conventions

| Rule | Guideline |
|------|-----------|
| **i18n** | All user-facing strings via `t("key")`; add keys to all locale files |
| **TTS Engines** | Subclass `BaseTTSEngine`; implement `synthesize()` returning `TTSResult` |
| **State** | Pages use local `dict` state, not global singletons |
| **Storage** | Pure JSON via `JsonIO`; history in `storage/history.json` |
| **Models** | Pydantic frozen dataclasses in `app/models/` |
| **Pages** | Each page = one function receiving `engines: dict`, registered in `main.py` |
| **Tests** | Pytest in `tests/`; no mocks, pure unit tests on logic |

## Testing

```bash
uv run pytest -v         # Run all tests
uv run pytest tests/test_i18n.py -v # Locale-specific tests
```

## Adding a New Locale

1. Create `app/i18n/xx.py` with `XX_TRANSLATIONS` dict (all keys matching `zh_tw.py`)
2. Register in `app/i18n/translations.py` (`SUPPORTED_LOCALES` + `_ALL_TRANSLATIONS`)
3. Add to settings page locale selector in `app/pages/settings_page.py`
4. Update `feature_i18n` string in all locale files
5. Add tests in `tests/test_i18n.py`

## Adding a New TTS Engine

1. Create `app/core/xxx_engine.py` subclassing `BaseTTSEngine`
2. Implement `synthesize()` method
3. Register in `app/main.py` engines dict
