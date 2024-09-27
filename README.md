# 靜宜小幫手
[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/release/python-3115/)

- [邀請機器人](https://discord.com/application-directory/976010011937488906)

## 簡介
專為靜宜大學學生設計的聊天機器人，旨在快速解答校園生活中的各類問題。該機器人提供學術、生活、服務等多方面的支持，讓學生在校園中更便捷地獲取所需資訊。

## 前置準備
在開始使用此專案之前，請確保您已完成以下步驟：

1. 申請 Discord 機器人並保存 Token。
2. 申請「運輸資料流通服務平臺」的 API 金鑰 (API Key)。
3. 申請「氣象資料開放平臺」的 API 金鑰 (API Key)。
4. 取得 Google 憑證，並在 AI Studio 上擁有已訓練的模型。

## 設定步驟
請按照以下步驟進行設定：

1. 在專案目錄中建立 `.env` 檔案。
2. 在 `.env` 檔案中填入以下資料：
    ```env
    DISCORD_TOKEN = <您的 Discord Token>
    TDX_ID = <您的 TDX ID>
    TDX_KEY = <您的 TDX API Key>
    CWA_KEY = <您的 CWA API Key>
    ```
3. 在專案目錄下運行以下指令以安裝所需的依賴：
    ```sh
    pip install -r requirements.txt
    ```
4. 將 `client_secret.json` 憑證放入 `/api` 目錄內。
5. 運行 `main.py` 以及 `api/gs_api.py` 來啟動機器人。

## 使用說明
啟動機器人後，您可以在 Discord 伺服器中與其互動。機器人將根據您輸入的指令提供相應的資訊和服務。

## 貢獻
歡迎對此專案進行貢獻。請提交 Pull Request 或創建 Issue 來提出您的建議和改進。

## 聯絡方式
如有任何問題或建議，請聯絡專案維護者。
