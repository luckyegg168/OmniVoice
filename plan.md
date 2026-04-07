# OmniVoice TTS App — 實作計畫 (plan.md)

## 1. 專案概述

OmniVoice TTS App 是一款基於 **NiceGUI** 框架的桌面/Web 文字轉語音應用程式，
後端整合 **k2-fsa/OmniVoice** 和 **Edge-TTS** 雙引擎，支援 600+ 語言，
提供語音克隆、語音設計、批次轉換、SSML 編輯等 30 項實用功能。

## 2. 技術架構

```
┌──────────────────────────────────────────────────────────┐
│                    NiceGUI Frontend                       │
│  ┌───────┐ ┌───────┐ ┌───────┐ ┌───────┐ ┌───────────┐  │
│  │ TTS   │ │ Voice │ │ Batch │ │ SSML  │ │ History   │  │
│  │ Page  │ │ Clone │ │ Page  │ │ Editor│ │ /Settings │  │
│  └───┬───┘ └───┬───┘ └───┬───┘ └───┬───┘ └─────┬─────┘  │
│      └─────────┴─────────┴─────────┴───────────┘         │
│                          │                                │
│                    ┌─────▼─────┐                          │
│                    │  App Core │                          │
│                    └─────┬─────┘                          │
│                          │                                │
│         ┌────────────────┼────────────────┐               │
│    ┌────▼────┐     ┌─────▼─────┐   ┌─────▼─────┐        │
│    │OmniVoice│     │ Edge-TTS  │   │  gTTS     │        │
│    │ Engine  │     │  Engine   │   │  Engine   │        │
│    └─────────┘     └───────────┘   └───────────┘        │
└──────────────────────────────────────────────────────────┘
```

## 3. 30 項功能清單

| # | 功能 | 類別 | 優先級 |
|---|------|------|--------|
| 1 | 文字轉語音（Text-to-Speech） | 核心 | P0 |
| 2 | Edge-TTS 多引擎支援 | 核心 | P0 |
| 3 | gTTS 引擎支援 | 核心 | P0 |
| 4 | 多國語系 UI（zh-TW 預設） | 核心 | P0 |
| 5 | 語音克隆（Voice Cloning） | 進階 | P1 |
| 6 | 語音設計（Voice Design） | 進階 | P1 |
| 7 | SSML 編輯器 | 進階 | P1 |
| 8 | 批次文字轉語音 | 生產力 | P1 |
| 9 | 語音速度調節 | 控制 | P0 |
| 10 | 語音音調調節 | 控制 | P0 |
| 11 | 語音音量調節 | 控制 | P0 |
| 12 | 即時預覽播放 | UX | P0 |
| 13 | 音檔下載（WAV/MP3） | 核心 | P0 |
| 14 | 歷史紀錄管理 | 生產力 | P1 |
| 15 | 收藏文字片段 | 生產力 | P1 |
| 16 | 語音角色預設 | UX | P1 |
| 17 | 深色/淺色主題切換 | UX | P1 |
| 18 | 文字字數/預估時長顯示 | UX | P2 |
| 19 | 文字檔匯入（TXT/SRT） | 生產力 | P1 |
| 20 | SRT 字幕生成 | 進階 | P2 |
| 21 | 非語言符號插入 | 進階 | P2 |
| 22 | 發音校正（拼音/CMU） | 進階 | P2 |
| 23 | 音檔波形可視化 | UX | P2 |
| 24 | 鍵盤快捷鍵 | UX | P2 |
| 25 | 匯出設定/匯入設定 | 生產力 | P2 |
| 26 | 多分頁工作區 | UX | P2 |
| 27 | 佇列任務管理 | 生產力 | P2 |
| 28 | 文字預處理（數字/縮寫展開） | 進階 | P2 |
| 29 | 系統通知（任務完成） | UX | P2 |
| 30 | 關於頁面 & 使用說明 | 資訊 | P2 |

## 4. 實作階段

### Phase 1: 基礎架構 (Core)
- 專案結構建置
- i18n 多國語系系統
- TTS 引擎抽象層
- Edge-TTS & gTTS 引擎實作
- 基本 UI 框架

### Phase 2: 核心功能 (Features)
- 全部 P0 功能
- Edge-TTS 語音列表
- 播放/下載功能
- 速度/音調/音量控制

### Phase 3: 進階功能 (Advanced)
- 語音克隆（OmniVoice）
- 語音設計
- SSML 編輯器
- 批次處理
- 歷史紀錄

### Phase 4: 品質 & 發佈 (Ship)
- Ruff 格式化
- Pytest 測試
- 效能優化
- GitHub 推送

## 5. 目錄結構

```
OmniVoice/
├── app/
│   ├── __init__.py
│   ├── main.py              # 入口
│   ├── config.py             # 配置
│   ├── core/
│   │   ├── __init__.py
│   │   ├── tts_engine.py     # 引擎抽象
│   │   ├── edge_tts_engine.py
│   │   ├── gtts_engine.py
│   │   ├── omnivoice_engine.py
│   │   └── audio_utils.py
│   ├── i18n/
│   │   ├── __init__.py
│   │   ├── translations.py
│   │   ├── zh_tw.py
│   │   ├── en.py
│   │   └── ja.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── tts_request.py
│   │   └── history.py
│   ├── pages/
│   │   ├── __init__.py
│   │   ├── tts_page.py
│   │   ├── voice_clone_page.py
│   │   ├── batch_page.py
│   │   ├── ssml_page.py
│   │   ├── history_page.py
│   │   ├── settings_page.py
│   │   └── about_page.py
│   ├── components/
│   │   ├── __init__.py
│   │   ├── audio_player.py
│   │   ├── voice_selector.py
│   │   ├── text_stats.py
│   │   └── theme_toggle.py
│   └── storage/
│       ├── __init__.py
│       └── db.py
├── tests/
│   ├── __init__.py
│   ├── test_tts_engine.py
│   ├── test_i18n.py
│   ├── test_models.py
│   └── test_audio_utils.py
├── output/                   # 生成音檔
├── plan.md
├── spec.md
├── pyproject.toml
├── README.md
└── .gitignore
```
