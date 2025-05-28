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

        # Click on product specification
        element = await page.querySelector('#product-specification-link')
        await page.evaluate('(element) => { element.scrollIntoView({ behavior: "smooth", block: "center" }); }', element)
        await element.click()
        await asyncio.sleep(2)

        # Change quantity 
        element = await page.querySelector('#action-plus')
        await page.evaluate('(element) => { element.scrollIntoView({ behavior: "smooth", block: "center" }); }', element)
        await element.click()
        print("✅ Updated quantity")
        await asyncio.sleep(3)

        # Click on the standard dimension
        element = await page.querySelector('li[data-dimension]:first-child')
        await page.evaluate('(element) => { element.scrollIntoView({ behavior: "smooth", block: "center" }); }', element)
        await element.click()
        await asyncio.sleep(3)

        # Hover on the question mark to open the tooltip
        element = await page.querySelector('span.field-tooltip-action.action-help[data-dropdown="true"]')
        await page.evaluate('(element) => { element.scrollIntoView({ behavior: "smooth", block: "center" }); }', element)
        await element.hover()
        await asyncio.sleep(2)

        # Locate warranty checkbox check
        element = await page.querySelector('input[data-label="1 Year"]')
        await page.evaluate('(element) => { element.scrollIntoView({ behavior: "smooth", block: "center" }); }', element)
        await element.click()
        await asyncio.sleep(2)

        # Locate warranty checkbox uncheck
        element = await page.querySelector('input[data-label="1 Year"]')
        await page.evaluate('(element) => { element.scrollIntoView({ behavior: "smooth", block: "center" }); }', element)
        await element.click()
        await asyncio.sleep(2)

        # Click fabric color
        element = await page.querySelector('li.tool-color:nth-of-type(2)')
        await page.evaluate('(element) => { element.scrollIntoView({ behavior: "smooth", block: "center" }); }', element)
        await element.click()
        await asyncio.sleep(2)

        # Click on dimension field, clear it, then enter new value
        element = await page.querySelector('#H1')   
        await page.evaluate('(element) => { element.scrollIntoView({ behavior: "smooth", block: "center" }); }', element)
        await element.click()
        await asyncio.sleep(1)
        await page.evaluate('(selector) => document.querySelector(selector).value = ""', '#H1')
        await page.type('#H1', '12')
        print("✅ Cleared and changed dimension to 12")
        await asyncio.sleep(2)

        # Personalize section select
        # element = await page.querySelector('label[for="personalize_cover"]')
        # await page.evaluate('(element) => { element.scrollIntoView({ behavior: "smooth", block: "center" }); }', element)
        # await element.click()
        # await asyncio.sleep(2)

        # Personalize section deselect
        # element = await page.querySelector('label[for="personalize_cover"]')
        # await page.evaluate('(element) => { element.scrollIntoView({ behavior: "smooth", block: "center" }); }', element)
        # await element.click()
        # await asyncio.sleep(2)

        # Airbags checkbox check
        element = await page.querySelector('label[data-id="Air Bags"]')
        await page.evaluate('(element) => { element.scrollIntoView({ behavior: "smooth", block: "center" }); }', element)
        await element.click()
        await asyncio.sleep(2)

        # Airbags checkbox uncheck
        element = await page.querySelector('label[data-id="Air Bags"]')
        await page.evaluate('(element) => { element.scrollIntoView({ behavior: "smooth", block: "center" }); }', element)
        await element.click()
        await asyncio.sleep(2)

        # Product details section click
        element = await page.querySelector('a[href="#tiedownsgrommets"]')
        await page.evaluate('(element) => { element.scrollIntoView({ behavior: "smooth", block: "center" }); }', element)
        await element.click()
        await asyncio.sleep(2)

        # Back to top button click
        element = await page.querySelector('#back-to-top')
        await page.evaluate('(element) => { element.scrollIntoView({ behavior: "smooth", block: "center" }); }', element)
        await element.click()
        await asyncio.sleep(2)

        # Add to cart button click
        element = await page.querySelector('#product-addtocart-button')
        await page.evaluate('(element) => { element.scrollIntoView({ behavior: "smooth", block: "center" }); }', element)
        await element.click()

        # View cart button to be present and visible
        element = await page.waitForSelector('a.action.viewcart[data-id="view_cart"]', {'visible': True, 'timeout': 10000})
        await page.evaluate('(element) => { element.scrollIntoView({ behavior: "smooth", block: "center" }); }', element)
        await asyncio.sleep(5)  # Small delay after scroll
        await element.click()

    
        await asyncio.sleep(15)

        # Click on continue shopping button
        element = await page.waitForSelector('a.action-continue-shopping', {'visible': True, 'timeout': 15000})
        await page.evaluate('(element) => { element.scrollIntoView({ behavior: "smooth", block: "center" }); }', element)
        await asyncio.sleep(5)  # Small delay after scroll
        await element.click()
        

        # Click on continue shopping button pop up no
        element = await page.waitForSelector('button.action.primary.action-dismiss.action-small', {'visible': True, 'timeout': 10000})
        await page.evaluate('(element) => { element.scrollIntoView({ behavior: "smooth", block: "center" }); }', element)
        await asyncio.sleep(5)  # Small delay after scroll
        await element.click()
      

        # Click on delete prodcut button
        element = await page.waitForSelector('a.action-delete', {'visible': True, 'timeout': 10000})
        await page.evaluate('(element) => { element.scrollIntoView({ behavior: "smooth", block: "center" }); }', element)
        await asyncio.sleep(5)  # Small delay after scroll
        await element.click()
       
        # Click on delete prodcut button pop up no
        element = await page.waitForSelector('button.action.primary.action-dismiss.action-small', {'visible': True, 'timeout': 10000})
        await page.evaluate('(element) => { element.scrollIntoView({ behavior: "smooth", block: "center" }); }', element)
        await asyncio.sleep(5)  # Small delay after scroll
        await element.click()

        # Click on available offer
        element = await page.waitForSelector('#cart-offer-link', {'visible': True, 'timeout': 10000})
        await page.evaluate('(element) => { element.scrollIntoView({ behavior: "smooth", block: "center" }); }', element)
        await asyncio.sleep(5)  # Small delay after scroll
        await element.click()

        # Click on coupon field and enter coupon code
        element = await page.waitForSelector('#coupon_code_popup', {'visible': True, 'timeout': 10000})
        await page.evaluate('(element) => { element.scrollIntoView({ behavior: "smooth", block: "center" }); }', element)
        await asyncio.sleep(5)  # Small delay after scroll
        await element.click()
        await element.type('QA')  # Type coupon code into the field

        # Click on apply button
        element = await page.waitForSelector('#applyCoupon', {'visible': True, 'timeout': 10000})
        await page.evaluate('(element) => { element.scrollIntoView({ behavior: "smooth", block: "center" }); }', element)
        await asyncio.sleep(5)  # Small delay after scroll
        await element.click()

        await asyncio.sleep(10)

        # Click on the applye button in side drawer
        element = await page.waitForSelector('.applyCurrCoupon', {'visible': True, 'timeout': 10000})
        await page.evaluate('(element) => { element.scrollIntoView({ behavior: "smooth", block: "center" }); }', element)
        await asyncio.sleep(5)  # Small delay after scroll
        await element.click()
        
        await asyncio.sleep(10)

        # Click on cancel button in coupon code field.
        element = await page.waitForSelector('img[alt="Cancel"]', {'visible': True, 'timeout': 10000})
        await page.evaluate('(element) => { element.scrollIntoView({ behavior: "smooth", block: "center" }); }', element)
        await asyncio.sleep(5)  # Small delay after scroll
        await element.click()

        await asyncio.sleep(10)

        #scroll to shipping method section.
        element = await page.waitForSelector('fieldset.fieldset.rate', {'visible': True, 'timeout': 10000})
        await page.evaluate('(element) => { element.scrollIntoView({ behavior: "smooth", block: "center" }); }', element)
        await asyncio.sleep(2)  # Small delay after scroll
        
        # Click shiping method priority.
        element = await page.waitForSelector('label[for*="priority"]', {'visible': True, 'timeout': 15000})
        await page.evaluate('(element) => { element.scrollIntoView({ behavior: "smooth", block: "center" }); }', element)
        await asyncio.sleep(2)  # Small delay after scroll
        await element.click()

        #Remove assurance charge.
        element = await page.waitForSelector('input[name="remove_warranty"]', {'visible': True, 'timeout': 10000})
        await page.evaluate('(element) => { element.scrollIntoView({ behavior: "smooth", block: "center" }); }', element)
        await asyncio.sleep(5)  # Small delay after scroll
        await element.click()

        #Select assurance charge.
        element = await page.waitForSelector('input[data-title="1 Year"]', {'visible': True, 'timeout': 10000})
        await page.evaluate('(element) => { element.scrollIntoView({ behavior: "smooth", block: "center" }); }', element)
        await asyncio.sleep(5)  # Small delay after scroll
        await element.click()

        #scroll to order summary section.
        element = await page.waitForSelector('#secure_checkout', {'visible': True, 'timeout': 10000})
        await page.evaluate('(element) => { element.scrollIntoView({ behavior: "smooth", block: "center" }); }', element)
        await asyncio.sleep(2)  # Small delay after scroll

        await asyncio.sleep(6)

        #Click amazon pay button.
        element = await page.waitForSelector('div.amazonpay-merchant-shadow-root-parent-element-for-executing-modal-script.amazonpay-button-parent-container-checkout-A2KGO0QV9T7EUE', {'visible': True, 'timeout': 10000})
        await page.evaluate('(element) => { element.scrollIntoView({ behavior: "smooth", block: "center" }); }', element)
        await asyncio.sleep(2)  # Small delay after scroll
        await element.click()

        # Wait for new window to open and get all pages
        await asyncio.sleep(5)  # Wait for window to open
        pages = await browser.pages()
        
        # Close the amazon pay window (last one in the list)
        if len(pages) > 1:
            await pages[-1].close() 

        #Click link button.
        element = await page.waitForSelector('#payment-request-button-cart iframe', {'visible': True, 'timeout': 10000})
        await page.evaluate('(element) => { element.scrollIntoView({ behavior: "smooth", block: "center" }); }', element)
        await asyncio.sleep(2)  # Small delay after scroll
        await element.click()

        # Wait for new window to open and get all pages
        pages = await browser.pages()

        # Close the link window (last one in the list)
        if len(pages) > 1:
            await pages[-1].close()

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

        # Hover on the question mark to open the tooltip
        # element = await page.querySelector('span.field-tooltip-action.action-help')
        # await page.evaluate('(element) => { element.scrollIntoView({ behavior: "smooth", block: "center" }); }', element)
        # await element.hover()
        # await asyncio.sleep(2)

        await asyncio.sleep(10)

        # Click on priority shipping option on shipping page. #label_method_matrixrate_priority_matrixrate
        element = await page.waitForSelector('#label_method_matrixrate_standardground_matrixrate', {'visible': True, 'timeout': 10000})
        await page.evaluate('(element) => { element.scrollIntoView({ behavior: "smooth", block: "center" }); }', element)
        await asyncio.sleep(2)  # Small delay after scroll
        await element.click()

        # Click on next button.  
        element = await page.waitForSelector('button.continue', {'visible': True, 'timeout': 10000})
        await page.evaluate('(element) => { element.scrollIntoView({ behavior: "smooth", block: "center" }); }', element)
        await asyncio.sleep(2)  # Small delay after scroll
        await element.click()

        await asyncio.sleep(10)

        # Click on amazon pay button.   
        element = await page.waitForSelector('.pay-icon.checkout-amazon-pay.amazon-button-container', {'visible': True, 'timeout': 10000})
        await page.evaluate('(element) => { element.scrollIntoView({ behavior: "smooth", block: "center" }); }', element)
        await asyncio.sleep(2)  # Small delay after scroll
        await element.click()

         # Wait for new window to open and get all pages
        await asyncio.sleep(5)  # Wait for window to open
        pages = await browser.pages()
        
        # Close the amazon pay window (last one in the list)
        if len(pages) > 1:
            await pages[-1].close()
            print("✅ Closed the Amazon Pay popup window")

        # Click on link button. 
        element = await page.waitForSelector('#payment-request-button', {'visible': True, 'timeout': 10000})
        await page.evaluate('(element) => { element.scrollIntoView({ behavior: "smooth", block: "center" }); }', element)
        await asyncio.sleep(2)  # Small delay after scroll
        await element.click()
        
        # Wait for new window to open and get all pages
        await asyncio.sleep(5)  # Wait for window to open
        pages = await browser.pages()
        
        # Close the link window (last one in the list)
        if len(pages) > 1:
            await pages[-1].close()
            print("✅ Closed the link popup window")

        # Click on paypal button.  
        element = await page.waitForSelector('#braintree-paypal-express-checkout-button iframe', {'visible': True, 'timeout': 10000})
        await page.evaluate('(element) => { element.scrollIntoView({ behavior: "smooth", block: "center" }); }', element)
        await asyncio.sleep(2)  # Small delay after scroll
        await element.click()

        # Wait for window to open
        pages = await browser.pages()
        
        # Close the paypal window (last one in the list)
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

        # Extract and print order ID
        order_id_element = await page.waitForSelector('a.order-number > strong', {'visible': True, 'timeout': 10000})
        order_id = await page.evaluate('(element) => element.textContent', order_id_element)
        print(f"Order ID: {order_id}")
        

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



