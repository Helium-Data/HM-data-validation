import smtplib
import os
from email.message import EmailMessage
from config import recipient_email, sender_email

def send_email(sender_password, file_path):
    """
    Sends an email with an attachment
    """

    # Create email message
    message = EmailMessage()
    sender_email = message["From"] = "data@heliumhealth.com"
    message["To"] = recipient_email
    message["Subject"] = "HTHA Data Validity Check Report"
    message.set_content("Please find the attached report.")

    # Check if file exists
    if os.path.exists(file_path):
        with open(file_path, "rb") as file:
            file_data = file.read()
            file_name = os.path.basename(file_path)
        
        # Attach the validation file
        message.add_attachment(file_data, maintype="application", subtype="octet-stream", filename=file_name)
    else:
        print(f"Error: File '{file_path}' not found.")
        return

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, sender_password)
            server.send_message(message)
        print("Email sent successfully!")
    except Exception as e:
        print(f" Error sending email: {e}")

# Example usage
# send_email(
#     sender_email="data@heliumhealth.com",
#     sender_password="",  
#     recipient_email="obiechina@heliumhealth.com",
#     subject="HTHA Data Validity Check Report",
#     body="Please find the attached report.",
#     file_path="HTHA_Data_Validity_Check_Report.txt"
# )
