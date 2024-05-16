import os
import pandas as pd
import xml.etree.ElementTree as ET

# Function to update the "Description" column in the DataFrame
def update_description(df, xml_folder):
    updated_count = 0
    not_updated_count = 0
    not_updated_ticket_ids = []

    # Print Request IDs from the CSV file before processing XML files
    print("Request IDs from the CSV file:")
    print(df['Request ID'].tolist())

    for filename in os.listdir(xml_folder):
        if filename.endswith(".xml"):
            xml_file_path = os.path.join(xml_folder, filename)
            print(f"Processing XML file: {filename}")
            tree = ET.parse(xml_file_path)
            root = tree.getroot()
            
            for ticket_elem in root.findall("helpdesk-ticket"):
                display_id = ticket_elem.find("display-id").text
                description = ticket_elem.find("description-html").text

                if description is not None:
                    # Check if the Request ID exists in the DataFrame
                    if int(display_id) in df['Request ID'].values:
                        # Check if description length exceeds the cell limit
                        if len(description) > 99999999:
                            not_updated_count += 1
                            not_updated_ticket_ids.append(display_id)
                        else:
                            # Update the "Description" column for the corresponding Request ID
                            df.loc[df['Request ID'] == int(display_id), 'Description'] = description
                            updated_count += 1

                            # Print progress indicator
                            print(f"Updated description for Request ID: {display_id}")

    print(f"Initial row count: {len(df)}")
    print(f"Updated rows count: {updated_count}")
    print(f"Not updated rows count: {not_updated_count}")
    
    if not_updated_ticket_ids:
        print(f"Request IDs not updated due to character limit: {', '.join(not_updated_ticket_ids)}")

    # Remove rows with oversized descriptions
    df = df[~df['Request ID'].isin(not_updated_ticket_ids)].reset_index(drop=True)

    return df

if __name__ == "__main__":
    # Specify the path to your clean CSV file and the folder containing XML files
    csv_file = "2014-complete.csv"  # Replace with your clean CSV file path
    xml_folder = "XML_Folder"  # Replace with your folder containing XML files

    # Read the clean CSV file into a DataFrame
    df = pd.read_csv(csv_file, encoding='utf-8')

    # Call the function to update the "Description" column
    df = update_description(df, xml_folder)

    # Save the updated DataFrame back to the CSV file
    df.to_csv(csv_file, index=False)

    print("Description update completed.")
