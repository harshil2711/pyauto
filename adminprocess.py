from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
import time

# Navigate to the website
# Initialize Chrome with options
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=options)

# Navigate to page with explicit wait for page load
driver.get("https://www.coversandall.com/9pkg678a2p9q/admin/")


# Wait for and click login button with explicit wait
login_button = driver.find_element(By.CSS_SELECTOR, "button[type='button']")
login_button.click()

time.sleep(10)

# Switch to the new window
windows = driver.window_handles
driver.switch_to.window(windows[1])

# Wait for email field and enter email
email_field = driver.find_element(By.XPATH, "//input[@id='i0116']")
email_field.send_keys("harshil.shukla@commercepundit.com")
time.sleep(3)

# Wait for and click next button
next_button = driver.find_element(By.XPATH, "//input[@id='idSIButton9']")
next_button.click()
time.sleep(3)

# Wait for password field and enter password
password_field = driver.find_element(By.XPATH, "//input[@id='i0118']")
password_field.send_keys("CPHS@2711#")

# Click the submit button
submit_button = driver.find_element(By.XPATH, "//input[@id='idSIButton9']")
submit_button.click()
time.sleep(3)

# Click on confirm button
click_on_confirm = driver.find_element(By.XPATH, "//input[@id='idSIButton9']")
click_on_confirm.click()
time.sleep(50)

#click on sales button
sales_button = driver.find_element(By.CSS_SELECTOR, 'li#menu-magento-sales-sales > a')
sales_button.click()





# Wait for login to complete before closing

driver.quit()  # Use quit() instead of close() to properly terminate session

