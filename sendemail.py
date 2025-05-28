import smtplib
from email.mime.multipart import MIMEMultipart
from email.message import EmailMessage
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication


#Sending email
subject = "Adobe event"
body = "Please find the adobe events results below."
sender_email = "cp.harshil@gmail.com"
recipient_email = "harshil.shukla@commercepundit.com"
sender_password = "culo jpqg pmtr iafc"
smtp_server = 'smtp.gmail.com'
smtp_port = 465
path_to_file = 'adb_events_with_actions.json'

# MIMEMultipart() creates a container for an email message that can hold
# different parts, like text and attachments and in next line we are
# attaching different parts to email container like subject and others.
message = MIMEMultipart()
message['Subject'] = subject
message['From'] = sender_email
message['To'] = recipient_email
body_part = MIMEText(body)
message.attach(body_part)

# section to attach file
with open(path_to_file,'rb') as file:
    # Attach the file with filename to the email
    message.attach(MIMEApplication(file.read(), Name="network_respones.csv"))
# Add error handling for email sending
try:
    # Create secure connection with server and send email
    with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, message.as_string())
    print("✅ Email sent successfully!")
except smtplib.SMTPAuthenticationError:
    print("❌ Error: Email authentication failed. Please check your username and password.")
except smtplib.SMTPException as e:
    print(f"❌ Error sending email: {str(e)}")
except Exception as e:
    print(f"❌ Unexpected error: {str(e)}")
