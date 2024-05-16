import os
import pandas as pd
import xml.etree.ElementTree as ET
from datetime import datetime
from pandas.io.formats import excel

# Suppress header styling
excel.ExcelFormatter.header_style = None

# Function to update the "Description" column in the DataFrame
def update_description(df, xml_folder):
    updated_count = 0
    not_updated_count = 0
    not_updated_ticket_ids = []

    # Print ticket IDs from the CSV file before processing XML files
    print("Ticket IDs from the CSV file:")
    print(df['Ticket Id'].tolist())

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
                    # Check if the ticket ID exists in the DataFrame
                    if int(display_id) in df['Ticket Id'].values:
                        # Check if description length exceeds the cell limit
                        if len(description) > 999999:
                            not_updated_count += 1
                            not_updated_ticket_ids.append(display_id)
                        else:
                            # Update the "Description" column for the corresponding ticket ID
                            df.loc[df['Ticket Id'] == int(display_id), 'Description'] = description
                            updated_count += 1

                            # Print progress indicator
                            print(f"Updated description for Ticket ID: {display_id}")

    print(f"Initial row count: {len(df)}")
    print(f"Updated rows count: {updated_count}")
    print(f"Not updated rows count: {not_updated_count}")
    
    if not_updated_ticket_ids:
        print(f"Ticket IDs not updated due to character limit: {', '.join(not_updated_ticket_ids)}")

    # Remove rows with oversized descriptions
    df = df[~df['Ticket Id'].isin(not_updated_ticket_ids)].reset_index(drop=True)

    return df

# Format date and time columns#
def format_datetime_columns(row):
    columns_to_format = ['Completed Date', 'Created Date', 'Due by date', 'Resolved Time', 'Last Updated Time']
    
    for col in columns_to_format:
        if pd.notna(row[col]):
            try:
                datetime_obj = datetime.strptime(str(row[col]), "%d/%m/%Y %I:%M")
                formatted_datetime = datetime_obj.strftime("%m-%d-%Y %I:%M:%S")
                row[col] = formatted_datetime
            except ValueError:
                try:
                    datetime_obj = datetime.strptime(str(row[col]), "%d/%m/%Y %H:%M")
                    formatted_datetime = datetime_obj.strftime("%m-%d-%Y %H:%M:%S")
                    row[col] = formatted_datetime
                except ValueError:
                    pass  # Handle the case where the value is not in the expected format

    return row

def convert_custom_datetime_format(row):
    columns_to_format = ['Responded Date']

    for col in columns_to_format:
        try:
            # Parse the input datetime string
            input_datetime = str(row[col])
            parsed_datetime = datetime.strptime(input_datetime, "%Y-%m-%dT%H:%M:%S%z")

            # Convert to the desired format
            formatted_datetime = parsed_datetime.strftime("%Y/%m/%d %H:%M:%S")

            row[col] = formatted_datetime
        except ValueError:
            # Handle the case where the input datetime is not in the expected format
            pass  # Do nothing if parsing fails

    return row

if __name__ == "__main__":
    # Specify the path to your clean CSV file and the folder containing XML files
    csv_file = "2021.csv"  # Replace with your clean CSV file path
    xml_folder = "XML_Folder"  # Replace with your folder containing XML files

    # Read the clean CSV file into a DataFrame
    df = pd.read_csv(csv_file)
    df = df.apply(format_datetime_columns, axis=1)

    # Call the function to update the "Description" column
    df = update_description(df, xml_folder)
    
    # Rename specific headers
    df.rename(columns={'Ticket Id': 'Request ID', 'Agent': 'Freshservice Technician', 'Initial Response Time': 'Responded Date', 'Site Affected' : 'Freshservice Site/s Affected', 'Requester Email': 'Email id', 'Sub-Category' : 'Sub Category', 'Source' : 'Mode', 'Client affected' : 'Freshservice Client Affected', 'Closed Time' : 'Completed Date', 'Created Time' : 'Created Date', 'Due by Time': 'Due by date', 'Type' : 'Request Type'}, inplace=True)

    # Save the updated DataFrame back to the CSV file
    df.to_csv(csv_file, index=False)

    print("Description update completed.")
