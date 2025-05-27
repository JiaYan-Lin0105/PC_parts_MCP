from dataclasses import dataclass
from typing import List, Optional
from mcp.server.fastmcp import FastMCP
import json
from datetime import datetime
import sqlite3
import ast  # 用於將 specs 字串轉回 dict
import os
# 建立 MCP 伺服器
mcp = FastMCP("PC Parts Price Checker")

# 定義零件資料結構
@dataclass
class PCPart:
    category: str
    name: str
    brand: str
    price: float
    specs: dict
    last_updated: str

def load_parts_from_db(db_path=None):
    if db_path is None:
        here = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(here, "pc_parts.db")
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('SELECT category, name, brand, price, specs, last_updated FROM parts')
    rows = c.fetchall()
    conn.close()

    db = {}
    for row in rows:
        category, name, brand, price, specs, last_updated = row
        part = PCPart(
            category=category,
            name=name,
            brand=brand,
            price=price,
            specs=ast.literal_eval(specs),  # 將字串轉回 dict
            last_updated=last_updated
        )
        if category.lower() not in db:
            db[category.lower()] = []
        db[category.lower()].append(part)
    return db

# 用 SQLite 取代原本的 pc_parts_db
pc_parts_db = load_parts_from_db()

# 工具：查詢特定類別的所有零件
@mcp.tool()
def list_parts_by_category(category: str) -> str:
    """列出指定類別的所有零件
    
    Args:
        category: 零件類別（cpu 或 gpu）
    
    Returns:
        該類別所有零件的詳細資訊
    """
    category = category.lower()
    if category not in pc_parts_db:
        return f"找不到類別：{category}。可用類別：{', '.join(pc_parts_db.keys())}"
    
    parts = pc_parts_db[category]
    result = f"【{category.upper()} 清單】\n"
    for part in parts:
        result += f"\n品名：{part.name}"
        result += f"\n品牌：{part.brand}"
        result += f"\n價格：NT$ {part.price:,}"
        result += f"\n規格：{json.dumps(part.specs, ensure_ascii=False, indent=2)}"
        result += f"\n最後更新：{part.last_updated}"
        result += "\n" + "-"*30 + "\n"
    
    return result

# 工具：搜尋特定價格範圍的零件
@mcp.tool()
def find_parts_by_price_range(min_price: float, max_price: float) -> str:
    """搜尋特定價格範圍內的零件
    
    Args:
        min_price: 最低價格
        max_price: 最高價格
    
    Returns:
        符合價格範圍的零件清單
    """
    results = []
    for category, parts in pc_parts_db.items():
        for part in parts:
            if min_price <= part.price <= max_price:
                results.append(part)
    
    if not results:
        return f"找不到價格在 NT$ {min_price:,} 到 NT$ {max_price:,} 範圍內的零件"
    
    result_str = f"價格範圍 NT$ {min_price:,} 到 NT$ {max_price:,} 的零件：\n"
    for part in results:
        result_str += f"\n類別：{part.category}"
        result_str += f"\n品名：{part.name}"
        result_str += f"\n品牌：{part.brand}"
        result_str += f"\n價格：NT$ {part.price:,}"
        result_str += "\n" + "-"*30 + "\n"
    
    return result_str

# 工具：建議配備組合
@mcp.tool()
def suggest_pc_build(budget: float) -> str:
    """根據預算建議電腦配備組合（六大類均衡分配）
    
    Args:
        budget: 總預算
    
    Returns:
        建議的配備組合
    """
    if budget < 20000:
        return "預算過低，建議至少 NT$ 20,000 以上才能組裝基本配備"

    # 六大類均分預算
    categories = ["cpu", "gpu", "motherboard", "ram", "psu", "case"]
    per_part_budget = budget / len(categories)
    selected_parts = {}
    total = 0

    for cat in categories:
        # 找出不超過預算且價格最高的零件
        candidates = [part for part in pc_parts_db[cat] if part.price <= per_part_budget]
        if candidates:
            best = max(candidates, key=lambda p: p.price)
        else:
            # 若無法在預算內找到，則選最便宜的
            best = min(pc_parts_db[cat], key=lambda p: p.price)
        selected_parts[cat] = best
        total += best.price

    result = f"預算 NT$ {budget:,} 的建議配備：\n\n"
    for cat in categories:
        part = selected_parts[cat]
        result += f"{part.category}：\n"
        result += f"- {part.name}（{part.brand}）\n"
        result += f"- 價格：NT$ {part.price:,}\n\n"

    result += f"六大主要配件總價：NT$ {total:,}\n"
    result += f"剩餘預算：NT$ {budget - total:,}\n"
    result += "（建議剩餘預算可用於購買儲存裝置、散熱器等其他配件）"

    return result

# 資源：取得價格更新時間
@mcp.resource("file:///price/last_update")
def get_price_update_time() -> str:
    """取得價格的最後更新時間"""
    latest_update = "1970-01-01"
    for parts in pc_parts_db.values():
        for part in parts:
            if part.last_updated > latest_update:
                latest_update = part.last_updated
    return f"價格最後更新時間：{latest_update}"
if __name__ == "__main__":
    # 默認 transport="stdio"，會監聽 stdin/stdout
    mcp.run()
    