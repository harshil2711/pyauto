import asyncio
import json
from pyppeteer import launch
import smtplib
from email.mime.multipart import MIMEMultipart
from email.message import EmailMessage
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication


adb_events = []

# Convert async function to be triggered properly inside sync callback
def handle_console(msg):
    asyncio.create_task(process_console(msg))

async def process_console(msg):
    try:
        for arg in msg.args:
            val = await arg.jsonValue()
            if isinstance(val, dict) and val.get('event', '').startswith('adb_'):
                adb_events.append(val)
                print("✅ Captured:", val['event'])
    except Exception:
        pass

async def capture_events_with_actions():
    chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    
    # Launch browser once
    browser = await launch(
        headless=True,
        executablePath=chrome_path,
        args=['--start-maximized'],
        defaultViewport=None
    )
    page = await browser.newPage()
    page.on('console', handle_console)

    # Load initial page
    url = 'https://www.coversandall.com/patio-furniture-covers/seating-covers/chair-covers/chair-cover-design-1-p'
    print("🌐 Navigating to:", url)
    await page.goto(url, {'waitUntil': 'networkidle2', 'timeout': 60000})
    await asyncio.sleep(5)  # Initial wait to capture events
    # Scroll down a moderate amount to trigger potential events
    # await page.evaluate('window.scrollBy(0, 500)')
    # print("⬇️ Scrolled down 500px")
    await asyncio.sleep(2)

    # Perform actions directly with Pyppeteer
    try:
        # Click breadcrumb while holding Ctrl to open in new tab
        element = await page.querySelector('.breadcrumbs ul.items li.item:nth-child(3) a')
        await page.evaluate('(element) => { element.scrollIntoView({ behavior: "smooth", block: "center" }); }', element)
        await page.keyboard.down('Control')
        await element.click()
        await page.keyboard.up('Control')
        await asyncio.sleep(2)

      

        

    except Exception as e:
        print(f"⚠️ Action failed: {str(e)}")

    # Wait to capture events after actions
    await asyncio.sleep(25)

    # Save all captured events
    with open('adb_events_with_actions.json', 'w') as f:
        json.dump(adb_events, f, indent=2)
        print(f"✅ Saved {len(adb_events)} adb_* events to adb_events_with_actions.json")


    await browser.close()

# Run the function
asyncio.run(capture_events_with_actions())


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
    message.attach(MIMEApplication(file.read(), Name="adb_events_with_actions.json"))
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
