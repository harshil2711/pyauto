import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

#Sending email
subject = "Adobe event"
body = "Please find the adobe events results below."
sender_email = "cp.harshil@gmail.com"
recipient_emails = ["harshil.shukla@commercepundit.com", "prashant@commercepundit.com"]
sender_password = "culo jpqg pmtr iafc"
smtp_server = 'smtp.gmail.com'
smtp_port = 465
path_to_file = 'adb_events_with_actions.json'

# Add error handling for email sending
try:
    # Create secure connection with server
    with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
        server.login(sender_email, sender_password)
        
        # Send email to each recipient individually
        for recipient in recipient_emails:
            # Create new message for each recipient
            message = MIMEMultipart()
            message['Subject'] = subject
            message['From'] = sender_email
            message['To'] = recipient  # Single recipient per message
            body_part = MIMEText(body)
            message.attach(body_part)
            
            # Attach file
            with open(path_to_file,'rb') as file:
                message.attach(MIMEApplication(file.read(), Name="adb_events_with_actions.json"))
            
            # Send email
            server.sendmail(sender_email, recipient, message.as_string())
            print(f"✅ Email sent successfully to {recipient}!")
            
except smtplib.SMTPAuthenticationError:
    print("❌ Error: Email authentication failed. Please check your username and password.")
except smtplib.SMTPException as e:
    print(f"❌ Error sending email: {str(e)}")
except Exception as e:
    print(f"❌ Unexpected error: {str(e)}")
