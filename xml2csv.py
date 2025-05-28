# This script is about to extract data from the xml in csv file.

import xml.etree.ElementTree as ET
import csv

# Load and parse the XML file
tree = ET.parse('C:\\Users\\harshil.shukla\\Downloads\\roi_us.xml')  # Replace with your actual XML file path
root = tree.getroot()

# Open a CSV file to write the data on Desktop
output_path = 'C:\\Users\\harshil.shukla\\Downloads\\output.csv'
with open(output_path, mode='w', newline='', encoding='utf-8') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(['Link', 'Sale Price'])  # Header row

    # Loop through the XML structure and extract the required tags
    for item in root.findall('.//item'):
        link = item.find('link')
        sale_price = item.find('sale_price')

        if link is not None and sale_price is not None:
            sale_price_text = sale_price.text.replace(' EUR', '')  # Remove 'USA' from sale price
            writer.writerow([link.text, sale_price_text])

print("✅ Data has been successfully written to your Desktop as US.csv.")
