import os
import pandas as pd
import xml.etree.ElementTree as ET

# Function to update the "Client Affected" and "Site Affected" columns in the DataFrame
def update_custom_fields(df, xml_folder):
    updated_count = 0
    not_updated_count = 0
    not_updated_ticket_ids = []

    for filename in os.listdir(xml_folder):
        if filename.endswith(".xml"):
            xml_file_path = os.path.join(xml_folder, filename)
            tree = ET.parse(xml_file_path)
            root = tree.getroot()
            
            for ticket_elem in root.findall("helpdesk-ticket"):
                display_id = ticket_elem.find("display-id").text

                # Find the "client_affected_133428" and "site_affected_133428" values within custom_fields
                custom_fields = ticket_elem.findall("custom_field")
                client_affected = None
                site_affected = None

                for custom_field in custom_fields:
                    if custom_field.find("client_affected_133428") is not None:
                        client_affected = custom_field.find("client_affected_133428").text
                    if custom_field.find("sites_affected_133428") is not None:
                        site_affected = custom_field.find("sites_affected_133428").text

                # Check if the ticket ID exists in the DataFrame
                if int(display_id) in df['Ticket Id'].values:
                    # Update the "Client Affected" and "Site Affected" columns for the corresponding ticket ID
                    df.loc[df['Ticket Id'] == int(display_id), 'Client affected'] = client_affected
                    df.loc[df['Ticket Id'] == int(display_id), 'Site Affected'] = site_affected
                    updated_count += 1

                    # Print progress indicator
                    print(f"Updated Client Affected and Site Affected for Ticket ID: {display_id}")
                else:
                    not_updated_count += 1
                    not_updated_ticket_ids.append(display_id)

    print(f"Initial row count: {len(df)}")
    print(f"Updated rows count: {updated_count}")
    print(f"Not updated rows count: {not_updated_count}")
    if not_updated_ticket_ids:
        print(f"Ticket IDs not updated due to missing data: {', '.join(not_updated_ticket_ids)}")

    return df

if __name__ == "__main__":
    # Specify the path to your clean CSV file and the folder containing XML files
    csv_file = "test.csv"  # Replace with your clean CSV file path
    xml_folder = "testxml"  # Replace with your folder containing XML files

    # Read the clean CSV file into a DataFrame
    df = pd.read_csv(csv_file)

    # Add "Client Affected" and "Site Affected" columns to the DataFrame
    df['Client affected'] = ""
    df['Site Affected'] = ""

    # Call the function to update the "Client Affected" and "Site Affected" columns
    df = update_custom_fields(df, xml_folder)

    # Save the updated DataFrame back to the CSV file
    df.to_csv(csv_file, index=False)

    print("Custom Fields update completed.")
