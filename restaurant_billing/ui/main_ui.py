import streamlit as st
import sys
import os
import uuid
from datetime import datetime
import pandas as pd
import sqlite3
import json
from playsound import playsound

# Add parent directory for utils imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.db_utils import save_order
from utils.pdf_utils import generate_pdf
from utils.sentiment_analyzer import analyze_sentiment
from utils.ai_recommendations import get_recommendations


# -------------------- Sidebar --------------------
st.sidebar.title("🪑 Table Info")
st.sidebar.markdown(f"🕒 **{datetime.now().strftime('%A, %d %B %Y — %I:%M %p')}**")

table_number = st.sidebar.selectbox("Select Table", options=[f"Table {i}" for i in range(1, 11)])

# Suggested Items (history-based)
suggested_items = {}
history_folder = os.path.join("data", "sample_bills")
if os.path.exists(history_folder):
    item_count = {}
    for filename in os.listdir(history_folder):
        if filename.endswith(".json"):
            with open(os.path.join(history_folder, filename), "r", encoding="utf-8") as f:
                try:
                    bill = json.load(f)
                    if bill.get("table") == table_number:
                        for item, details in bill["items"].items():
                            item_count[item] = item_count.get(item, 0) + details.get("qty", 0)
                except Exception:
                    continue
    if item_count:
        suggested_items = dict(sorted(item_count.items(), key=lambda x: x[1], reverse=True)[:3])
        st.sidebar.markdown("📌 **Frequently Ordered:**")
        for item, qty in suggested_items.items():
            st.sidebar.markdown(f"🔹 {item} (×{qty})")

# Bill ID + time
billing_id = str(uuid.uuid4())[:8]
st.sidebar.markdown(f"**Bill ID:** `{billing_id}`")
st.sidebar.markdown(f"🕒 Time: `{datetime.now().strftime('%d %b %Y %H:%M')}`")

# -------------------- Load Menu --------------------
def load_menu():
    conn = sqlite3.connect(os.path.join("db", "restaurant.db"))
    df = pd.read_sql_query("SELECT * FROM menu", conn)
    conn.close()
    return df

menu = load_menu()
st.subheader("📋 Select Items to Order")

# show menu with quantity inputs
selected_items = {}
for index, row in menu.iterrows():
    widget_key = f"qty_{row['id']}"
    qty = st.number_input(f"{row['name']} (₹{row['price']})", min_value=0, step=1, key=widget_key)
    if qty > 0:
        selected_items[row['name']] = (qty, row['price'])

# -------------------- Live Preview + Recommendations --------------------
if selected_items:
    st.markdown("### 👁️ Live Order Preview")
    preview_data = {"Item": [], "Qty": [], "Unit Price (₹)": [], "Total (₹)": []}
    for item, (qty, price) in selected_items.items():
        preview_data["Item"].append(item)
        preview_data["Qty"].append(qty)
        preview_data["Unit Price (₹)"].append(price)
        preview_data["Total (₹)"].append(qty * price)
    st.table(pd.DataFrame(preview_data))

    # Recommendations (optional)
    try:
        from utils.recommender import get_combo_recommendations
        st.markdown("🍽️ **You might also like:**")
        current_selection = list(selected_items.keys())
        suggestions = get_combo_recommendations(current_selection)
        if suggestions:
            for item, count in suggestions:
                st.markdown(f"🔸 **{item}** — ordered together {count} times")
        else:
            st.markdown("✅ No additional suggestions.")
    except Exception:
        # recommender optional - don't break app if missing
        pass

# -------------------- Tip Options --------------------
st.subheader("💰 Tip Options")
tip_choice = st.radio("Add Tip?", options=["No Tip", "5% Tip", "10% Tip", "Custom"], key="tip_choice")
custom_tip = 0.0
if tip_choice == "Custom":
    custom_tip = st.number_input("Enter custom tip amount (₹):", min_value=0.0, step=1.0, key="custom_tip_input")


    # --- Generate Bill ---
