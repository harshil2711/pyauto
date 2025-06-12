import asyncio
import json
from playwright.async_api import async_playwright, Page, BrowserContext
import smtplib
from email.mime.multipart import MIMEMultipart
from email.message import EmailMessage
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import datetime
import os
import logging
from playwright._impl._errors import TargetClosedError # Import for specific error handling

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

adb_events = []

def handle_console(msg):
    asyncio.create_task(process_console_message(msg))

async def process_console_message(msg):
    try:
        for arg in msg.args:
            val = await arg.json_value()
            if isinstance(val, dict) and val.get('event', '').startswith('adb_'):
                adb_events.append(val)
                logger.info(f"✅ Captured: {val['event']}")
    except Exception as e:
        logger.warning(f"Error processing console message: {e}")
        pass # Silently ignore parsing errors for console messages

async def capture_events_with_actions():
    browser = None
    context = None
    page = None

    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(
                headless=False,
                channel="chrome",
                slow_mo=200,
                args=['--start-maximized']
            )
            async with browser:
                context = await browser.new_context(no_viewport=True)
                async with context:
                    page = await context.new_page()

                    # Attach console listener
                    page.on('console', handle_console)

                    # Load initial page
                    url = 'https://www.coversandall.com/patio-furniture-covers/seating-covers/chair-covers/chair-cover-design-1-p'
                    logger.info(f"🌐 Navigating to: {url}")
                    
                    try:
                        await page.goto(url, wait_until="load", timeout=90000)
                        await page.wait_for_selector('h1.page-title', state='visible', timeout=30000)
                        logger.info("✅ Product page loaded and key element visible.")
                    except Exception as e:
                        logger.error(f"⚠️ Could not load initial page or find key element: {e}")
                        # If critical navigation fails, we might want to exit or take a different path
                        # For now, allowing it to continue for demonstration of skipping
                        pass 

                    await asyncio.sleep(5)

                    logger.info("Starting actions...")

                    try:
                        breadcrumb_locator = page.locator('.breadcrumbs ul.items li.item:nth-child(3) a')
                        await breadcrumb_locator.scroll_into_view_if_needed()
                        
                        async with context.expect_page() as new_page_info:
                            await page.keyboard.down('Control')
                            await breadcrumb_locator.click()
                            await page.keyboard.up('Control')
                        new_tab = await new_page_info.value
                        logger.info(f"New tab opened: {new_tab.url}")
                        await new_tab.close() 
                        logger.info("New tab closed.")
                    except Exception as e:
                        logger.warning(f"⚠️ Could not click breadcrumb or close new tab, skipping: {e}")
                    await asyncio.sleep(2)

                    try:
                        product_spec_locator = page.locator('#product-specification-link')
                        await product_spec_locator.click()
                        logger.info("✅ Clicked product specification")
                    except Exception as e:
                        logger.warning(f"⚠️ Could not click product specification, skipping: {e}")
                    await asyncio.sleep(2)

                    try:
                        quantity_plus_locator = page.locator('#action-plus')
                        await quantity_plus_locator.click()
                        logger.info("✅ Updated quantity")
                    except Exception as e:
                        logger.warning(f"⚠️ Could not update quantity, skipping: {e}")
                    await asyncio.sleep(3)

                    try:
                        standard_dimension_locator = page.locator('li[data-dimension]:first-child')
                        await standard_dimension_locator.click()
                        logger.info("✅ Clicked standard dimension")
                    except Exception as e:
                        logger.warning(f"⚠️ Could not click standard dimension, skipping: {e}")
                    await asyncio.sleep(3)

                    try:
                        tooltip_locator = page.locator('#measurement-component span.field-tooltip-action.action-help[data-dropdown="true"]')
                        await tooltip_locator.hover()
                        logger.info("✅ Hovered on tooltip")
                    except Exception as e:
                        logger.warning(f"⚠️ Could not hover on tooltip, skipping: {e}")
                    await asyncio.sleep(2)

                    try:
                        warranty_checkbox_locator = page.locator('input[data-label="1 Year"]')
                        await warranty_checkbox_locator.click()
                        logger.info("✅ Checked warranty checkbox")
                    except Exception as e:
                        logger.warning(f"⚠️ Could not check warranty checkbox, skipping: {e}")
                    await asyncio.sleep(2)

                    try:
                        # Attempt to uncheck even if previous check failed, as this is a separate action
                        warranty_checkbox_locator = page.locator('input[data-label="1 Year"]')
                        await warranty_checkbox_locator.click(force=True)
                        logger.info("✅ Unchecked warranty checkbox")
                    except Exception as e:
                        logger.warning(f"⚠️ Could not uncheck warranty checkbox, skipping: {e}")
                    await asyncio.sleep(2)

                    try:
                        fabric_color_locator = page.locator('li.tool-color').filter(has_text("Brown"))
                        await fabric_color_locator.click()
                        logger.info("✅ Clicked fabric color (Brown)")
                    except Exception as e:
                        logger.warning(f"⚠️ Could not click fabric color (Brown), skipping: {e}")
                    await asyncio.sleep(2)

                    try:
                        dimension_h1_locator = page.locator('#H1')
                        await dimension_h1_locator.click()
                        await dimension_h1_locator.fill('12') 
                        logger.info("✅ Cleared and changed dimension to 12")
                    except Exception as e:
                        logger.warning(f"⚠️ Could not change dimension, skipping: {e}")
                    await asyncio.sleep(2)

                    try:
                        airbags_checkbox_locator = page.locator('label[data-id="Air Bags"]')
                        await airbags_checkbox_locator.click()
                        logger.info("✅ Checked Airbags checkbox")
                    except Exception as e:
                        logger.warning(f"⚠️ Could not check Airbags checkbox, skipping: {e}")
                    await asyncio.sleep(2)

                    try:
                        # Attempt to uncheck even if previous check failed
                        airbags_checkbox_locator = page.locator('label[data-id="Air Bags"]')
                        await airbags_checkbox_locator.click()
                        logger.info("✅ Unchecked Airbags checkbox")
                    except Exception as e:
                        logger.warning(f"⚠️ Could not uncheck Airbags checkbox, skipping: {e}")
                    await asyncio.sleep(2)

                    try:
                        tiedown_grommets_locator = page.locator('a[href="#tiedownsgrommets"]')
                        await tiedown_grommets_locator.click()
                        logger.info("✅ Clicked 'Tiedowns & Grommets' link")
                    except Exception as e:
                        logger.warning(f"⚠️ Could not click 'Tiedowns & Grommets' link, skipping: {e}")
                    await asyncio.sleep(2)

                    try:
                        back_to_top_locator = page.locator('#back-to-top')
                        await back_to_top_locator.click()
                        logger.info("✅ Clicked 'Back to Top' button")
                    except Exception as e:
                        logger.warning(f"⚠️ Could not click 'Back to Top' button, skipping: {e}")
                    await asyncio.sleep(2)

                    try:
                        add_to_cart_locator = page.locator('#product-addtocart-button')
                        await add_to_cart_locator.click()
                        logger.info("✅ Clicked 'Add to Cart'")
                    except Exception as e:
                        logger.warning(f"⚠️ Could not click 'Add to Cart', skipping: {e}")

                    try:
                        view_cart_locator = page.locator('a.action.viewcart[data-id="view_cart"]')
                        await view_cart_locator.wait_for(state='visible', timeout=10000)
                        await view_cart_locator.click()
                        logger.info("✅ Clicked 'View Cart'")
                    except Exception as e:
                        logger.warning(f"⚠️ Could not click 'View Cart', skipping: {e}")
                    await asyncio.sleep(15)

                    try:
                        continue_shopping_locator = page.locator('a.action-continue-shopping')
                        await continue_shopping_locator.wait_for(state='visible', timeout=15000)
                        await continue_shopping_locator.click()
                        logger.info("✅ Clicked 'Continue Shopping'")
                    except Exception as e:
                        logger.warning(f"⚠️ Could not click 'Continue Shopping', skipping: {e}")
                    await asyncio.sleep(5)

                    try:
                        continue_shopping_popup_no_locator = page.locator('button.action.primary.action-dismiss.action-small')
                        await continue_shopping_popup_no_locator.wait_for(state='visible', timeout=10000)
                        await continue_shopping_popup_no_locator.click()
                        logger.info("✅ Clicked 'No' on continue shopping popup")
                    except Exception as e:
                        logger.warning(f"⚠️ Could not click 'No' on continue shopping popup, skipping: {e}")
                    await asyncio.sleep(5)

                    try:
                        delete_product_locator = page.locator('a.action-delete')
                        await delete_product_locator.wait_for(state='visible', timeout=10000)
                        await delete_product_locator.click()
                        logger.info("✅ Clicked delete product button")
                    except Exception as e:
                        logger.warning(f"⚠️ Could not click delete product button, skipping: {e}")
                    await asyncio.sleep(5)

                    try:
                        delete_product_popup_no_locator = page.locator('button.action.primary.action-dismiss.action-small')
                        await delete_product_popup_no_locator.wait_for(state='visible', timeout=10000)
                        await delete_product_popup_no_locator.click()
                        logger.info("✅ Clicked 'No' on delete product popup")
                    except Exception as e:
                        logger.warning(f"⚠️ Could not click 'No' on delete product popup, skipping: {e}")
                    await asyncio.sleep(5)

                    try:
                        available_offer_locator = page.locator('#cart-offer-link')
                        await available_offer_locator.wait_for(state='visible', timeout=10000)
                        await available_offer_locator.click()
                        logger.info("✅ Clicked 'Available Offer'")
                    except Exception as e:
                        logger.warning(f"⚠️ Could not click 'Available Offer', skipping: {e}")
                    await asyncio.sleep(5)

                    try:
                        coupon_code_popup_locator = page.locator('#coupon_code_popup')
                        await coupon_code_popup_locator.wait_for(state='visible', timeout=10000)
                        await coupon_code_popup_locator.click()
                        await coupon_code_popup_locator.type('QA')
                        logger.info("✅ Entered 'QA' in coupon code field")
                    except Exception as e:
                        logger.warning(f"⚠️ Could not interact with coupon code field, skipping: {e}")

                    try:
                        apply_coupon_button_locator = page.locator('#applyCoupon')
                        await apply_coupon_button_locator.wait_for(state='visible', timeout=10000)
                        await apply_coupon_button_locator.click()
                        logger.info("✅ Clicked 'Apply' coupon button")
                    except Exception as e:
                        logger.warning(f"⚠️ Could not click 'Apply' coupon button, skipping: {e}")
                    await asyncio.sleep(10)

                    try:
                        apply_curr_coupon_locator = page.locator('.applyCurrCoupon')
                        await apply_curr_coupon_locator.wait_for(state='visible', timeout=10000)
                        await apply_curr_coupon_locator.click()
                        logger.info("✅ Clicked 'Apply' button in side drawer")
                    except Exception as e:
                        logger.warning(f"⚠️ Could not click 'Apply' button in side drawer, skipping: {e}")
                    await asyncio.sleep(10)

                    try:
                        cancel_coupon_locator = page.locator('img[alt="Cancel"]')
                        await cancel_coupon_locator.wait_for(state='visible', timeout=10000)
                        await cancel_coupon_locator.click()
                        logger.info("✅ Clicked 'Cancel' button in coupon code field")
                    except Exception as e:
                        logger.warning(f"⚠️ Could not click 'Cancel' button, skipping: {e}")
                    await asyncio.sleep(10)

                    try:
                        shipping_fieldset_locator = page.locator('fieldset.fieldset.rate')
                        await shipping_fieldset_locator.scroll_into_view_if_needed()
                        logger.info("✅ Scrolled to shipping method section")
                    except Exception as e:
                        logger.warning(f"⚠️ Could not scroll to shipping method section, skipping: {e}")
                    await asyncio.sleep(2)

                    try:
                        shipping_priority_locator = page.locator('label[for*="priority"]')
                        await shipping_priority_locator.wait_for(state='visible', timeout=15000)
                        await shipping_priority_locator.click()
                        logger.info("✅ Clicked 'Priority' shipping method")
                    except Exception as e:
                        logger.warning(f"⚠️ Could not click 'Priority' shipping method, skipping: {e}")
                    await asyncio.sleep(2)

                    try:
                        remove_warranty_locator = page.locator('input[name="remove_warranty"]')
                        await remove_warranty_locator.wait_for(state='visible', timeout=10000)
                        await remove_warranty_locator.click()
                        logger.info("✅ Removed assurance charge")
                    except Exception as e:
                        logger.warning(f"⚠️ Could not remove assurance charge, skipping: {e}")
                    await asyncio.sleep(5)

                    try:
                        select_warranty_locator = page.locator('input[data-title="1 Year"]')
                        await select_warranty_locator.wait_for(state='visible', timeout=10000)
                        await select_warranty_locator.click()
                        logger.info("✅ Selected assurance charge")
                    except Exception as e:
                        logger.warning(f"⚠️ Could not select assurance charge, skipping: {e}")
                    await asyncio.sleep(5)

                    try:
                        secure_checkout_locator = page.locator('#secure_checkout')
                        await secure_checkout_locator.scroll_into_view_if_needed()
                        logger.info("✅ Scrolled to order summary section")
                    except Exception as e:
                        logger.warning(f"⚠️ Could not scroll to order summary section, skipping: {e}")
                    await asyncio.sleep(2)
                    await asyncio.sleep(6)

                    try:
                        amazon_pay_button_locator = page.locator('div.amazonpay-merchant-shadow-root-parent-element-for-executing-modal-script.amazonpay-button-parent-container-checkout-A2KGO0QV9T7EUE')
                        await amazon_pay_button_locator.wait_for(state='visible', timeout=10000)
                        
                        async with context.expect_page() as new_page_info:
                            await amazon_pay_button_locator.click()
                        amazon_pay_popup = await new_page_info.value
                        
                        logger.info("✅ Clicked Amazon Pay button. Waiting for popup...")
                        await asyncio.sleep(5)
                        
                        await amazon_pay_popup.close()
                        logger.info("✅ Closed the Amazon Pay popup window")
                    except Exception as e:
                        logger.warning(f"⚠️ Could not interact with Amazon Pay button or popup, skipping: {e}")
                    await asyncio.sleep(2)

                    try:
                        link_button_iframe_locator = page.locator('#payment-request-button-cart iframe')
                        await link_button_iframe_locator.wait_for(state='visible', timeout=10000)
                        
                        async with context.expect_page() as new_page_info:
                            await link_button_iframe_locator.click()
                        link_popup = await new_page_info.value

                        logger.info("✅ Clicked Link button. Waiting for popup...")
                        await asyncio.sleep(5)

                        await link_popup.close()
                        logger.info("✅ Closed the Link popup window")
                    except Exception as e:
                        logger.warning(f"⚠️ Could not interact with Link button or popup, skipping: {e}")
                    await asyncio.sleep(10)

                    try:
                        await secure_checkout_locator.scroll_into_view_if_needed()
                        logger.info("✅ Scrolled to order summary section (again)")
                    except Exception as e:
                        logger.warning(f"⚠️ Could not scroll to order summary section (again), skipping: {e}")
                    await asyncio.sleep(2)

                    try:
                        secure_checkout_button_locator = page.locator('#secure_checkout > span.button-text')
                        await secure_checkout_button_locator.wait_for(state='visible', timeout=10000)
                        await secure_checkout_button_locator.click()
                        logger.info("✅ Clicked 'Secure Checkout' button")
                    except Exception as e:
                        logger.warning(f"⚠️ Could not click 'Secure Checkout' button, skipping: {e}")
                    await asyncio.sleep(10)

                    try:
                        customer_email_locator = page.locator('input#customer-email')
                        await customer_email_locator.wait_for(state='visible', timeout=10000)
                        await customer_email_locator.fill('harshil.shukla@commercepundit.com')
                        logger.info("✅ Filled customer email")
                    except Exception as e:
                        logger.warning(f"⚠️ Could not fill customer email, skipping: {e}")

                    try:
                        confirm_email_locator = page.locator('#conifrm_email_address')
                        await confirm_email_locator.wait_for(state='visible', timeout=10000)
                        await confirm_email_locator.fill('harshil.shukla@commercepundit.com')
                        logger.info("✅ Confirmed email address")
                    except Exception as e:
                        logger.warning(f"⚠️ Could not confirm email address, skipping: {e}")
                    await asyncio.sleep(2)

                    try:
                        first_name_locator = page.locator('input[name="firstname"]')
                        await first_name_locator.wait_for(state='visible', timeout=10000)
                        await first_name_locator.fill('cp')
                        logger.info("✅ Filled first name")
                    except Exception as e:
                        logger.warning(f"⚠️ Could not fill first name, skipping: {e}")
                    await asyncio.sleep(2)

                    try:
                        last_name_locator = page.locator('input[name="lastname"]')
                        await last_name_locator.wait_for(state='visible', timeout=10000)
                        await last_name_locator.fill('test')
                        logger.info("✅ Filled last name")
                    except Exception as e:
                        logger.warning(f"⚠️ Could not fill last name, skipping: {e}")
                    await asyncio.sleep(2)

                    try:
                        street_address_locator = page.locator('input[name="street[0]"]:first-of-type')
                        await street_address_locator.wait_for(state='visible', timeout=10000)
                        await street_address_locator.fill('street 1')
                        logger.info("✅ Filled street address")
                    except Exception as e:
                        logger.warning(f"⚠️ Could not fill street address, skipping: {e}")
                    await asyncio.sleep(2)

                    try:
                        region_dropdown_locator = page.locator('select[name="region_id"]')
                        await region_dropdown_locator.wait_for(state='visible', timeout=10000)
                        await region_dropdown_locator.select_option('19') # Select by value
                        logger.info("✅ Selected 'Georgia' in region dropdown")
                    except Exception as e:
                        logger.warning(f"⚠️ Could not select 'Georgia' in region dropdown, skipping: {e}")
                    await asyncio.sleep(1)

                    try:
                        city_locator = page.locator('input[name="city"]')
                        await city_locator.wait_for(state='visible', timeout=10000)
                        await city_locator.fill('Suwanee')
                        logger.info("✅ Filled city")
                    except Exception as e:
                        logger.warning(f"⚠️ Could not fill city, skipping: {e}")
                    await asyncio.sleep(2)

                    try:
                        postcode_locator = page.locator('input[name="postcode"]')
                        await postcode_locator.wait_for(state='visible', timeout=10000)
                        await postcode_locator.fill('30024')
                        logger.info("✅ Filled zip code")
                    except Exception as e:
                        logger.warning(f"⚠️ Could not fill zip code, skipping: {e}")
                    await asyncio.sleep(2)

                    try:
                        telephone_locator = page.locator('input[name="telephone"]')
                        await telephone_locator.wait_for(state='visible', timeout=10000)
                        await telephone_locator.fill('9876543210')
                        logger.info("✅ Filled phone number")
                    except Exception as e:
                        logger.warning(f"⚠️ Could not fill phone number, skipping: {e}")
                    await asyncio.sleep(2)

                    await asyncio.sleep(10)

                    try:
                        shipping_standard_ground_locator = page.locator('#label_method_matrixrate_standardground_matrixrate')
                        await shipping_standard_ground_locator.wait_for(state='visible', timeout=10000)
                        await shipping_standard_ground_locator.click()
                        logger.info("✅ Clicked 'Standard Ground' shipping option")
                    except Exception as e:
                        logger.warning(f"⚠️ Could not click 'Standard Ground' shipping option, skipping: {e}")
                    await asyncio.sleep(2)

                    try:
                        continue_button_locator = page.locator('button.continue')
                        await continue_button_locator.wait_for(state='visible', timeout=10000)
                        await continue_button_locator.click()
                        logger.info("✅ Clicked 'Next' button on shipping page")
                    except Exception as e:
                        logger.warning(f"⚠️ Could not click 'Next' button on shipping page, skipping: {e}")
                    await asyncio.sleep(10)

                    try:
                        amazon_pay_checkout_locator = page.locator('.pay-icon.checkout-amazon-pay.amazon-button-container')
                        await amazon_pay_checkout_locator.wait_for(state='visible', timeout=10000)
                        
                        async with context.expect_page() as new_page_info:
                            await amazon_pay_checkout_locator.click()
                        amazon_pay_popup_checkout = await new_page_info.value

                        logger.info("✅ Clicked Amazon Pay button in checkout. Waiting for popup...")
                        await asyncio.sleep(5)
                        
                        await amazon_pay_popup_checkout.close()
                        logger.info("✅ Closed the Amazon Pay popup window from checkout")
                    except Exception as e:
                        logger.warning(f"⚠️ Could not interact with Amazon Pay button in checkout, skipping: {e}")
                    await asyncio.sleep(2)

                    try:
                        link_button_checkout_locator = page.locator('#payment-request-button')
                        await link_button_checkout_locator.wait_for(state='visible', timeout=10000)
                        
                        async with context.expect_page() as new_page_info:
                            await link_button_checkout_locator.click()
                        link_popup_checkout = await new_page_info.value

                        logger.info("✅ Clicked Link button in checkout. Waiting for popup...")
                        await asyncio.sleep(5)
                        
                        await link_popup_checkout.close()
                        logger.info("✅ Closed the Link popup window from checkout")
                    except Exception as e:
                        logger.warning(f"⚠️ Could not interact with Link button in checkout, skipping: {e}")
                    await asyncio.sleep(2)

                    try:
                        paypal_iframe_locator = page.locator('#braintree-paypal-express-checkout-button iframe')
                        await paypal_iframe_locator.wait_for(state='visible', timeout=10000)
                        
                        async with context.expect_page() as new_page_info:
                            await paypal_iframe_locator.click()
                        paypal_popup = await new_page_info.value

                        logger.info("✅ Clicked PayPal button. Waiting for popup...")
                        await asyncio.sleep(5)
                        
                        await paypal_popup.close()
                        logger.info("✅ Closed the PayPal popup window")
                    except Exception as e:
                        logger.warning(f"⚠️ Could not interact with PayPal button or popup, skipping: {e}")
                    await asyncio.sleep(2)

                    try:
                        billing_shipping_same_checkbox_locator = page.locator('span[data-bind="i18n: \'My billing and shipping address are the same\'"]')
                        await billing_shipping_same_checkbox_locator.wait_for(state='visible', timeout=10000)
                        await billing_shipping_same_checkbox_locator.click()
                        logger.info("✅ Checked 'My billing and shipping address are the same'")
                    except Exception as e:
                        logger.warning(f"⚠️ Could not check billing/shipping checkbox, skipping: {e}")
                    await asyncio.sleep(2)

                    try:
                        # Attempt to uncheck even if previous check failed
                        billing_shipping_same_checkbox_locator = page.locator('span[data-bind="i18n: \'My billing and shipping address are the same\'"]')
                        await billing_shipping_same_checkbox_locator.click()
                        logger.info("✅ Unchecked 'My billing and shipping address are the same'")
                    except Exception as e:
                        logger.warning(f"⚠️ Could not uncheck billing/shipping checkbox, skipping: {e}")
                    await asyncio.sleep(5)

                    try:
                        discount_form_locator = page.locator('#discount-form')
                        await discount_form_locator.wait_for(state='visible', timeout=10000)
                        await discount_form_locator.locator('input').fill('CPQADISCOUNT')
                        logger.info("✅ Entered 'CPQADISCOUNT' in coupon code field")
                    except Exception as e:
                        logger.warning(f"⚠️ Could not enter coupon code, skipping: {e}")
                    await asyncio.sleep(2)

                    try:
                        apply_coupon_action_locator = page.locator('button.action-apply')
                        await apply_coupon_action_locator.wait_for(state='visible', timeout=10000)
                        await apply_coupon_action_locator.click()
                        logger.info("✅ Clicked 'Apply' coupon button")
                    except Exception as e:
                        logger.warning(f"⚠️ Could not click 'Apply' coupon button, skipping: {e}")
                    await asyncio.sleep(10)

                    try:
                        edit_shipping_address_locator = page.locator("button[data-bind='click: back']")
                        await edit_shipping_address_locator.wait_for(state='visible', timeout=10000)
                        await edit_shipping_address_locator.click()
                        logger.info("✅ Clicked 'Edit Shipping Address' button")
                    except Exception as e:
                        logger.warning(f"⚠️ Could not click 'Edit Shipping Address' button, skipping: {e}")
                    await asyncio.sleep(2)

                    try:
                        continue_after_edit_locator = page.locator('button.continue')
                        await continue_after_edit_locator.wait_for(state='visible', timeout=10000)
                        await continue_after_edit_locator.click()
                        logger.info("✅ Clicked 'Next' button after editing shipping address")
                    except Exception as e:
                        logger.warning(f"⚠️ Could not click 'Next' button after editing shipping address, skipping: {e}")
                    await asyncio.sleep(2)

                    try:
                        edit_shipping_method_locator = page.locator('button[data-bind="click: backToShippingMethod"]')
                        await edit_shipping_method_locator.wait_for(state='visible', timeout=10000)
                        await edit_shipping_method_locator.click()
                        logger.info("✅ Clicked 'Edit Shipping Method' button")
                    except Exception as e:
                        logger.warning(f"⚠️ Could not click 'Edit Shipping Method' button, skipping: {e}")
                    await asyncio.sleep(2)
                    
                    try:
                        continue_after_edit_shipping_locator = page.locator('button.continue')
                        await continue_after_edit_shipping_locator.wait_for(state='visible', timeout=10000)
                        await continue_after_edit_shipping_locator.click()
                        logger.info("✅ Clicked 'Next' button after editing shipping method")
                    except Exception as e:
                        logger.warning(f"⚠️ Could not click 'Next' button after editing shipping method, skipping: {e}")
                    await asyncio.sleep(2)

                    try:
                        comment_box_title_locator = page.locator('#co-payment-form > fieldset > div.checkout-agreements-block.custom > div.payment-option._collapsible.opc-payment-additional.comment.last > div.payment-option-title.field.choice')
                        await comment_box_title_locator.wait_for(state='visible', timeout=10000)
                        await comment_box_title_locator.click()
                        logger.info("✅ Clicked on comment box title")
                    except Exception as e:
                        logger.warning(f"⚠️ Could not click on comment box title, skipping: {e}")
                    await asyncio.sleep(2)
                    
                    try:
                        comment_textarea_locator = page.locator('div[class="payment-option _collapsible opc-payment-additional comment last _active"] textarea[placeholder="Enter your comment..."]')
                        await comment_textarea_locator.wait_for(state='visible', timeout=10000)
                        await comment_textarea_locator.fill('CP test order do not process')
                        logger.info("✅ Typed comment in comment box")
                    except Exception as e:
                        logger.warning(f"⚠️ Could not type comment in comment box, skipping: {e}")
                    await asyncio.sleep(2)

                    try:
                        po_payment_locator = page.locator('label[for="popayment"]')
                        await po_payment_locator.wait_for(state='visible', timeout=10000)
                        await po_payment_locator.click()
                        logger.info("✅ Selected 'PO Order' payment method")
                    except Exception as e:
                        logger.warning(f"⚠️ Could not select 'PO Order' payment method, skipping: {e}")
                    await asyncio.sleep(2)

                    try:
                        cc_payment_locator = page.locator('label[for="onlycard_payment_method"]')
                        await cc_payment_locator.wait_for(state='visible', timeout=10000)
                        await cc_payment_locator.click()
                        logger.info("✅ Selected 'Credit Card' payment method")
                    except Exception as e:
                        logger.warning(f"⚠️ Could not select 'Credit Card' payment method, skipping: {e}")
                    await asyncio.sleep(2)

                    try:
                        # Attempt to re-select PO even if previous selection failed
                        po_payment_locator = page.locator('label[for="popayment"]')
                        await po_payment_locator.click()
                        logger.info("✅ Re-selected 'PO Order' payment method")
                    except Exception as e:
                        logger.warning(f"⚠️ Could not re-select 'PO Order' payment method, skipping: {e}")
                    await asyncio.sleep(2)

                    try:
                        po_image_upload_locator = page.locator('#po_image_file')
                        await po_image_upload_locator.wait_for(state='visible', timeout=10000)
                        await po_image_upload_locator.set_input_files('pdf_1.pdf')
                        logger.info("✅ Uploaded 'pdf_1.pdf' for PO")
                    except Exception as e:
                        logger.warning(f"⚠️ Could not upload 'pdf_1.pdf' for PO, skipping: {e}")
                    await asyncio.sleep(2)

                    try:
                        place_order_locator = page.locator('#place-order-trigger')
                        await place_order_locator.wait_for(state='visible', timeout=10000)
                        await place_order_locator.click()
                        logger.info("✅ Clicked 'Place Order' button")
                    except Exception as e:
                        logger.warning(f"⚠️ Could not click 'Place Order' button, skipping: {e}")
                    await asyncio.sleep(15)

                    order_id = "N/A" # Initialize order_id
                    try:
                        order_id_element_locator = page.locator('a.order-number > strong')
                        await order_id_element_locator.wait_for(state='visible', timeout=10000)
                        order_id = await order_id_element_locator.text_content()
                        logger.info(f"Order ID: {order_id}")
                    except Exception as e:
                        logger.warning(f"⚠️ Could not extract Order ID, skipping: {e}")

    except Exception as e:
        logger.error(f"⚠️ An error occurred during automation: {str(e)}")
        if 'page' in locals() and page:
            try:
                if not page.is_closed():
                    await page.evaluate("window.scrollTo(0, 0)")
                    await page.screenshot(path="error_automation.png")
                    logger.info("📸 Error screenshot saved as error_automation.png")
                else:
                    logger.warning("Page was already closed; cannot take error screenshot.")
            except TargetClosedError:
                logger.warning("Page was closed while attempting to take error screenshot.")
            except Exception as screenshot_err:
                logger.error(f"Failed to take error screenshot: {screenshot_err}")
        else:
            logger.warning("Page object was not created or is out of scope; cannot take error screenshot.")

    await asyncio.sleep(10)
    date = datetime.datetime.now().strftime('%Y-%m-%d')
    filename = f'adb_events_{date}.json'
    try:
        with open(filename, 'w') as f:
            json.dump(adb_events, f, indent=2)
        logger.info(f"✅ Saved {len(adb_events)} adb_* events to {filename}")
    except Exception as e:
        logger.error(f"Error saving adb events to file: {e}")

