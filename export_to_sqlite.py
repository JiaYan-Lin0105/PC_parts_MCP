import sqlite3
from pc_parts_server import pc_parts_db, PCPart

# 建立資料庫連線
conn = sqlite3.connect('pc_parts.db')
c = conn.cursor()

# 建立 parts 資料表
c.execute('''
CREATE TABLE IF NOT EXISTS parts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category TEXT,
    name TEXT,
    brand TEXT,
    price REAL,
    specs TEXT,
    last_updated TEXT
)
''')

# 清空舊資料
c.execute('DELETE FROM parts')

# 寫入所有零件
for category, parts in pc_parts_db.items():
    for part in parts:
        c.execute(
            'INSERT INTO parts (category, name, brand, price, specs, last_updated) VALUES (?, ?, ?, ?, ?, ?)',
            (
                part.category,
                part.name,
                part.brand,
                part.price,
                str(part.specs),  # specs 以字串存入
                part.last_updated
            )
        )

conn.commit()
conn.close()
print("所有零件已寫入 pc_parts.db")