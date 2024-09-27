# 靜宜小幫手

## 簡介
> 專為靜宜大學學生設計的聊天機器人，快速解答校園生活中的各類問題，提供學術、生活、服務等多方面的支持，讓學生在校園中更便捷地獲取所需資訊。

## 前置
- 申請 Discord 機器人並保存 Token。
- 申請「運輸資料流通服務平臺」的 API 金鑰 (API Key)。
- 申請「氣象資料開放平臺」的 API 金鑰 (API Key)。
- 取得 Google 憑證，並在 AI Studio 上擁有已訓練的模型。

## 設定
1. 在專案目錄中建立 .env 檔案。
2. 在 .env 檔案中填入以下資料：
    ```
    DISCORD_TOKEN = 
    TDX_ID = 
    TDX_KEY = 
    CWA_KEY = 
    ```
3. 在專案目錄下運行以下指令：
    ```
    pip install -r requirements.txt
    ```
4. 將 client_secret.json 憑證放入 `/api` 目錄內。
4. 運行 `main.py` 以及 `api/gs_api.py`。