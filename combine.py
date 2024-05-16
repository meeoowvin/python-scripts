import os
import pandas as pd
import xml.etree.ElementTree as ET

# Function to update the "Description" in the CSV file
def update_csv_description(df, xml_folder):
    for filename in os.listdir(xml_folder):
        if filename.endswith(".xml"):
            xml_file_path = os.path.join(xml_folder, filename)
            print(f"Processing XML file: {filename}")

            tree = ET.parse(xml_file_path)
            root = tree.getroot()

            for ticket_elem in root.findall("helpdesk-ticket"):
                display_id = int(ticket_elem.find("display-id").text)

                # Check if the ticket ID exists in the DataFrame
                if display_id in df['Ticket Id'].values:
                    # Update the "Description" column with data from the XML
                    description = ticket_elem.find("description-html").text
                    df.loc[df['Ticket Id'] == display_id, 'Description'] = description

                    # Print details of the updated ticket
                    print(f"Updated Ticket ID: {display_id}")
                    print(f"Updated Description: {description}")

    return df

# Function to convert the CSV data into an XML file
def convert_csv_to_xml(df, output_xml_file):
    combined_root = ET.Element("helpdesk-tickets")

    for _, row in df.iterrows():
        combined_ticket_elem = ET.Element("helpdesk-ticket")

        # Add attributes from the CSV
        for col in df.columns:
            combined_ticket_elem.set(col, str(row[col]))

        # Add the "description-html" element
        description_elem = ET.Element("description-html")
        description_elem.text = str(row['Description'])
        combined_ticket_elem.append(description_elem)

        combined_root.append(combined_ticket_elem)

    combined_tree = ET.ElementTree(combined_root)
    combined_tree.write(output_xml_file)

if __name__ == "__main__":
    # Specify the paths for your CSV file, XML folder, and the output XML file
    csv_file = "2021.csv"  # Replace with your CSV file path
    xml_folder = "XML_Folder"  # Replace with your folder containing XML files
    output_xml_file = "2021-complete.xml"  # Replace with your desired output XML file path

    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_file)

    # Call the function to update the CSV file with descriptions from XML
    df = update_csv_description(df, xml_folder)

    # Save the updated DataFrame back to the CSV file
    df.to_csv(csv_file, index=False)

    # Call the function to convert the updated CSV data into an XML file
    convert_csv_to_xml(df, output_xml_file)

    print(f"Updated CSV file and combined data saved to {output_xml_file}")
