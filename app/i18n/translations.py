"""Translation system for multi-locale support."""

from __future__ import annotations

from app.i18n.en import EN_TRANSLATIONS
from app.i18n.ja import JA_TRANSLATIONS
from app.i18n.ko import KO_TRANSLATIONS
from app.i18n.zh_cn import ZH_CN_TRANSLATIONS
from app.i18n.zh_tw import ZH_TW_TRANSLATIONS

SUPPORTED_LOCALES: dict[str, str] = {
    "zh-TW": "繁體中文",
    "zh-CN": "简体中文",
    "en": "English",
    "ja": "日本語",
    "ko": "한국어",
}

_ALL_TRANSLATIONS: dict[str, dict[str, str]] = {
    "zh-TW": ZH_TW_TRANSLATIONS,
    "zh-CN": ZH_CN_TRANSLATIONS,
    "en": EN_TRANSLATIONS,
    "ja": JA_TRANSLATIONS,
    "ko": KO_TRANSLATIONS,
}

# Current locale state
_current_locale: str = "zh-TW"


def set_locale(locale: str) -> None:
    """Set the current UI locale."""
    global _current_locale
    if locale in SUPPORTED_LOCALES:
        _current_locale = locale


def get_locale() -> str:
    """Get the current UI locale."""
    return _current_locale


def t(key: str, locale: str | None = None) -> str:
    """Translate a key to the current or specified locale.

    Falls back to English, then returns the key itself.
    """
    loc = locale or _current_locale
    translations = _ALL_TRANSLATIONS.get(loc, {})
    if key in translations:
        return translations[key]
    # Fallback to English
    en = _ALL_TRANSLATIONS.get("en", {})
    if key in en:
        return en[key]
    return key
