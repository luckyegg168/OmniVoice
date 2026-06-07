"""Voice selector component with language grouping."""

from __future__ import annotations

from nicegui import ui

from app.i18n.translations import t
from app.models.tts_request import VoiceInfo

# ── Language code → friendly name ──
_LANG_NAMES: dict[str, str] = {
    "af": "Afrikaans",
    "am": "አማርኛ",
    "ar": "العربية",
    "az": "Azərbaycanca",
    "bg": "Български",
    "bn": "বাংলা",
    "ca": "Català",
    "cs": "Čeština",
    "cy": "Cymraeg",
    "da": "Dansk",
    "de": "Deutsch",
    "el": "Ελληνικά",
    "en": "English",
    "es": "Español",
    "et": "Eesti",
    "eu": "Euskara",
    "fa": "فارسی",
    "fi": "Suomi",
    "fil": "Filipino",
    "fr": "Français",
    "ga": "Gaeilge",
    "gl": "Galego",
    "gu": "ગુજરાતી",
    "he": "עברית",
    "hi": "हिन्दी",
    "hr": "Hrvatski",
    "hu": "Magyar",
    "hy": "Հայերեն",
    "id": "Indonesia",
    "is": "Íslenska",
    "it": "Italiano",
    "ja": "日本語",
    "jv": "Jawa",
    "ka": "ქართული",
    "kk": "Қазақ",
    "km": "ខ្មែរ",
    "kn": "ಕನ್ನಡ",
    "ko": "한국어",
    "lo": "ລາວ",
    "lt": "Lietuvių",
    "lv": "Latviešu",
    "mk": "Македонски",
    "ml": "മലയാളം",
    "mn": "Монгол",
    "mr": "मराठी",
    "ms": "Melayu",
    "mt": "Malti",
    "my": "မြန်မာ",
    "nb": "Norsk Bokmål",
    "ne": "नेपाली",
    "nl": "Nederlands",
    "pl": "Polski",
    "pt": "Português",
    "ro": "Română",
    "ru": "Русский",
    "si": "සිංහල",
    "sk": "Slovenčina",
    "sl": "Slovenščina",
    "so": "Soomaali",
    "sq": "Shqip",
    "sr": "Српски",
    "sv": "Svenska",
    "sw": "Kiswahili",
    "ta": "தமிழ்",
    "te": "తెలుగు",
    "th": "ไทย",
    "tr": "Türkçe",
    "uk": "Українська",
    "ur": "اردو",
    "uz": "Oʻzbek",
    "vi": "Tiếng Việt",
    "yue": "粵語",
    "zh": "中文",
}


def _lang_code(locale: str) -> str:
    """Extract language code from locale string (e.g. 'zh-TW' → 'zh')."""
    return locale.split("-")[0].lower()


def _lang_display(code: str) -> str:
    """Get user-friendly language name from a 2-letter code."""
    return _LANG_NAMES.get(code, code.upper())


def voice_selector(
    voices: list[VoiceInfo],
    value: str = "",
    on_change=None,
) -> dict:
    """Create a language-grouped voice selector.

    Renders two chained dropdowns:
      1. Language — filters voices by language
      2. Voice    — shows only voices matching the selected language

    Returns a dict with keys:
        'lang_select':  the language ``ui.select``
        'voice_select': the voice ``ui.select``
        'update(voices, value)': refresh the widget with a new voice list
    """
    # ── Language index ──
    lang_index: dict[str, list[VoiceInfo]] = {}

    def _rebuild(src: list[VoiceInfo]) -> None:
        lang_index.clear()
        for v in src:
            code = _lang_code(v.language)
            lang_index.setdefault(code, []).append(v)

    _rebuild(voices)

    sorted_langs = sorted(lang_index.keys())

    # ── Resolve initial language ──
    def _resolve_lang() -> str:
        if value:
            match = next((_lang_code(v.language) for v in voices if v.id == value), "")
            if match in lang_index:
                return match
        if voices:
            code = _lang_code(voices[0].language)
            if code in lang_index:
                return code
        return sorted_langs[0] if sorted_langs else ""

    init_lang = _resolve_lang()

    # ── Language dropdown ──
    lang_opts = {code: _lang_display(code) for code in sorted_langs}
    lang_select = ui.select(
        options=lang_opts,
        value=init_lang or None,
        label=t("language_label"),
        on_change=lambda _e: _sync_voice(),
    ).classes("w-44")

    # ── Voice dropdown (filtered by language) ──
    def _sync_voice() -> None:
        lang: str = lang_select.value or ""
        pool = lang_index.get(lang, [])
        opts = {v.id: v.name for v in pool}
        voice_select.options = opts
        if pool and voice_select.value not in opts:
            voice_select.value = pool[0].id
        voice_select.update()

    pool = lang_index.get(init_lang, [])
    voice_opts = {v.id: v.name for v in pool}
    voice_val = value if value in voice_opts else (pool[0].id if pool else None)

    voice_select = ui.select(
        options=voice_opts,
        value=voice_val,
        label=t("voice_label"),
        on_change=on_change,
    ).classes("w-80")

    # ── Public update API ──
    def update(new_voices: list[VoiceInfo], new_value: str = "") -> None:
        nonlocal voices, value
        voices = new_voices
        value = new_value
        _rebuild(new_voices)
        sorted_l = sorted(lang_index.keys())
        lang_select.options = {code: _lang_display(code) for code in sorted_l}
        if sorted_l:
            lang_select.value = sorted_l[0]
        else:
            lang_select.value = None
            voice_select.options = {}
            voice_select.value = None
        _sync_voice()

    return {
        "lang_select": lang_select,
        "voice_select": voice_select,
        "update": update,
    }
