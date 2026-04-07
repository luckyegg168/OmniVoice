# OmniVoice TTS App — 技術規格 (spec.md)

## 1. 系統需求

| 項目 | 規格 |
|------|------|
| Python | >= 3.10 |
| OS | Windows / macOS / Linux |
| RAM | >= 4 GB (Edge-TTS/gTTS), >= 8 GB (OmniVoice) |
| GPU | 選用 (OmniVoice 加速) |
| 瀏覽器 | Chrome / Edge / Firefox (最新版) |

## 2. 核心依賴

| 套件 | 版本 | 用途 |
|------|------|------|
| nicegui | >= 2.0 | Web UI 框架 |
| edge-tts | >= 6.1 | 微軟 Edge TTS 引擎 |
| gTTS | >= 2.5 | Google TTS 引擎 |
| pydantic | >= 2.0 | 資料模型驗證 |
| aiofiles | >= 23.0 | 非同步檔案操作 |
| mutagen | >= 1.47 | 音檔 metadata |

### 選用依賴 (OmniVoice)
| 套件 | 版本 | 用途 |
|------|------|------|
| omnivoice | >= 0.1.3 | 600+ 語言零次語音克隆 |
| torch | >= 2.0 | 深度學習推論 |
| torchaudio | >= 2.0 | 音訊處理 |

## 3. API 設計

### 3.1 TTS Engine 抽象介面

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass(frozen=True)
class TTSRequest:
    text: str
    voice: str
    language: str = "zh-TW"
    speed: float = 1.0
    pitch: float = 0.0
    volume: float = 1.0
    output_format: str = "mp3"

@dataclass(frozen=True)
class TTSResult:
    audio_path: str
    duration_seconds: float
    sample_rate: int
    engine: str

class TTSEngine(ABC):
    @abstractmethod
    async def synthesize(self, request: TTSRequest) -> TTSResult: ...

    @abstractmethod
    async def list_voices(self, language: str | None = None) -> list[dict]: ...

    @abstractmethod
    def name(self) -> str: ...
```

### 3.2 多國語系介面

```python
# 支援語系
SUPPORTED_LOCALES = {
    "zh-TW": "繁體中文",
    "en": "English",
    "ja": "日本語",
    "ko": "한국어",
    "zh-CN": "简体中文",
}

# 翻譯鍵值範例
translations = {
    "app_title": {"zh-TW": "OmniVoice 語音生成", "en": "OmniVoice TTS"},
    "generate": {"zh-TW": "生成語音", "en": "Generate"},
    ...
}
```

## 4. 頁面規格

### 4.1 TTS 主頁 (`/`)
- 文字輸入區（支援多行、字數統計）
- 引擎選擇（Edge-TTS / gTTS / OmniVoice）
- 語音選擇（依引擎動態載入）
- 速度 / 音調 / 音量滑桿
- 生成按鈕、預覽播放、下載
- 預估時長顯示

### 4.2 語音克隆頁 (`/clone`)
- 參考音檔上傳（3-10 秒）
- 參考文字輸入（選填）
- 目標文字輸入
- 生成 & 播放

### 4.3 批次處理頁 (`/batch`)
- 文字檔上傳（TXT / SRT）
- 逐行或逐句分割
- 批次佇列管理
- 進度指示器
- 打包下載

### 4.4 SSML 編輯器 (`/ssml`)
- CodeMirror / 程式碼編輯器
- SSML 標籤快捷插入
- 即時預覽
- 語法驗證

### 4.5 歷史紀錄 (`/history`)
- 表格顯示（時間、文字、引擎、音檔）
- 搜尋 & 篩選
- 重新播放 / 下載 / 刪除
- 收藏功能

### 4.6 設定頁 (`/settings`)
- 語系切換
- 深色 / 淺色主題
- 預設引擎
- 預設語音
- 輸出目錄
- 匯出 / 匯入設定

### 4.7 關於頁 (`/about`)
- 版本資訊
- 引擎狀態
- 使用說明
- 授權資訊

## 5. 資料模型

### History Record
```python
@dataclass(frozen=True)
class HistoryRecord:
    id: str                  # UUID
    timestamp: str           # ISO 8601
    text: str
    engine: str
    voice: str
    language: str
    speed: float
    pitch: float
    volume: float
    audio_path: str
    duration_seconds: float
    is_favorite: bool = False
```

### App Settings
```python
@dataclass(frozen=True)
class AppSettings:
    locale: str = "zh-TW"
    theme: str = "dark"
    default_engine: str = "edge-tts"
    default_voice: str = "zh-TW-HsiaoChenNeural"
    output_dir: str = "./output"
    max_history: int = 500
```

## 6. 非功能需求

| 項目 | 目標 |
|------|------|
| 啟動時間 | < 3 秒 |
| TTS 延遲 (Edge-TTS) | < 2 秒 (100 字) |
| 同時使用者 | 1-5 (本機部署) |
| 測試覆蓋率 | >= 80% |
| Ruff 檢查 | 零 error |
| 無障礙 | 鍵盤可操作 |

## 7. 安全考量

- 不存儲使用者密碼或 API Key 於原始碼
- 檔案上傳限制大小 (10 MB)
- 輸入文字長度限制 (10,000 字)
- XSS 防護（NiceGUI 內建）
- 路徑遍歷防護（音檔存取驗證）
