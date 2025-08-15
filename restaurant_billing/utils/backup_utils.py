import os
from datetime import datetime
from utils.pdf_utils import generate_pdf

BACKUP_DIR = os.path.join(os.getcwd(), "bills_backup")

def ensure_backup_dir():
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)

def backup_bill(bill_data):
    """
    bill_data: dict containing bill details
    Expected keys: 'bill_id', 'items', 'total', 'date', 'customer_name'
    """
    ensure_backup_dir()
    filename = f"Bill_{bill_data['bill_id']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    filepath = os.path.join(BACKUP_DIR, filename)
    generate_pdf(bill_data, filepath)
    return filepath
