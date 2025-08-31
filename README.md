# Management Fee Query (Public)

這是「公開查詢版」的 Streamlit App 專案，預載 `data/fee_data_normalized.xlsx`。
任何人打開網址即可查詢與下載**單筆** PDF 收據（僅針對已繳款資料）。

## 一鍵部署步驟（Streamlit Cloud）
1. 建立一個 GitHub 倉庫，將本專案全部檔案上傳。
2. 前往 [share.streamlit.io](https://share.streamlit.io) 用 GitHub 帳號登入。
3. 建立新 App → 選擇你的倉庫與分支，入口檔設為 `app.py`。
4. 等待部署完成，取得公開網址（任何人可開）。

> 若要更新資料，只需在同倉庫的 `data/fee_data_normalized.xlsx` 置換新版，重新部署或等待自動重新整理即可。
