import os
import xml.etree.ElementTree as ET

def find_xml_file_by_display_id(xml_folder, target_display_id):
    # Iterate through each XML file in the specified folder
    for filename in os.listdir(xml_folder):
        if filename.endswith(".xml"):
            xml_path = os.path.join(xml_folder, filename)

            # Parse the XML file
            tree = ET.parse(xml_path)
            root = tree.getroot()

            # Check if the target display-id exists in the current XML file
            for ticket in root.findall('.//helpdesk-ticket'):
                display_id = int(ticket.find('display-id').text)
                if display_id == target_display_id:
                    print(f"Display-ID {target_display_id} found in file: {filename}")
                    return

    print(f"Display-ID {target_display_id} not found in any XML file in {xml_folder}")

# Replace 'XML_Folder' with the actual path to your XML files
xml_folder_path = 'XML_Folder'
target_display_id = 602399  # Replace with the desired display-id to search for
find_xml_file_by_display_id(xml_folder_path, target_display_id)