import sqlite3
import pandas as pd

# Load the CSV
menu_df = pd.read_csv("data/menu.csv")

# Connect to the SQLite DB
conn = sqlite3.connect("db/restaurant.db")
c = conn.cursor()

# Create table
c.execute('''
    CREATE TABLE IF NOT EXISTS menu (
        id INTEGER PRIMARY KEY,
        name TEXT,
        price INTEGER
    )
''')

# Clear any old data
c.execute("DELETE FROM menu")

# Insert from CSV
for _, row in menu_df.iterrows():
    c.execute("INSERT INTO menu (id, name, price) VALUES (?, ?, ?)", 
              (int(row["id"]), row["name"], int(row["price"])))

conn.commit()
conn.close()

print("✅ Menu table created in restaurant.db")
