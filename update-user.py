import csv
import os
import xml.etree.ElementTree as ET

# Set a larger field size limit
csv.field_size_limit(1000000000)

def update_csv(xml_folder, csv_path):
    # Create an empty dictionary to store id-name mappings
    id_name_mapping = {}

    # Loop through all XML files in the specified folder
    for filename in os.listdir(xml_folder):
        if filename.endswith(".xml"):
            xml_path = os.path.join(xml_folder, filename)
            tree = ET.parse(xml_path)
            root = tree.getroot()

            # Update the id-name mapping with data from the current XML file
            id_name_mapping.update({user.find('id').text: user.find('name').text for user in root.findall('.//user')})

    # Update CSV file
    with open(csv_path, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        fieldnames = reader.fieldnames

        # Create a list to store updated rows
        updated_rows = []

        for row in reader:
            sender_id = str(row.get('Sender', '')).split('.')[0]  # Convert to string and remove .0 suffix

            if sender_id in id_name_mapping:
                # Update the 'Sender' column in the CSV with the name from XML
                row['Sender'] = id_name_mapping[sender_id]
                print(f"Updated Sender ID {sender_id} with Name {row['Sender']}")
            else:
                print(f"Sender ID {sender_id} not found in XML")

            updated_rows.append(row)

    # Write the updated rows to a new CSV file
    with open(csv_path, 'w', newline='', encoding='utf-8') as updated_csvfile:
        writer = csv.DictWriter(updated_csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(updated_rows)

    print(f"CSV file '{csv_path}' updated successfully.")

# File
update_csv('Users', 'complete-conversations.csv')