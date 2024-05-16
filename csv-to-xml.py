import csv
import xml.etree.ElementTree as ET

# Set a larger field size limit
csv.field_size_limit(1000000)

# Replace 'input.csv' with the path to your CSV file
csv_path = '2021.csv'

# Replace 'output.xml' with the desired output XML file path
output_xml = '2021-complete.xml'

# Read the CSV file into a list of dictionaries
csv_data = []
with open(csv_path, mode='r', newline='', encoding='utf-8') as csvfile:
    csv_reader = csv.DictReader(csvfile)
    for row in csv_reader:
        csv_data.append(row)

# Create XML tree
root = ET.Element('data')

# Iterate through the list of dictionaries and add data to the XML tree
for item in csv_data:
    item_elem = ET.SubElement(root, 'item')
    for key, value in item.items():
        field_elem = ET.SubElement(item_elem, key)
        field_elem.text = value

# Create an ElementTree from the root element
tree = ET.ElementTree(root)

# Write the XML tree to a file
tree.write(output_xml, encoding='utf-8', xml_declaration=True)

print(f'CSV file "{csv_path}" has been successfully converted to XML file "{output_xml}".')
