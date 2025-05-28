# This script is about to extract data from the xml in excel file.


import xml.etree.ElementTree as ET
from openpyxl import Workbook

# Load and parse the XML file
tree = ET.parse('C:\\Users\\harshil.shukla\\Desktop\\xmll\\Feeds\\EU.xml')  # Replace with your actual XML file path
root = tree.getroot()

# Create a new Excel workbook and select the active worksheet
wb = Workbook()
ws = wb.active
ws.title = "EU Data"

# Write header row
ws.append(['Link', 'Sale Price'])

# Loop through the XML structure and extract the required tags
for item in root.findall('.//item'):
    link = item.find('link')
    sale_price = item.find('sale_price')

    if link is not None and sale_price is not None:
        sale_price_text = sale_price.text.replace(' EUR', '')  # Remove 'AUD'
        if sale_price_text and sale_price_text.strip():
             ws.append([link.text, float(sale_price_text.replace(',', ''))])
        # ws.append([link.text,float(sale_price_text.replace(',', ''))])

# Save the Excel file
output_path = 'C:\\Users\\harshil.shukla\\Desktop\\xmll\\XML output\\output_EU.xlsx'
wb.save(output_path)

print("Data has been successfully written to Excel:", output_path)
