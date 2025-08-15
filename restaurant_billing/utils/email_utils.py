import os
import smtplib
from email.message import EmailMessage

def send_email_with_bill(receiver_email, billing_id):
    filename = f"data/sample_bills/Bill_{billing_id}.pdf"

    if not os.path.exists(filename):
        raise FileNotFoundError("Bill PDF not found")

    # Send email (example using SMTP)
    sender_email = "your_email@gmail.com"
    password = "your_password"  # Or use environment variable / app password

    msg = EmailMessage()
    msg['Subject'] = f"Your Restaurant Bill #{billing_id}"
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg.set_content("Thank you for dining with us. Please find your bill attached.")

    with open(filename, 'rb') as f:
        file_data = f.read()
        msg.add_attachment(file_data, maintype='application', subtype='pdf', filename=os.path.basename(filename))

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(sender_email, password)
        smtp.send_message(msg)

