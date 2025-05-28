import asyncio
import json
from pyppeteer import launch

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
        headless=False,
        executablePath=chrome_path,
        args=['--start-maximized'],
        defaultViewport=None
    )
    page = await browser.newPage()
    page.on('console', handle_console)

    # Load initial page
    url = 'https://www.coversandall.com/custom-covers/custom-cylinder-round-covers-p'
    print("🌐 Navigating to:", url)
    await page.goto(url, {'waitUntil': 'networkidle2', 'timeout': 60000})
    await asyncio.sleep(5)  # Initial wait to capture events
    # Scroll down a moderate amount to trigger potential events
    # await page.evaluate('window.scrollBy(0, 500)')
    # print("⬇️ Scrolled down 500px")
    await asyncio.sleep(2)

    # Perform actions directly with Pyppeteer
    try:

   
        # Add to cart button click
        element = await page.querySelector('#product-addtocart-button')
        await page.evaluate('(element) => { element.scrollIntoView({ behavior: "smooth", block: "center" }); }', element)
        await element.click()


        # View cart button to be present and visible
        element = await page.waitForSelector('a.action.viewcart[data-id="view_cart"]', {'visible': True, 'timeout': 10000})
        await page.evaluate('(element) => { element.scrollIntoView({ behavior: "smooth", block: "center" }); }', element)
        await asyncio.sleep(5)  # Small delay after scroll
        await element.click()

        await asyncio.sleep(10)

        #scroll to order summary section.
        element = await page.waitForSelector('#secure_checkout', {'visible': True, 'timeout': 10000})
        await page.evaluate('(element) => { element.scrollIntoView({ behavior: "smooth", block: "center" }); }', element)
        await asyncio.sleep(2)  # Small delay after scroll

        # Click on secure checkout button.
        element = await page.waitForSelector('#secure_checkout > span.button-text', {'visible': True, 'timeout': 10000})
        await page.evaluate('(element) => { element.scrollIntoView({ behavior: "smooth", block: "center" }); }', element)
        await asyncio.sleep(2)  # Small delay after scroll
        await element.click()

        await asyncio.sleep(10)

        # Click in email field and enter value
        element = await page.waitForSelector('input#customer-email', {'visible': True, 'timeout': 10000})
        await page.evaluate('(element) => { element.scrollIntoView({ behavior: "smooth", block: "center" }); }', element)
        await asyncio.sleep(2)  # Small delay after scroll
        await element.click()
        await element.type('harshil.shukla@commercepundit.com')  # Type email into the field

        element = await page.waitForSelector('#conifrm_email_address', {'visible': True, 'timeout': 10000})
        await page.evaluate('(element) => { element.scrollIntoView({ behavior: "smooth", block: "center" }); }', element)
        await asyncio.sleep(2)  # Small delay after scroll
        await element.click()
        await element.type('harshil.shukla@commercepundit.com')  # Type email into the field

        # Click on first name field and enter value
        element = await page.waitForSelector('input[name="firstname"]', {'visible': True, 'timeout': 10000})
        await page.evaluate('(element) => { element.scrollIntoView({ behavior: "smooth", block: "center" }); }', element)
        await asyncio.sleep(2)  # Small delay after scroll
        await element.click()
        await element.type('cp')  # Type first name into the field

        # Click on last name field and enter value
        element = await page.waitForSelector('input[name="lastname"]', {'visible': True, 'timeout': 10000})
        await page.evaluate('(element) => { element.scrollIntoView({ behavior: "smooth", block: "center" }); }', element)
        await asyncio.sleep(2)  # Small delay after scroll
        await element.click()
        await element.type('test')  # Type last name into the field

        # Click on street address field and enter value
        element = await page.waitForSelector('input[name="street[0]"]:first-of-type', {'visible': True, 'timeout': 10000})
        await page.evaluate('(element) => { element.scrollIntoView({ behavior: "smooth", block: "center" }); }', element)
        await asyncio.sleep(2)  # Small delay after scroll
        await element.click()
        await element.type('street 1')  # Type last name into the field


        # Select value 'Georgia' directly without dropdown interaction
        element = await page.waitForSelector('select[name="region_id"]', {'visible': True, 'timeout': 10000})
        await page.evaluate('(element) => { element.scrollIntoView({ behavior: "smooth", block: "center" }); }', element)
        await asyncio.sleep(2)  # Small delay after scroll
        
        # Use select method to choose option by value directly
        await page.select('select[name="region_id"]', '19')
        await asyncio.sleep(1)  # Small delay after selection

        # Click on city field and enter value
        element = await page.waitForSelector('input[name="city"]', {'visible': True, 'timeout': 10000})
        await page.evaluate('(element) => { element.scrollIntoView({ behavior: "smooth", block: "center" }); }', element)
        await asyncio.sleep(2)  # Small delay after scroll
        await element.click()
        await element.type('Suwanee')  # Type last name into the field

        # Click on zip code field and enter value
        element = await page.waitForSelector('input[name="postcode"]', {'visible': True, 'timeout': 10000})
        await page.evaluate('(element) => { element.scrollIntoView({ behavior: "smooth", block: "center" }); }', element)
        await asyncio.sleep(2)  # Small delay after scroll
        await element.click()
        await element.type('30024')  # Type last name into the field

        # Click on phone number field and enter value
        element = await page.waitForSelector('input[name="telephone"]', {'visible': True, 'timeout': 10000})
        await page.evaluate('(element) => { element.scrollIntoView({ behavior: "smooth", block: "center" }); }', element)
        await asyncio.sleep(2)  # Small delay after scroll
        await element.click()
        await element.type('9876543210')  # Type last name into the field

        await asyncio.sleep(10)

        # Click on priority shipping option on shipping page. #label_method_matrixrate_standardground_matrixrate (For standard ground)
        element = await page.waitForSelector('#label_method_matrixrate_priority_matrixrate', {'visible': True, 'timeout': 10000})
        await page.evaluate('(element) => { element.scrollIntoView({ behavior: "smooth", block: "center" }); }', element)
        await asyncio.sleep(2)  # Small delay after scroll
        await element.click()

        # Click on next button.  
        element = await page.waitForSelector('button.continue', {'visible': True, 'timeout': 10000})
        await page.evaluate('(element) => { element.scrollIntoView({ behavior: "smooth", block: "center" }); }', element)
        await asyncio.sleep(2)  # Small delay after scroll
        await element.click()

        await asyncio.sleep(10)
        
        # Click on paypal button.  
        element = await page.waitForSelector('#braintree-paypal-express-checkout-button iframe', {'visible': True, 'timeout': 10000})
        await page.evaluate('(element) => { element.scrollIntoView({ behavior: "smooth", block: "center" }); }', element)
        await asyncio.sleep(2)  # Small delay after scroll
        await element.click()

        # Wait for new window to open and get all pages
        pages = await browser.pages()

        # Close the popup window directly
        if len(pages) > 1:
            await pages[-1].close()


        # Click on checkbox to use billing address as shipping address.  
        element = await page.waitForSelector('span[data-bind="i18n: \'My billing and shipping address are the same\'"]', {'visible': True, 'timeout': 10000})
        await page.evaluate('(element) => { element.scrollIntoView({ behavior: "smooth", block: "center" }); }', element)
        await asyncio.sleep(2)  # Small delay after scroll
        await element.click()

        # Click on checkbox to use billing address as shipping address.  
        element = await page.waitForSelector('span[data-bind="i18n: \'My billing and shipping address are the same\'"]', {'visible': True, 'timeout': 10000})
        await page.evaluate('(element) => { element.scrollIntoView({ behavior: "smooth", block: "center" }); }', element)
        await asyncio.sleep(2)  # Small delay after scroll
        await element.click()
        
        await asyncio.sleep(5)

        # Click on coupon code field and enter value.  
        element = await page.waitForSelector('#discount-form', {'visible': True, 'timeout': 10000})
        await page.evaluate('(element) => { element.scrollIntoView({ behavior: "smooth", block: "center" }); }', element)
        await asyncio.sleep(2)  # Small delay after scroll
        await element.click()
        await element.type('CPQADISCOUNT')

        # Click on apply coupon button
        element = await page.waitForSelector('button.action-apply', {'visible': True, 'timeout': 10000})
        await page.evaluate('(element) => { element.scrollIntoView({ behavior: "smooth", block: "center" }); }', element)
        await asyncio.sleep(2)  # Small delay after scroll
        await element.click()
                
        await asyncio.sleep(10)
        
        # Click on edit shipping address button.  
        element = await page.waitForSelector("button[data-bind='click: back']", {'visible': True, 'timeout': 10000})
        await page.evaluate('(element) => { element.scrollIntoView({ behavior: "smooth", block: "center" }); }', element)
        await asyncio.sleep(2)  # Small delay after scroll
        await element.click()

        # Click on next button.  
        element = await page.waitForSelector('button.continue', {'visible': True, 'timeout': 10000})
        await page.evaluate('(element) => { element.scrollIntoView({ behavior: "smooth", block: "center" }); }', element)
        await asyncio.sleep(2)  # Small delay after scroll
        await element.click()

        # Click on edit shipping address button.  
        element = await page.waitForSelector('button[data-bind="click: backToShippingMethod"]', {'visible': True, 'timeout': 10000})
        await page.evaluate('(element) => { element.scrollIntoView({ behavior: "smooth", block: "center" }); }', element)
        await asyncio.sleep(2)  # Small delay after scroll
        await element.click()
        
        # Click on next button.  
        element = await page.waitForSelector('button.continue', {'visible': True, 'timeout': 10000})
        await page.evaluate('(element) => { element.scrollIntoView({ behavior: "smooth", block: "center" }); }', element)
        await asyncio.sleep(2)  # Small delay after scroll
        await element.click()

        # Click on comment box.  
        element = await page.waitForSelector('#co-payment-form > fieldset > div.checkout-agreements-block.custom > div.payment-option._collapsible.opc-payment-additional.comment.last > div.payment-option-title.field.choice', {'visible': True, 'timeout': 10000})
        await page.evaluate('(element) => { element.scrollIntoView({ behavior: "smooth", block: "center" }); }', element)
        await asyncio.sleep(2)  # Small delay after scroll
        await element.click()
        
        # Type comment in comment box.  
        element = await page.waitForSelector('div[class="payment-option _collapsible opc-payment-additional comment last _active"] textarea[placeholder="Enter your comment..."]', {'visible': True, 'timeout': 10000})
        await page.evaluate('(element) => { element.scrollIntoView({ behavior: "smooth", block: "center" }); }', element)
        await asyncio.sleep(2)  # Small delay after scroll
        await element.click()
        await element.type('CP test order do not process')

        # Click on PO order button.  
        element = await page.waitForSelector('label[for="popayment"]', {'visible': True, 'timeout': 10000})
        await page.evaluate('(element) => { element.scrollIntoView({ behavior: "smooth", block: "center" }); }', element)
        await asyncio.sleep(2)  # Small delay after scroll
        await element.click()

        # Click on CC.  
        element = await page.waitForSelector('label[for="onlycard_payment_method"]', {'visible': True, 'timeout': 10000})
        await page.evaluate('(element) => { element.scrollIntoView({ behavior: "smooth", block: "center" }); }', element)
        await asyncio.sleep(2)  # Small delay after scroll
        await element.click()

        # Click on PO order button.  
        element = await page.waitForSelector('label[for="popayment"]', {'visible': True, 'timeout': 10000})
        await page.evaluate('(element) => { element.scrollIntoView({ behavior: "smooth", block: "center" }); }', element)
        await asyncio.sleep(2)  # Small delay after scroll
        await element.click()

        # Click on upload button
        element = await page.waitForSelector('#po_image_file', {'visible': True, 'timeout': 10000})
        await page.evaluate('(element) => { element.scrollIntoView({ behavior: "smooth", block: "center" }); }', element)
        await asyncio.sleep(2)  # Small delay after scroll
        
        # Upload test file
        await element.uploadFile('pdf_1.pdf')
        await asyncio.sleep(2)  # Small delay after upload

        # Click on place order button.  
        element = await page.waitForSelector('#place-order-trigger', {'visible': True, 'timeout': 10000})
        await page.evaluate('(element) => { element.scrollIntoView({ behavior: "smooth", block: "center" }); }', element)
        await asyncio.sleep(2)  # Small delay after scroll
        await element.click()
        
        await asyncio.sleep(15)
        
    except Exception as e:
        print(f"⚠️ Action failed: {str(e)}")

    # Wait to capture events after actions
    await asyncio.sleep(10)

    # Save all captured events
    with open('adb_events_with_actions.json', 'w') as f:
        json.dump(adb_events, f, indent=2)
        print(f"✅ Saved {len(adb_events)} adb_* events to adb_events_with_actions.json")

    await browser.close()

# Run the function
asyncio.run(capture_events_with_actions())


