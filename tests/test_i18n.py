"""Tests for i18n translations."""

from __future__ import annotations

from app.i18n.translations import get_locale, set_locale, t


class TestTranslations:
    def setup_method(self):
        set_locale("zh-TW")

    def test_default_locale(self):
        assert get_locale() == "zh-TW"

    def test_set_locale_en(self):
        set_locale("en")
        assert get_locale() == "en"

    def test_set_locale_ja(self):
        set_locale("ja")
        assert get_locale() == "ja"

    def test_invalid_locale_fallback(self):
        set_locale("xx-YY")
        # Should fall back to zh-TW
        assert get_locale() == "zh-TW"

    def test_translate_zh_tw(self):
        set_locale("zh-TW")
        result = t("app_title")
        assert "OmniVoice" in result

    def test_translate_en(self):
        set_locale("en")
        result = t("app_title")
        assert "OmniVoice" in result

    def test_missing_key_returns_key(self):
        result = t("nonexistent_key_xyz")
        assert result == "nonexistent_key_xyz"

    def test_navigation_keys_exist(self):
        for key in [
            "nav_tts",
            "nav_clone",
            "nav_batch",
            "nav_ssml",
            "nav_history",
            "nav_settings",
            "nav_about",
        ]:
            result = t(key)
            assert result != key, f"Missing translation for {key}"

    def test_en_has_all_required_keys(self):
        set_locale("en")
        required = ["app_title", "generate_btn", "settings_title", "history_title"]
        for key in required:
            assert t(key) != key, f"EN missing key: {key}"

    def test_set_locale_zh_cn(self):
        set_locale("zh-CN")
        assert get_locale() == "zh-CN"
        result = t("app_title")
        assert "OmniVoice" in result

    def test_set_locale_ko(self):
        set_locale("ko")
        assert get_locale() == "ko"
        result = t("app_title")
        assert "OmniVoice" in result

    def test_new_locales_have_all_section_keys(self):
        """Verify zh-CN and ko have all keys from the zh-TW master locale."""
        set_locale("zh-TW")
        master_keys = {
            k
            for k, v in __import__(
                "app.i18n.zh_tw", fromlist=["ZH_TW_TRANSLATIONS"]
            ).ZH_TW_TRANSLATIONS.items()
        }

        for locale_code, mod_name in [("zh-CN", "zh_cn"), ("ko", "ko"), ("ja", "ja")]:
            set_locale(locale_code)
            mod = __import__(f"app.i18n.{mod_name}", fromlist=["translations"])
            locale_keys = set(getattr(mod, f"{mod_name.upper()}_TRANSLATIONS").keys())
            missing = master_keys - locale_keys
            assert not missing, f"{locale_code} missing keys: {missing}"
