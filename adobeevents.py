import asyncio
import json
from pyppeteer import launch
import smtplib
from email.mime.multipart import MIMEMultipart
from email.message import EmailMessage
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import datetime
import os

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
        try:
            element = await page.querySelector('.breadcrumbs ul.items li.item:nth-child(3) a')
            await page.evaluate('(element) => { element.scrollIntoView({ behavior: "smooth", block: "center" }); }', element)
            await page.keyboard.down('Control')
            await element.click()
            await page.keyboard.up('Control')
            await asyncio.sleep(2)
        except Exception as e:
            print(f"❌ Error clicking breadcrumb: {e}")

        # Click on product specification
        try : 
            element = await page.querySelector('#product-specification-link')
            await page.evaluate('(element) => { element.scrollIntoView({ behavior: "smooth", block: "center" }); }', element)
            await element.click()
            await asyncio.sleep(2)
        except Exception as e:
            print(e)
            
        # Change quantity 
        try:
            element = await page.querySelector('#action-plus')
            await page.evaluate('(element) => { element.scrollIntoView({ behavior: "smooth", block: "center" }); }', element)
            await element.click()
            print("✅ Updated quantity")
            await asyncio.sleep(3)
        except Exception as e:
            print(f"❌ Error changing quantity: {e}")

        # Click on the standard dimension
        try:
            element = await page.querySelector('li[data-dimension]:first-child')
            await page.evaluate('(element) => { element.scrollIntoView({ behavior: "smooth", block: "center" }); }', element)
            await element.click()
            await asyncio.sleep(3)
        except Exception as e:
            print(f"❌ Error clicking standard dimension: {e}")

        # Hover on the question mark to open the tooltip
        try:
            element = await page.querySelector('span.field-tooltip-action.action-help[data-dropdown="true"]')
            await page.evaluate('(element) => { element.scrollIntoView({ behavior: "smooth", block: "center" }); }', element)
            await element.hover()
            await asyncio.sleep(2)
        except Exception as e:
            print(f"❌ Error hovering question mark: {e}")

        # Locate warranty checkbox check
        try:
            element = await page.querySelector('input[data-label="1 Year"]')
            await page.evaluate('(element) => { element.scrollIntoView({ behavior: "smooth", block: "center" }); }', element)
            await element.click()
            await asyncio.sleep(2)
        except Exception as e:
            print(f"❌ Error checking warranty checkbox: {e}")

        # Locate warranty checkbox uncheck
        try:
            element = await page.querySelector('input[data-label="1 Year"]')
            await page.evaluate('(element) => { element.scrollIntoView({ behavior: "smooth", block: "center" }); }', element)
            await element.click()
            await asyncio.sleep(2)
        except Exception as e:
            print(f"❌ Error unchecking warranty checkbox: {e}")

        # Click fabric color
        try:
            element = await page.querySelector('li.tool-color:nth-of-type(2)')
            await page.evaluate('(element) => { element.scrollIntoView({ behavior: "smooth", block: "center" }); }', element)
            await element.click()
            await asyncio.sleep(2)
        except Exception as e:
            print(f"❌ Error clicking fabric color: {e}")

        # Click on dimension field, clear it, then enter new value
        try:
            element = await page.querySelector('#H1')   
            await page.evaluate('(element) => { element.scrollIntoView({ behavior: "smooth", block: "center" }); }', element)
            await element.click()
            await asyncio.sleep(1)
            await page.evaluate('(selector) => document.querySelector(selector).value = ""', '#H1')
            await page.type('#H1', '12')
            print("✅ Cleared and changed dimension to 12")
            await asyncio.sleep(2)
        except Exception as e:
            print(f"❌ Error changing dimension: {e}")

        # Airbags checkbox check
        try:
            element = await page.querySelector('label[data-id="Air Bags"]')
            await page.evaluate('(element) => { element.scrollIntoView({ behavior: "smooth", block: "center" }); }', element)
            await element.click()
            await asyncio.sleep(2)
        except Exception as e:
            print(f"❌ Error checking airbags checkbox: {e}")

        # Airbags checkbox uncheck
        try:
            element = await page.querySelector('label[data-id="Air Bags"]')
            await page.evaluate('(element) => { element.scrollIntoView({ behavior: "smooth", block: "center" }); }', element)
            await element.click()
            await asyncio.sleep(2)
        except Exception as e:
            print(f"❌ Error unchecking airbags checkbox: {e}")

        # Product details section click
        try:
            element = await page.querySelector('a[href="#tiedownsgrommets"]')
            await page.evaluate('(element) => { element.scrollIntoView({ behavior: "smooth", block: "center" }); }', element)
            await element.click()
            await asyncio.sleep(2)
        except Exception as e:
            print(f"❌ Error clicking product details: {e}")

        #scroll to the warranty section for add to cart.
        try:
            element = await page.waitForSelector('img[alt="Assurance Plus"]', {'visible': True, 'timeout': 10000})
            await page.evaluate('(element) => { element.scrollIntoView({ behavior: "smooth", block: "center" }); }', element)
            await asyncio.sleep(2)  # Small delay after scroll
        except Exception as e:
            print(f"Failed to scroll to the warranty section: {e}")

        # Add to cart button click
        try:
            element = await page.querySelector('#product-addtocart-button')
            await page.evaluate('(element) => { element.scrollIntoView({ behavior: "smooth", block: "center" }); }', element)
            await element.click()
        except Exception as e:
            print(f"❌ Error clicking add to cart: {e}")

        # View cart button to be present and visible
        try:
            element = await page.waitForSelector('a.action.viewcart[data-id="view_cart"]', {'visible': True, 'timeout': 10000})
            await page.evaluate('(element) => { element.scrollIntoView({ behavior: "smooth", block: "center" }); }', element)
            await asyncio.sleep(5)
            await element.click()
        except Exception as e:
            print(f"❌ Error clicking view cart: {e}")

        await asyncio.sleep(15)

        # Click on continue shopping button
        try:
            element = await page.waitForSelector('a.action-continue-shopping', {'visible': True, 'timeout': 15000})
            await page.evaluate('(element) => { element.scrollIntoView({ behavior: "smooth", block: "center" }); }', element)
            await asyncio.sleep(5)
            await element.click()
        except Exception as e:
            print(f"❌ Error clicking continue shopping: {e}")

        # Click on continue shopping button pop up no
        try:
            element = await page.waitForSelector('button.action.primary.action-dismiss.action-small', {'visible': True, 'timeout': 10000})
            await page.evaluate('(element) => { element.scrollIntoView({ behavior: "smooth", block: "center" }); }', element)
            await asyncio.sleep(5)
            await element.click()
        except Exception as e:
            print(f"❌ Error dismissing continue shopping popup: {e}")

        # Click on delete product button
        try:
            element = await page.waitForSelector('a.action-delete', {'visible': True, 'timeout': 10000})
            await page.evaluate('(element) => { element.scrollIntoView({ behavior: "smooth", block: "center" }); }', element)
            await asyncio.sleep(5)
            await element.click()
        except Exception as e:
            print(f"❌ Error clicking delete product: {e}")

        # Click on delete product button pop up no
        try:
            element = await page.waitForSelector('button.action.primary.action-dismiss.action-small', {'visible': True, 'timeout': 10000})
            await page.evaluate('(element) => { element.scrollIntoView({ behavior: "smooth", block: "center" }); }', element)
            await asyncio.sleep(5)
            await element.click()
        except Exception as e:
            print(f"❌ Error dismissing delete product popup: {e}")

        # Click on available offer
        try:
            element = await page.waitForSelector('#cart-offer-link', {'visible': True, 'timeout': 10000})
            await page.evaluate('(element) => { element.scrollIntoView({ behavior: "smooth", block: "center" }); }', element)
            await asyncio.sleep(5)
            await element.click()
        except Exception as e:
            print(f"❌ Error clicking available offer: {e}")

        # Click on coupon field and enter coupon code
        try:
            element = await page.waitForSelector('#coupon_code_popup', {'visible': True, 'timeout': 10000})
            await page.evaluate('(element) => { element.scrollIntoView({ behavior: "smooth", block: "center" }); }', element)
            await asyncio.sleep(5)
            await element.click()
            await element.type('QA')
        except Exception as e:
            print(f"❌ Error entering coupon code: {e}")

        # Click on apply button
        try:
            element = await page.waitForSelector('#applyCoupon', {'visible': True, 'timeout': 10000})
            await page.evaluate('(element) => { element.scrollIntoView({ behavior: "smooth", block: "center" }); }', element)
            await asyncio.sleep(5)
            await element.click()
        except Exception as e:
            print(f"❌ Error applying coupon: {e}")


        await asyncio.sleep(10)

        # Click on the apply button in side drawer
        try:
            element = await page.waitForSelector('.applyCurrCoupon', {'visible': True, 'timeout': 10000})
            await page.evaluate('(element) => { element.scrollIntoView({ behavior: "smooth", block: "center" }); }', element)
            await asyncio.sleep(5)  # Small delay after scroll
            await element.click()
        except Exception as e:
            print(f"❌ Error clicking apply button in side drawer: {e}")
        
        await asyncio.sleep(10)

        # Click on cancel button in coupon code field.
        try:
            element = await page.waitForSelector('img[alt="Cancel"]', {'visible': True, 'timeout': 10000})
            await page.evaluate('(element) => { element.scrollIntoView({ behavior: "smooth", block: "center" }); }', element)
            await asyncio.sleep(5)  # Small delay after scroll
            await element.click()
        except Exception as e:
            print(f"❌ Error clicking cancel button in coupon code field: {e}")

        await asyncio.sleep(10)

        #scroll to shipping method section.
        try:
            element = await page.waitForSelector('fieldset.fieldset.rate', {'visible': True, 'timeout': 10000})
            await page.evaluate('(element) => { element.scrollIntoView({ behavior: "smooth", block: "center" }); }', element)
            await asyncio.sleep(2)  # Small delay after scroll
        except Exception as e:
            print(f"❌ Error scrolling to shipping method: {e}")
        
        # Click shiping method priority.
        try:
            element = await page.waitForSelector('label[for*="priority"]', {'visible': True, 'timeout': 15000})
            await page.evaluate('(element) => { element.scrollIntoView({ behavior: "smooth", block: "center" }); }', element)
            await asyncio.sleep(2)  # Small delay after scroll
            await element.click()
        except Exception as e:
            print(f"❌ Error clicking shipping method priority: {e}")

        #Remove assurance charge.
        try:
            element = await page.waitForSelector('input[name="remove_warranty"]', {'visible': True, 'timeout': 10000})
            await page.evaluate('(element) => { element.scrollIntoView({ behavior: "smooth", block: "center" }); }', element)
            await asyncio.sleep(5)  # Small delay after scroll
            await element.click()
        except Exception as e:
            print(f"❌ Error removing assurance charge: {e}")

        #Select assurance charge.
        try:
            element = await page.waitForSelector('input[data-title="1 Year"]', {'visible': True, 'timeout': 10000})
            await page.evaluate('(element) => { element.scrollIntoView({ behavior: "smooth", block: "center" }); }', element)
            await asyncio.sleep(5)  # Small delay after scroll
            await element.click()
        except Exception as e:
            print(f"❌ Error selecting assurance charge: {e}")

        #scroll to order summary section.
        element = await page.waitForSelector('#secure_checkout', {'visible': True, 'timeout': 10000})
        await page.evaluate('(element) => { element.scrollIntoView({ behavior: "smooth", block: "center" }); }', element)
        await asyncio.sleep(2)  # Small delay after scroll

        await asyncio.sleep(6)

        #Click amazon pay button.
        try:
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
        except Exception as e:
            print(f"❌ Error with Amazon Pay button: {e}")

        #Click link button.
        try:
            element = await page.waitForSelector('#payment-request-button-cart iframe', {'visible': True, 'timeout': 10000})
            await page.evaluate('(element) => { element.scrollIntoView({ behavior: "smooth", block: "center" }); }', element)
            await asyncio.sleep(2)  # Small delay after scroll
            await element.click()

            # Wait for new window to open and get all pages
            pages = await browser.pages()

            # Close the link window (last one in the list)
            if len(pages) > 1:
                await pages[-1].close()
        except Exception as e:
            print(f"❌ Error with Link button: {e}")

        await asyncio.sleep(10)

        #scroll to order summary section.
        try:
            element = await page.waitForSelector('#secure_checkout', {'visible': True, 'timeout': 10000})
            await page.evaluate('(element) => { element.scrollIntoView({ behavior: "smooth", block: "center" }); }', element)
            await asyncio.sleep(2)  # Small delay after scroll
        except Exception as e:
            print(f"❌ Error scrolling to order summary: {e}")

        # Click on secure checkout button.
        try:
            element = await page.waitForSelector('#secure_checkout > span.button-text', {'visible': True, 'timeout': 10000})
            await page.evaluate('(element) => { element.scrollIntoView({ behavior: "smooth", block: "center" }); }', element)
            await asyncio.sleep(2)  # Small delay after scroll
            await element.click()
        except Exception as e:
            print(f"❌ Error clicking secure checkout button: {e}")

        await asyncio.sleep(15)

        try:
            # Click in email field and enter value
            element = await page.waitForSelector('input#customer-email', {'visible': True, 'timeout': 10000})
            await page.evaluate('(element) => { element.scrollIntoView({ behavior: "smooth", block: "center" }); }', element)
            await asyncio.sleep(2)  # Small delay after scroll
            await element.click()
            await element.type('harshil.shukla@commercepundit.com')
        except Exception as e:
            print(f"❌ Error with email field: {e}")

        try:
            element = await page.waitForSelector('#conifrm_email_address', {'visible': True, 'timeout': 10000})
            await page.evaluate('(element) => { element.scrollIntoView({ behavior: "smooth", block: "center" }); }', element)
            await asyncio.sleep(2)
            await element.click()
            await element.type('harshil.shukla@commercepundit.com')
        except Exception as e:
            print(f"❌ Error with confirm email field: {e}")

        try:
            # Click on first name field and enter value
            element = await page.waitForSelector('input[name="firstname"]', {'visible': True, 'timeout': 10000})
            await page.evaluate('(element) => { element.scrollIntoView({ behavior: "smooth", block: "center" }); }', element)
            await asyncio.sleep(2)
            await element.click()
            await element.type('cp')
        except Exception as e:
            print(f"❌ Error with first name field: {e}")

        try:
            # Click on last name field and enter value
            element = await page.waitForSelector('input[name="lastname"]', {'visible': True, 'timeout': 10000})
            await page.evaluate('(element) => { element.scrollIntoView({ behavior: "smooth", block: "center" }); }', element)
            await asyncio.sleep(2)
            await element.click()
            await element.type('test')
        except Exception as e:
            print(f"❌ Error with last name field: {e}")

        try:
            # Click on street address field and enter value
            element = await page.waitForSelector('input[name="street[0]"]:first-of-type', {'visible': True, 'timeout': 10000})
            await page.evaluate('(element) => { element.scrollIntoView({ behavior: "smooth", block: "center" }); }', element)
            await asyncio.sleep(2)
            await element.click()
            await element.type('street 1')
        except Exception as e:
            print(f"❌ Error with street address field: {e}")

        try:
            # Select value 'Georgia' directly without dropdown interaction
            element = await page.waitForSelector('select[name="region_id"]', {'visible': True, 'timeout': 10000})
            await page.evaluate('(element) => { element.scrollIntoView({ behavior: "smooth", block: "center" }); }', element)
            await asyncio.sleep(2)
            await page.select('select[name="region_id"]', '19')
            await asyncio.sleep(1)
        except Exception as e:
            print(f"❌ Error with region selection: {e}")

        try:
            # Click on city field and enter value
            element = await page.waitForSelector('input[name="city"]', {'visible': True, 'timeout': 10000})
            await page.evaluate('(element) => { element.scrollIntoView({ behavior: "smooth", block: "center" }); }', element)
            await asyncio.sleep(2)
            await element.click()
            await element.type('Suwanee')
        except Exception as e:
            print(f"❌ Error with city field: {e}")

        try:
            # Click on zip code field and enter value
            element = await page.waitForSelector('input[name="postcode"]', {'visible': True, 'timeout': 10000})
            await page.evaluate('(element) => { element.scrollIntoView({ behavior: "smooth", block: "center" }); }', element)
            await asyncio.sleep(2)
            await element.click()
            await element.type('10001')
        except Exception as e:
            print(f"❌ Error with zip code field: {e}")

        try:
            # Click on phone number field and enter value
            element = await page.waitForSelector('input[name="telephone"]', {'visible': True, 'timeout': 10000})
            await page.evaluate('(element) => { element.scrollIntoView({ behavior: "smooth", block: "center" }); }', element)
            await asyncio.sleep(2)
            await element.click()
            await element.type('9876543210')
        except Exception as e:
            print(f"❌ Error with phone number field: {e}")

        await asyncio.sleep(10)

        try:
            # Click on next button.  
            element = await page.waitForSelector('button.continue', {'visible': True, 'timeout': 10000})
            await page.evaluate('(element) => { element.scrollIntoView({ behavior: "smooth", block: "center" }); }', element)
            await asyncio.sleep(2)
            await element.click()
        except Exception as e:
            print(f"❌ Error clicking next button: {e}")

        await asyncio.sleep(10)

        try:
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
        except Exception as e:
            print(f"❌ Error with Amazon Pay button: {e}")

        try:
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
        except Exception as e:
            print(f"❌ Error with link button: {e}")

        try:
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
                print("✅ Closed the PayPal popup window")
        except Exception as e:
            print(f"❌ Error with PayPal button: {e}")

        try:
            # Click on checkbox to use billing address as shipping address.  
            element = await page.waitForSelector('span[data-bind="i18n: \'My billing and shipping address are the same\'"]', {'visible': True, 'timeout': 10000})
            await page.evaluate('(element) => { element.scrollIntoView({ behavior: "smooth", block: "center" }); }', element)
            await asyncio.sleep(2)  # Small delay after scroll
            await element.click()
        except Exception as e:
            print(f"❌ Error clicking billing/shipping address checkbox: {e}")

        try:
            # Click on checkbox to use billing address as shipping address.  
            element = await page.waitForSelector('span[data-bind="i18n: \'My billing and shipping address are the same\'"]', {'visible': True, 'timeout': 10000})
            await page.evaluate('(element) => { element.scrollIntoView({ behavior: "smooth", block: "center" }); }', element)
            await asyncio.sleep(2)  # Small delay after scroll
            await element.click()
        except Exception as e:
            print(f"❌ Error clicking billing/shipping address checkbox (2nd time): {e}")
        
        await asyncio.sleep(5)

        try:
            # Click on coupon code field and enter value.  
            element = await page.waitForSelector('#discount-form', {'visible': True, 'timeout': 10000})
            await page.evaluate('(element) => { element.scrollIntoView({ behavior: "smooth", block: "center" }); }', element)
            await asyncio.sleep(2)  # Small delay after scroll
            await element.click()
            await element.type('OFFER4CP')
        except Exception as e:
            print(f"❌ Error entering coupon code: {e}")

        try:
            # Click on apply coupon button
            element = await page.waitForSelector('button.action-apply', {'visible': True, 'timeout': 10000})
            await page.evaluate('(element) => { element.scrollIntoView({ behavior: "smooth", block: "center" }); }', element)
            await asyncio.sleep(2)  # Small delay after scroll
            await element.click()
        except Exception as e:
            print(f"❌ Error applying coupon: {e}")
                
        await asyncio.sleep(10)
        
        try:
            # Click on edit shipping address button.  
            element = await page.waitForSelector("button[data-bind='click: back']", {'visible': True, 'timeout': 10000})
            await page.evaluate('(element) => { element.scrollIntoView({ behavior: "smooth", block: "center" }); }', element)
            await asyncio.sleep(2)  # Small delay after scroll
            await element.click()
        except Exception as e:
            print(f"❌ Error clicking edit shipping address: {e}")

        try:
            # Click on next button.  
            element = await page.waitForSelector('button.continue', {'visible': True, 'timeout': 10000})
            await page.evaluate('(element) => { element.scrollIntoView({ behavior: "smooth", block: "center" }); }', element)
            await asyncio.sleep(2)  # Small delay after scroll
            await element.click()
        except Exception as e:
            print(f"❌ Error clicking next button: {e}")

        try:
            # Click on edit shipping address button.  
            element = await page.waitForSelector('button[data-bind="click: backToShippingMethod"]', {'visible': True, 'timeout': 10000})
            await page.evaluate('(element) => { element.scrollIntoView({ behavior: "smooth", block: "center" }); }', element)
            await asyncio.sleep(2)  # Small delay after scroll
            await element.click()
        except Exception as e:
            print(f"❌ Error clicking edit shipping address (2nd time): {e}")
        
        try:
            # Click on next button.  
            element = await page.waitForSelector('button.continue', {'visible': True, 'timeout': 10000})
            await page.evaluate('(element) => { element.scrollIntoView({ behavior: "smooth", block: "center" }); }', element)
            await asyncio.sleep(2)  # Small delay after scroll
            await element.click()
        except Exception as e:
            print(f"❌ Error clicking next button (2nd time): {e}")

        try:
            # Click on comment box.  
            element = await page.waitForSelector('#co-payment-form > fieldset > div.checkout-agreements-block.custom > div.payment-option._collapsible.opc-payment-additional.comment.last > div.payment-option-title.field.choice', {'visible': True, 'timeout': 10000})
            await page.evaluate('(element) => { element.scrollIntoView({ behavior: "smooth", block: "center" }); }', element)
            await asyncio.sleep(2)  # Small delay after scroll
            await element.click()
        except Exception as e:
            print(f"❌ Error clicking comment box: {e}")
        
        try:
            # Type comment in comment box.  
            element = await page.waitForSelector('div[class="payment-option _collapsible opc-payment-additional comment last _active"] textarea[placeholder="Enter your comment..."]', {'visible': True, 'timeout': 10000})
            await page.evaluate('(element) => { element.scrollIntoView({ behavior: "smooth", block: "center" }); }', element)
            await asyncio.sleep(2)  # Small delay after scroll
            await element.click()
            await element.type('CP test order do not process')
        except Exception as e:
            print(f"❌ Error typing comment: {e}")

        try:
            # Click on PO order button.  
            element = await page.waitForSelector('label[for="popayment"]', {'visible': True, 'timeout': 10000})
            await page.evaluate('(element) => { element.scrollIntoView({ behavior: "smooth", block: "center" }); }', element)
            await asyncio.sleep(2)  # Small delay after scroll
            await element.click()
        except Exception as e:
            print(f"❌ Error clicking PO order button: {e}")

        try:
            # Click on CC.  
            element = await page.waitForSelector('label[for="onlycard_payment_method"]', {'visible': True, 'timeout': 10000})
            await page.evaluate('(element) => { element.scrollIntoView({ behavior: "smooth", block: "center" }); }', element)
            await asyncio.sleep(2)  # Small delay after scroll
            await element.click()
        except Exception as e:
            print(f"❌ Error clicking CC button: {e}")

        try:
            # Click on PO order button.  
            element = await page.waitForSelector('label[for="popayment"]', {'visible': True, 'timeout': 10000})
            await page.evaluate('(element) => { element.scrollIntoView({ behavior: "smooth", block: "center" }); }', element)
            await asyncio.sleep(2)  # Small delay after scroll
            await element.click()
        except Exception as e:
            print(f"❌ Error clicking PO order button (2nd time): {e}")

        try:
            # Click on upload button
            element = await page.waitForSelector('#po_image_file', {'visible': True, 'timeout': 10000})
            await page.evaluate('(element) => { element.scrollIntoView({ behavior: "smooth", block: "center" }); }', element)
            await asyncio.sleep(2)  # Small delay after scroll
            
            # Upload test file
            await element.uploadFile('pdf_1.pdf')
            await asyncio.sleep(2)  # Small delay after upload
        except Exception as e:
            print(f"❌ Error uploading file: {e}")

        try:
            # Click on place order button.  
            element = await page.waitForSelector('#place-order-trigger', {'visible': True, 'timeout': 10000})
            await page.evaluate('(element) => { element.scrollIntoView({ behavior: "smooth", block: "center" }); }', element)
            await asyncio.sleep(2)  # Small delay after scroll
            await element.click()
        except Exception as e:
            print(f"❌ Error clicking place order button: {e}")
        
        await asyncio.sleep(15)

        # Extract and print order ID
        order_id_element = await page.waitForSelector('a.order-number > strong', {'visible': True, 'timeout': 10000})
        order_id = await page.evaluate('(element) => element.textContent', order_id_element)
        print(f"Order ID: {order_id}")
        

    except Exception as e:
        print(f"⚠️ Action failed: {str(e)}")

    # Wait to capture events after actions
    await asyncio.sleep(10)
    # Save all captured events
    date = datetime.datetime.now().strftime('%Y-%m-%d')
    filename = f'adb_events_{date}.json'
    with open(filename, 'w') as f:
        json.dump(adb_events, f, indent=2)
        print(f"✅ Saved {len(adb_events)} adb_* events to {filename}")


    await browser.close()

# Run the function
asyncio.run(capture_events_with_actions())




#Sending email
subject = "Adobe event"
body = "Please find the adobe events results below."
sender_email = "cp.harshil@gmail.com"
recipient_emails = ["harshil.shukla@commercepundit.com"]
sender_password = "culo jpqg pmtr iafc"
smtp_server = 'smtp.gmail.com'
smtp_port = 465
path_to_file = f'adb_events_{datetime.datetime.now().strftime("%Y-%m-%d")}.json'

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
                message.attach(MIMEApplication(file.read(), Name=os.path.basename(path_to_file)))
            
            # Send email
            server.sendmail(sender_email, recipient, message.as_string())
            print(f"✅ Email sent successfully to {recipient}!")
            
except smtplib.SMTPAuthenticationError:
    print("❌ Error: Email authentication failed. Please check your username and password.")
except smtplib.SMTPException as e:
    print(f"❌ Error sending email: {str(e)}")
except Exception as e:
    print(f"❌ Unexpected error: {str(e)}")
