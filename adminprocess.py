from playwright.async_api import async_playwright
import asyncio
import logging
import time

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def run():
    async with async_playwright() as p:
        try:
            # Launch browser with context
            browser = await p.chromium.launch(headless=False, channel="chrome", slow_mo=200 ,args=["--start-maximized"])
            context = await browser.new_context(no_viewport=True)
            page = await context.new_page()
            
            # Navigate to login page
            logger.info("Navigating to login page...")
            await page.goto("https://www.coversandall.com/9pkg678a2p9q/admin", wait_until="networkidle")
            
            # Click on the login button and wait for popup
            logger.info("Clicking login button...")
            await page.click("button[type='button']")
            popup = await page.wait_for_event('popup')
            page = popup

            # Wait for and fill email
            logger.info("Filling email...")
            await page.wait_for_selector('#i0116', state='visible', timeout=30000)
            await page.fill('#i0116', 'harshil.shukla@commercepundit.com')
            await page.click('#idSIButton9')
            
            # Wait for and fill password
            logger.info("Filling password...")
            await page.wait_for_selector('#i0118', state='visible', timeout=30000)
            await page.fill('#i0118', 'CPHS@2711#')
            await page.click('#idSIButton9')

            # Handle "Stay signed in?" prompt
            logger.info("Handling stay signed in prompt...")
            await page.wait_for_selector('#idSIButton9', state='visible', timeout=30000)
            await page.click('#idSIButton9')

            # Switch back to main window
            page = context.pages[0]  # Get the first page (main window)

            # Wait for dashboard to load
            logger.info("Waiting for dashboard to load...")
            await page.wait_for_selector('#menu-magento-backend-stores', state='visible', timeout=30000)
            logger.info("Login successful and menu found")

            time.sleep(5)

            # Click on sales menu
            logger.info("Clicking sales menu...")
            await page.click('#menu-magento-sales-sales')
            await page.wait_for_load_state('networkidle')

            #Click on orders
            logger.info('click on orders')
            await page.wait_for_selector("li[data-ui-id='menu-magento-sales-sales-order'] a span", state='visible', timeout=30000)
            await page.click("li[data-ui-id='menu-magento-sales-sales-order'] a span")
            await page.wait_for_load_state('networkidle')

            order_ids = ["COV1016564131"]

            for i in order_ids:
                #click on the keyword search
                logger.info('click on the keyword search')
                await page.wait_for_selector('#fulltext', state='visible',timeout=30000)
                await page.fill('#fulltext', i )
                await page.keyboard.press('Enter')
                await page.wait_for_load_state('networkidle')

                #click on veiw order
                logger.info('click on veiw order')
                await page.wait_for_selector('a.action-menu-item', state='visible',timeout=30000)
                await page.click('a.action-menu-item')
                await page.wait_for_load_state('networkidle')

                #Navigate to the status dropdown.
                logger.info('Navigate to the status dropdown.')
                await page.wait_for_selector('#history_status', state='visible', timeout=30000)
                await page.evaluate('document.querySelector("#history_status").scrollIntoView({behavior: "smooth", block: "center"})')

                # Select status from the dropdown
                await page.wait_for_selector('#history_status', state='visible', timeout=30000)
                await page.click('#history_status')
                await page.keyboard.type('T')
                await page.keyboard.press('Enter')
                logger.info('Selected status by typing T and pressing Enter')
                await page.wait_for_load_state('networkidle')
                
                #Click on the submit button.
                logger.info('Click on the submit button.')
                await page.wait_for_selector('button[title="Submit Comment"]', state='visible', timeout=30000)
                await page.click('button[title="Submit Comment"]')
                await page.wait_for_load_state('networkidle')

                # Click browser back button
                logger.info('Navigating back to orders page...')
                await page.evaluate('window.history.back()')
                await page.wait_for_load_state('networkidle')

            time.sleep(20)
        except Exception as e:
            logger.error(f"An error occurred: {e}")
            if 'page' in locals():
                await page.screenshot(path="error.png")
                logger.info("Error screenshot saved as error.png")
        finally:
            if 'context' in locals():
                await context.close()
            if 'browser' in locals():
                await browser.close()

if __name__ == "__main__":
    asyncio.run(run())
