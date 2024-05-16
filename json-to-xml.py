import json
import xml.etree.ElementTree as ET

# Replace 'input.json' with the path to your JSON file
json_path = '2021-complete.json'

# Replace 'output.xml' with the desired output XML file path
output_xml = '2021-complete.xml'

# Read the JSON file
with open(json_path, 'r', encoding='utf-8') as json_file:
    json_data = json.load(json_file)

# Create XML tree
root = ET.Element('data')

# Iterate through the list of dictionaries from the JSON and add data to the XML tree
for item in json_data:
    item_elem = ET.SubElement(root, 'item')
    for key, value in item.items():
        field_elem = ET.SubElement(item_elem, key)
        field_elem.text = str(value)

# Create an ElementTree from the root element
tree = ET.ElementTree(root)

# Write the XML tree to a file
tree.write(output_xml, encoding='utf-8', xml_declaration=True)

print(f'JSON file "{json_path}" has been successfully converted to XML file "{output_xml}".')
