# 電腦零件價格查詢系統

這是一個基於 MCP (Model Context Protocol) 的電腦零件價格查詢系統，提供即時的零件價格資訊和組裝建議。

## 功能特點

1. **零件查詢**
   - 依類別查詢零件（CPU、GPU 等）
   - 依價格範圍搜尋零件
   - 顯示詳細規格和價格資訊

2. **組裝建議**
   - 根據預算提供均衡的配備建議
   - 自動計算六大主要配件的分配
   - 顯示總價和剩餘預算

3. **價格追蹤**
   - 顯示價格最後更新時間
   - 即時價格資訊

## 環境設置

### 前置需求
- Python 3.9 或更高版本
- Conda 或 uv 套件管理器

### 安裝步驟

1. **使用 Conda 設置環境**
   ```bash
   # 創建新環境
   conda create -n pc-parts python=3.9
   
   # 啟用環境
   conda activate pc-parts
   
   # 安裝必要套件
   pip install "mcp[cli]"
   ```

2. **使用 uv 設置環境**
   ```bash
   # 創建新專案
   uv init pc-parts
   cd pc-parts
   
   # 安裝必要套件
   uv add "mcp[cli]"
   ```

## 使用方式

1. **啟動伺服器**
   ```bash
   python pc_parts_server.py
   ```

2. **使用 MCP Inspector 測試**
   ```bash
   mcp dev pc_parts_server.py
   ```

3. **整合到 Claude Desktop**
   ```bash
   mcp install pc_parts_server.py
   ```

## 主要功能說明

### 1. 查詢零件
- 使用 `list_parts_by_category` 工具查詢特定類別的所有零件
- 支援的類別：CPU、GPU、主機板、記憶體、電源供應器、機殼

### 2. 價格搜尋
- 使用 `find_parts_by_price_range` 工具搜尋特定價格範圍的零件
- 輸入最低和最高價格即可獲得符合條件的零件清單

### 3. 組裝建議
- 使用 `suggest_pc_build` 工具獲取組裝建議
- 輸入總預算，系統會自動計算六大主要配件的均衡分配
- 建議預算至少 NT$ 20,000 以上

## 資料庫說明

系統使用 SQLite 資料庫（`pc_parts.db`）儲存零件資訊，包含：
- 零件類別
- 品名
- 品牌
- 價格
- 規格
- 最後更新時間

## 注意事項

1. 確保資料庫文件 `pc_parts.db` 存在於正確路徑
2. 價格資訊會定期更新，請注意查看最後更新時間
3. 組裝建議僅供參考，實際購買時請考慮個人需求和市場狀況

## 技術支援

如有任何問題或需要協助，請：
1. 檢查錯誤訊息
2. 確認環境設置是否正確
3. 確認資料庫連接是否正常