if __name__ == "__main__":
    asyncio.run(capture_events_with_actions())

subject = "Adobe event"
body = "Please find the adobe events results below."
sender_email = "cp.harshil@gmail.com"
recipient_emails = ["harshil.shukla@commercepundit.com", "suresh.kadara@commercepundit.com"]
sender_password = "culo jpqg pmtr iafc"
smtp_server = 'smtp.gmail.com'
smtp_port = 465
path_to_file = f'adb_events_{datetime.datetime.now().strftime("%Y-%m-%d")}.json'

try:
    with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
        server.login(sender_email, sender_password)
        
        for recipient in recipient_emails:
            message = MIMEMultipart()
            message['Subject'] = subject
            message['From'] = sender_email
            message['To'] = recipient
            body_part = MIMEText(body)
            message.attach(body_part)
            
            if os.path.exists(path_to_file):
                with open(path_to_file,'rb') as file:
                    message.attach(MIMEApplication(file.read(), Name=os.path.basename(path_to_file)))
            else:
                logger.warning(f"Attachment file not found: {path_to_file}")

            server.sendmail(sender_email, recipient, message.as_string())
            logger.info(f"✅ Email sent successfully to {recipient}!")
            
except smtplib.SMTPAuthenticationError:
    logger.error("❌ Error: Email authentication failed. Please check your username and password or app password settings.")
except smtplib.SMTPException as e:
    logger.error(f"❌ Error sending email via SMTP: {str(e)}")
except Exception as e:
    logger.error(f"❌ Unexpected error during email sending: {str(e)}")