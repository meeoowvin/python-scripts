import os
import pandas as pd
import xml.etree.ElementTree as ET

# Function to update the "Description" column in the DataFrame
def update_description(df, xml_folder):
    updated_count = 0
    not_updated_count = 0
    not_updated_ticket_ids = []

    # Print Parent Ids from the CSV file before processing XML files
    print("Parent Ids from the CSV file:")
    print(df['Parent Id'].tolist())

    for filename in os.listdir(xml_folder):
        if filename.endswith(".xml"):
            xml_file_path = os.path.join(xml_folder, filename)
            print(f"Processing XML file: {filename}")
            tree = ET.parse(xml_file_path)
            root = tree.getroot()

            for note_elem in root.findall(".//helpdesk-note"):
                try:
                    display_id = note_elem.find('../display-id').text
                    body_html = note_elem.find('body-html').text
                except AttributeError:
                    # Handle missing elements
                    display_id = body_html = ''

                if display_id and body_html:
                    # Check if the Parent Id exists in the DataFrame
                    if int(display_id) in df['Parent Id'].values:
                        # Check if description length exceeds the cell limit
                        if len(body_html) > 99999999:
                            not_updated_count += 1
                            not_updated_ticket_ids.append(display_id)
                        else:
                            # Update the "Description" column for the corresponding Parent Id
                            df.loc[df['Parent Id'] == int(display_id), 'Description'] = body_html
                            updated_count += 1

                            # Print progress indicator
                            print(f"Updated description for Parent Id: {display_id}")

    print(f"Initial row count: {len(df)}")
    print(f"Updated rows count: {updated_count}")
    print(f"Not updated rows count: {not_updated_count}")

    if not_updated_ticket_ids:
        print(f"Parent Ids not updated due to character limit: {', '.join(not_updated_ticket_ids)}")

    # Remove rows with oversized descriptions
    df = df[~df['Parent Id'].isin(not_updated_ticket_ids)].reset_index(drop=True)

    return df

if __name__ == "__main__":
    # Specify the path to your clean CSV file and the folder containing XML files
    csv_file = "output-final.csv"  # Replace with your clean CSV file path
    xml_folder = "testxml"  # Replace with your folder containing XML files

    # Read the clean CSV file into a DataFrame
    df = pd.read_csv(csv_file, encoding='utf-8')

    # Call the function to update the "Description" column
    df = update_description(df, xml_folder)

    # Convert 'Conversation Id' to string type
    df['Conversation Id'] = df['Conversation Id'].astype(str)

    # Save the updated DataFrame back to the CSV file
    df.to_csv(csv_file, index=False)

    print("Description update completed.")
