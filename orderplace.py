from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
from selenium.webdriver.chrome.options import Options


options = Options()
options.add_argument('--headless=new')
options.add_argument('--disable-gpu')
options.add_argument('--window-size=1920,1080')
options.add_argument("--start-maximized")

# Set up the Chrome driver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

wait = WebDriverWait(driver, 20)

# Open the browser and load the home page
home_url = 'https://betauk.alphaprints.in/'
driver.get(home_url)
time.sleep(5)  # Wait for page to load

# Hover on the element
hover_target = wait.until(EC.presence_of_element_located((By.XPATH, "//span[@class='text' and contains(., 'MyAccount')]")))
ActionChains(driver).move_to_element(hover_target).perform()

#: Wait for the button in the pop-up to be clickable, then click it
popup_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@id='login' and contains(@class, 'customer-login-link')]")))
popup_button.click()

# Wait for email field and enter email
email_field = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@id='email-login']")))
email_field.send_keys("harshil.shukla@commercepundit.com")

# Wait for password field and enter password 
password_field = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@id='pass']")))
password_field.send_keys("Test@1234")

# Click the login button
login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='send2-login']")))
login_button.click()

# Wait a moment for login to complete
time.sleep(5)

for order_place_count in range(1,6):

    # List of product URLs to add to cart
    product_urls = [
        'https://betauk.alphaprints.in/tarpaulins-curtains/privacy-screens/custom-mesh-fence-privacy-screen-p#',
        "https://betauk.alphaprints.in/solar-shades/outdoor-roller-shades/classic-outdoor-roller-shade-p",
        "https://betauk.alphaprints.in/fire-column-covers-design-4-p",
        # Add more product URLs here as needed
    ]

    for product_url in product_urls:
        # Open the product page
        driver.get(product_url)
        driver.maximize_window()
        
        try:
            time.sleep(5)
            # Wait for and click the add to cart button
            buttonaddtocart = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="product-addtocart-button"]')))
            buttonaddtocart.click()
            print(f"Added product from {product_url} to cart")
            time.sleep(10)  # Wait between adding items
        except Exception as e:
            print(f"Failed to add product from {product_url}: {str(e)}")

    time.sleep(10)  # Final wait after all items are added

    # Click on the button (assuming the button has an ID 'example-button')
    buttonptc = driver.find_element(By.XPATH, '//*[@id="top-cart-btn-checkout"]')
    buttonptc.click()
    time.sleep(20)
    print("Checkout URL:", driver.current_url)


    # Now click the continue button immediately
    next_btn = driver.find_element(By.XPATH, "//button[@data-role='opc-continue']")
    driver.execute_script("arguments[0].click();", next_btn)

    print("Shipping information filled successfully.")
    time.sleep(30)

    # Wait for the CVC field to be present and clickable
    # Switch to the CVC iframe
    iframe = driver.find_element(By.XPATH, "//iframe[@title='Secure CVC input frame']")
    driver.switch_to.frame(iframe)

    # Use JavaScript to set the CVC value and trigger events
    driver.execute_script("""
        var cvcField = document.getElementsByName('cvc')[0];
        cvcField.value = '552';
        cvcField.dispatchEvent(new Event('input', { bubbles: true }));
        cvcField.dispatchEvent(new Event('change', { bubbles: true }));
        cvcField.dispatchEvent(new Event('blur', { bubbles: true }));
    """)

    # Switch back to default content
    driver.switch_to.default_content()

    # Get and print the current payment page URL
    print("Payment Page URL:", driver.current_url)

    # Add a small wait to ensure the CVC is entered
    time.sleep(5)


    # Click the place order button
    place_order_btn = driver.find_element(By.XPATH, "//*[@id='place-order-trigger']")
    driver.execute_script("arguments[0].click();", place_order_btn)

    # Wait for success page to load (adjust timeout as needed)
    time.sleep(30)

    # Get and print the success page URL
    print("Success Page URL:", driver.current_url)
    time.sleep(10)


    # Close the review dialog
    close_button = driver.find_element(By.XPATH, "//button[@class='close-btn']")
    close_button.click()


    # Get the order ID - typically found in the success message or URL
    try:
        order_id = driver.find_element(By.XPATH, "//a[@class='order-number']//strong").text
        print("Order ID:", order_id)
    except:
        print("Could not locate order ID on page")

    # Write order ID to a separate text file
    try:
        with open('order_id.txt', 'a') as f:
            from datetime import datetime
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"\n{order_id} - {current_time}")
        print("Order ID successfully appended to order_id.txt")
    except Exception as e:
        print(f"Error writing order ID to file: {e}")

    # Add wait to ensure order completion
    time.sleep(10)

# Close the browser
driver.quit()