pdf_path = None  # ensure defined in outer scope
if st.button("🯞 Generate Bill", key="generate_btn"):
    if not selected_items:
        st.warning("Please select at least one item before generating the bill.")
    else:
        # Calculations
        total = sum(qty * price for qty, price in selected_items.values())
        gst_percent = 5
        gst_amount = (gst_percent / 100) * total
        discount_value = 0
        final_total = total + gst_amount - discount_value

        tip_value = 0.0
        if tip_choice == "5% Tip":
            tip_value = 0.05 * final_total
        elif tip_choice == "10% Tip":
            tip_value = 0.10 * final_total
        elif tip_choice == "Custom":
            tip_value = float(custom_tip)

        grand_total = final_total + tip_value

        # Bill data
        bill_data = {
            "billing_id": billing_id,
            "table": table_number,
            "timestamp": datetime.now().isoformat(),
            "items": {item: {"qty": qty, "price": price} for item, (qty, price) in selected_items.items()},
            "subtotal": total,
            "gst": gst_amount,
            "discount": discount_value,
            "final_total": final_total,
            "tip": tip_value,
            "grand_total": grand_total,
            "payment": ""
        }

        # Save to DB & JSON
        try:
            save_order(selected_items, grand_total, table_number, billing_id)
        except Exception as e:
            st.warning(f"Warning: could not save to DB: {e}")

        os.makedirs(history_folder, exist_ok=True)
        json_path = os.path.join(history_folder, f"{billing_id}.json")
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(bill_data, f, indent=4)

        # QR Code
        try:
            import qrcode
            qr_path = os.path.join(history_folder, f"{billing_id}_qr.png")
            qrcode.make(json_path).save(qr_path)
            st.image(qr_path, caption="📱 Scan to View Digital Bill", width=250)
        except Exception:
            qr_path = None

        # Play sound
        sound_file = os.path.join("data", "success.mp3")
        try:
            if os.path.exists(sound_file):
                playsound(sound_file)
        except Exception:
            pass

        # --- Show short bill summary on UI ---
        st.write("### 🧾 Bill Summary")
        for item, detail in bill_data["items"].items():
            st.write(f"{item} x {detail['qty']} = ₹{detail['qty'] * detail['price']}")
        st.markdown(f"✅ **Subtotal:** ₹{bill_data['subtotal']}")
        st.markdown(f"🔸 **+ GST (5%)**: ₹{bill_data['gst']:.2f}")
        st.markdown(f"🟢 **- Discount:** ₹{bill_data['discount']:.2f}")
        st.markdown(f"🔴 **Total Payable:** ₹{bill_data['final_total']:.2f}")
        st.markdown(f"🧾 **Tip:** ₹{bill_data['tip']:.2f}")
        st.markdown(f"💳 **Grand Total (with Tip): ₹{bill_data['grand_total']:.2f}")

        # --- Generate PDF ---
        try:
            pdf_path = generate_pdf(bill_data)
            if pdf_path and os.path.exists(pdf_path):
                st.success("📄 PDF receipt generated!")
                st.download_button(
                    "📥 Download Bill PDF",
                    open(pdf_path, "rb"),
                    file_name=os.path.basename(pdf_path)
                )
            else:
                st.error("PDF generation returned no valid file.")
                pdf_path = None
        except Exception as e:
            st.error(f"Failed to create PDF: {e}")
            pdf_path = None

        # --- Local backup after PDF creation ---
        try:
            bill_data["bill_id"] = billing_id
            from utils.backup_utils import backup_bill
            backup_path = backup_bill(bill_data)
            if backup_path:
                st.info(f"💾 Local backup created: {backup_path}")
        except Exception as e:
            st.warning(f"Backup failed: {e}")

        # --- AI Recommendations Section ---
        try:
            current_items = list(bill_data["items"].keys())
            recommendations = get_recommendations(current_items)
            st.write("### 🤖 AI-Powered Recommendations for You")
            if recommendations:
                st.markdown(
                    "Based on your current order, you might also enjoy: " +
                    ", ".join(recommendations)
                )
            else:
                st.markdown("We couldn't find any recommendations right now, but stay tuned!")
        except Exception as e:
            st.warning(f"AI recommendations unavailable: {e}")

        # --- Payment method ---
        payment_method = st.selectbox(
            "Select Payment Mode",
            ["Cash", "Card", "UPI"],
            key=f"payment_{billing_id}"
        )
        bill_data["payment"] = payment_method

        # Save final JSON with payment
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(bill_data, f, indent=4)

        # --- Email Section ---
        st.markdown("---")
        st.subheader("📧 Send Bill via Email")
        email = st.text_input("Enter customer email:", key=f"email_{billing_id}")
        if st.button("Send Email", key=f"send_email_{billing_id}"):
            if email and pdf_path and os.path.exists(pdf_path):
                try:
                    from utils.email_utils import send_email_with_bill
                    send_email_with_bill(email, pdf_path)
                    st.success("✅ Email sent successfully!")
                except Exception as e:
                    st.error(f"❌ Failed to send email: {e}")
            else:
                st.warning("⚠️ Please enter a valid email and ensure the PDF exists.")

        # --- Feedback Section ---
        st.markdown("---")
        st.subheader("💬 We'd love your feedback!")
        with st.form(f"feedback_form_{billing_id}"):
            comment = st.text_area(
                "Leave a comment about your experience:",
                key=f"feedback_input_{billing_id}"
            )
            submit_feedback = st.form_submit_button("Submit Feedback")
            if submit_feedback:
                if comment.strip():
                    sentiment = analyze_sentiment(comment)
                    st.success(f"✅ Feedback received! Sentiment: **{sentiment}**")
                    os.makedirs("data/feedback", exist_ok=True)
                    feedback_data = {
                        "bill_id": billing_id,
                        "table": table_number,
                        "timestamp": datetime.now().isoformat(),
                        "comment": comment,
                        "sentiment": sentiment
                    }
                    with open(
                        os.path.join("data/feedback", f"{billing_id}_feedback.json"),
                        "w",
                        encoding="utf-8"
                    ) as f:
                        json.dump(feedback_data, f, indent=4)
                else:
                    st.warning("Please write some feedback before submitting.")


