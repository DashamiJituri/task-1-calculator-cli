import streamlit as st
import os
import json
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt

st.title("📊 Restaurant Billing Analytics Dashboard")

# Folder location
folder = "data/sample_bills"
files = [f for f in os.listdir(folder) if f.endswith(".json")]

if not files:
    st.warning("No bills found in the system!")
    st.stop()

# Collect tables and dates first
table_numbers = set()
date_list = []

for file in files:
    with open(os.path.join(folder, file), "r") as f:
        content = json.load(f)
        table_numbers.add(content.get("table"))
        try:
            dt = datetime.fromisoformat(content.get("timestamp"))
            date_list.append(dt.date())
        except:
            pass

# Sidebar Filters
st.sidebar.header("🔍 Filters")
selected_table = st.sidebar.selectbox("Filter by Table", ["All"] + sorted(table_numbers))
start_date = st.sidebar.date_input("Start Date", min(date_list) if date_list else datetime.today())
end_date = st.sidebar.date_input("End Date", max(date_list) if date_list else datetime.today())

# Process files after filters are selected
data = []
for file in files:
    with open(os.path.join(folder, file), "r") as f:
        content = json.load(f)

        # Apply table filter
        if selected_table != "All" and content.get("table") != selected_table:
            continue

        # Apply date filter
        try:
            dt = datetime.fromisoformat(content.get("timestamp"))
            if not (start_date <= dt.date() <= end_date):
                continue
        except:
            continue

        for item, details in content["items"].items():
            data.append({
                "timestamp": content["timestamp"],
                "item": item,
                "qty": details["qty"],
                "amount": details["qty"] * details["price"]
            })

# Create DataFrame
df = pd.DataFrame(data)
df["timestamp"] = pd.to_datetime(df["timestamp"])
df["hour"] = df["timestamp"].dt.hour

# 📊 Metrics
st.metric("🧾 Total Orders", len(files))
st.metric("💰 Total Revenue", f"₹{df['amount'].sum():,.2f}")
st.metric("🍽️ Unique Items Sold", df['item'].nunique())

# 🔥 Top Items
st.subheader("🔥 Top Selling Items")
top_items = df.groupby("item")["qty"].sum().sort_values(ascending=False)
st.bar_chart(top_items)

# ⏰ Hourly Trends
st.subheader("⏰ Sales Trend by Hour")
hourly_sales = df.groupby("hour")["amount"].sum()
st.line_chart(hourly_sales)
