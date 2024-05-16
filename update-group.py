import csv
import xml.etree.ElementTree as ET

def update_csv(xml_path, csv_path):
    # Parse XML file
    tree = ET.parse(xml_path)
    root = tree.getroot()

    # Create a dictionary to store id-name mapping
    id_name_mapping = {group.find('id').text: group.find('name').text for group in root.findall('.//group')}

    # Update CSV file
    with open(csv_path, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        fieldnames = reader.fieldnames

        # Create a list to store updated rows
        updated_rows = []

        for row in reader:
            group_id = str(row.get('Group', '')).split('.')[0]  # Convert to string and remove .0 suffix

            if group_id in id_name_mapping:
                # Update the 'Group' column in the CSV with the name from XML
                row['Group'] = id_name_mapping[group_id]
                print(f"Updated Group ID {group_id} with Name {row['Group']}")
            else:
                print(f"Group ID {group_id} not found in XML")

            updated_rows.append(row)

    # Write the updated rows to a new CSV file
    with open(csv_path, 'w', newline='', encoding='utf-8') as updated_csvfile:
        writer = csv.DictWriter(updated_csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(updated_rows)

    print(f"CSV file '{csv_path}' updated successfully.")

# Example usage
update_csv('Groups/Groups.xml', '2014-complete.csv')