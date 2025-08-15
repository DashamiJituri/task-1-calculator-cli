import sqlite3
from datetime import datetime

def save_order(items, total, table, billing_id):
    conn = sqlite3.connect('db/restaurant.db')
    c = conn.cursor()
    
    # Ensure table exists (safe on multiple calls)
    c.execute('''
        CREATE TABLE IF NOT EXISTS bills (
            id TEXT PRIMARY KEY,
            table_number TEXT,
            items TEXT,
            total INTEGER,
            timestamp TEXT
        )
    ''')

    item_summary = ", ".join([f"{item} x {qty}" for item, (qty, _) in items.items()])
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    c.execute('''
        INSERT INTO bills (id, table_number, items, total, timestamp)
        VALUES (?, ?, ?, ?, ?)
    ''', (billing_id, table, item_summary, total, timestamp))

    conn.commit()
    conn.close()
