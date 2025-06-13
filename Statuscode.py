from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import json
import csv
import time

# Setup Chrome options
options = Options()

options.add_argument('--disable-gpu')
options.add_argument('--headless=new')
options.add_argument('--window-size=1920,1080')
options.add_argument("--start-maximized")
options.add_argument("--auto-open-devtools-for-tabs")  # Optional: opens DevTools
options.set_capability("goog:loggingPrefs", {"performance": "ALL"})



# Start the driver
driver = webdriver.Chrome(options=options)

# Enable Network tracking via CDP
driver.execute_cdp_cmd("Network.enable", {})


# Open CSV file for appending (to continue where left off)
with open('network_responses.csv', 'a', newline='') as csvfile:
    fieldnames = ['URL', 'Status','Product URL' , 'Status Text', 'Iteration']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    # Write header only if file is empty
    if csvfile.tell() == 0:
        writer.writeheader()

    # List of URL patterns to include
    include_patterns = [
        'https://www.coversandall.com/product/cart/addajax/',
    ]

    # Read URLs from CSV
    with open('C:\\Users\\harshil.shukla\\Downloads\\other.csv', 'r') as url_file:
        url_reader = csv.DictReader(url_file)
        urls = [row['Link'] for row in url_reader]
    
    # Find last processed URL if any
    try:
        with open('network_responses.csv', 'r') as check_file:
            last_line = list(csv.DictReader(check_file))[-1]
            last_url = last_line['Product URL']
            start_index = urls.index(last_url) + 1
    except (FileNotFoundError, IndexError, ValueError):
        start_index = 0
    
    i = start_index + 1
    for url in urls[start_index:]:
        print(f"\nStarting iteration {i} of {len(urls)} - Testing URL: {url}")
        
        try:
            # Load the URL
            driver.get(url)
            time.sleep(8)


            try:
                # Try multiple XPaths for finding the input field
                xpaths = [
                    "//input[@type='number' and @placeholder='Inches']",
                    "//span[text()='Feet']",
                    
                ]
                     
                for xpath in xpaths:
                    try:
                        input_field = driver.find_element(By.XPATH, xpath)
                        input_field.clear()
                        input_field.send_keys('10.35')
                        print(f"Iteration {i}: Updated dimensions using XPath: {xpath}")
                        break
                    except:
                        continue
                
                if not input_field:
                    raise Exception("Could not find dimension input field with any XPath")
            except Exception as e:
                print(f"Iteration {i}: Failed to update dimension - {str(e)}")
                continue

            # Add to cart button click
            try:
                buttonaddtocart = driver.find_element(By.XPATH, '//*[@id="product-addtocart-button"]')
                buttonaddtocart.click()
                print(f"Iteration {i}: Added product to cart")
            except Exception as e:
                print(f"Iteration {i}: Failed to add to cart - {str(e)}")
                continue

            time.sleep(5)

            # Get performance logs
            logs = driver.get_log("performance")

            for entry in logs:
                log = json.loads(entry["message"])["message"]
                if log["method"] == "Network.responseReceived":
                    response = log["params"]["response"]
                    current_url = response['url']
                    
                    if any(pattern in current_url for pattern in include_patterns):
                        writer.writerow({
                            'URL': current_url,
                            'Status': response['status'],
                            'Product URL' : url,
                            'Status Text': response['statusText'],
                            'Iteration': i
                        })            
        except Exception as e:
            print(f"Error processing URL {url}: {str(e)}")
            continue
        i += 1
    
    driver.quit()
