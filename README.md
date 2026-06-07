# OmniVoice TTS App

🎙️ 多引擎多國語系文字轉語音應用程式

## 功能特色

- 🌐 **多語系介面** — 繁體中文(預設)、English、日本語、한국어、简体中文
- 🔊 **多引擎支援** — Edge-TTS、gTTS、OmniVoice (600+ 語言)
- 🎭 **語音克隆** — 3-10 秒參考音檔即可克隆語音
- 📝 **SSML 編輯器** — 精細控制語音合成
- 📦 **批次處理** — TXT/SRT 檔案批次轉語音
- 🎛️ **進階控制** — 速度、音調、音量即時調整
- 📊 **歷史紀錄** — 搜尋、收藏、重播
- 🌙 **深色主題** — 護眼深色/淺色切換

## 快速開始

```bash
# 安裝依賴（需先安裝 uv: https://docs.astral.sh/uv/#installation）
uv sync

# 啟動應用
uv run python -m app.main
```

開啟瀏覽器訪問 http://localhost:8080

## 開發

```bash
# 安裝開發依賴
uv sync

# 程式碼檢查
uv run ruff check app/ tests/

# 執行測試
uv run pytest --cov=app tests/
```

## 技術棧

- **UI**: NiceGUI (Python → Web)
- **TTS**: Edge-TTS / gTTS / OmniVoice
- **語言**: Python 3.10+
- **授權**: MIT

## 30 項功能

1. 文字轉語音 (Text-to-Speech)
2. Edge-TTS 引擎
3. gTTS 引擎
4. 多國語系 UI (zh-TW 預設)
5. 語音克隆 (Voice Cloning)
6. 語音設計 (Voice Design)
7. SSML 編輯器
8. 批次轉語音
9. 語音速度調節
10. 語音音調調節
11. 語音音量調節
12. 即時預覽播放
13. 音檔下載 (WAV/MP3)
14. 歷史紀錄管理
15. 收藏文字片段
16. 語音角色預設
17. 深色/淺色主題
18. 文字字數/預估時長
19. 文字檔匯入 (TXT/SRT)
20. SRT 字幕生成
21. 非語言符號插入
22. 發音校正 (拼音/CMU)
23. 音檔波形可視化
24. 鍵盤快捷鍵
25. 匯出/匯入設定
26. 多分頁工作區
27. 佇列任務管理
28. 文字預處理 (數字/縮寫展開)
29. 系統通知 (任務完成)
30. 關於頁面 & 使用說明
