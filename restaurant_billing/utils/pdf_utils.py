import os
from datetime import datetime
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet


def generate_pdf(bill_data,billing_id=None):
    try:
        # ✅ Always create folder before PDF path
        folder_path = os.path.join("data", "sample_bills")
        os.makedirs(folder_path, exist_ok=True)

        # File path with timestamp
        timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = f"Bill_{bill_data['billing_id']}.pdf"
        pdf_path = os.path.join(folder_path, file_name)

        # PDF content
        doc = SimpleDocTemplate(pdf_path)
        styles = getSampleStyleSheet()
        elements = []

        elements.append(Paragraph(f"Bill ID: {bill_data['billing_id']}", styles['Title']))
        elements.append(Spacer(1, 12))
        elements.append(Paragraph(f"Table: {bill_data['table']}", styles['Normal']))
        elements.append(Paragraph(f"Date: {bill_data['timestamp']}", styles['Normal']))
        elements.append(Spacer(1, 12))

        for item, details in bill_data['items'].items():
            elements.append(Paragraph(
                f"{item} - Qty: {details['qty']} - Price: ₹{details['price']}", 
                styles['Normal']
            ))

        elements.append(Spacer(1, 12))
        elements.append(Paragraph(f"Subtotal: ₹{bill_data['subtotal']}", styles['Normal']))
        elements.append(Paragraph(f"GST: ₹{bill_data['gst']}", styles['Normal']))
        elements.append(Paragraph(f"Discount: ₹{bill_data['discount']}", styles['Normal']))
        elements.append(Paragraph(f"Final Total: ₹{bill_data['final_total']}", styles['Normal']))
        elements.append(Paragraph(f"Tip: ₹{bill_data['tip']}", styles['Normal']))
        elements.append(Paragraph(f"Grand Total: ₹{bill_data['grand_total']}", styles['Normal']))

        # ✅ Save PDF
        doc.build(elements)
        print(f"✅ PDF generated: {pdf_path}")
        return pdf_path

    except Exception as e:
        print(f"❌ Failed to create PDF: {e}")
        return None
    
