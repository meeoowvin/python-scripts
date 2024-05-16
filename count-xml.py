import os
import xml.etree.ElementTree as ET
from collections import defaultdict

def count_display_ids_by_year(xml_folder):
    display_ids_by_year = defaultdict(set)
    total_display_ids = set()

    # Iterate through each XML file in the specified folder
    for filename in os.listdir(xml_folder):
        if filename.endswith(".xml"):
            xml_path = os.path.join(xml_folder, filename)

            print(f"Processing file: {filename}")

            # Parse the XML file
            tree = ET.parse(xml_path)
            root = tree.getroot()

            # Extract and add display-id values to the set based on their year of creation
            for ticket in root.findall('.helpdesk-ticket'):
                display_id = int(ticket.find('display-id').text)
                created_at = ticket.find('created-at').text
                year = created_at.split('-')[0]  # Extract the year from the 'created-at' value
                display_ids_by_year[year].add(display_id)

                # Add display-id to the total set
                total_display_ids.add(display_id)

    # Print the count of display-ids for each year
    for year, display_ids in display_ids_by_year.items():
        print(f"Year: {year}, Ticket Count: {len(display_ids)}")

    # Print the total count of display-ids across all years
    print(f"Total Ticket Count across all years: {len(total_display_ids)}")

# Replace 'XML_Folder' with the actual path to your XML files
xml_folder_path = 'XML_Folder'
count_display_ids_by_year(xml_folder_path)