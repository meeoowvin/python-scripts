import os
import csv
import xml.etree.ElementTree as ET
from datetime import datetime

# Define the directory containing the XML files
directory = 'XML Folder'

# Define the output CSV file
output_file = 'Requests-Date-Data.csv'

# Define the CSV column names
csv_columns = ['Request ID', 'Created Date', 'Completed Date', 'Due by date', 'Responded Date', 'Resolution Time', 'Resolved Time', 'Subject', 'Requester Name', 'Status']

# Open the CSV file for writing
with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
    writer.writeheader()

    # Loop through each XML file in the directory
    for filename in os.listdir(directory):
        if filename.endswith('.xml'):
            print(f'Processing file: {filename}')
            # Parse the XML file
            tree = ET.parse(os.path.join(directory, filename))
            root = tree.getroot()

            # Loop through each ticket in the XML file
            for ticket in root.findall('helpdesk-ticket'):
                # Extract the necessary data
                subject = ticket.find('subject').text
                if not subject:
                    subject = 'Untitled'
                else:
                    subject = subject.replace('<', '(').replace('>', ')')
                if not subject:
                    subject = 'No Subject'
                data = {
                    'Request ID': ticket.find('display-id').text,
                    'Created Date': datetime.strptime(ticket.find('created-at').text, '%Y-%m-%dT%H:%M:%S%z').strftime('%Y-%m-%d %H:%M:%S'),
                    'Completed Date': datetime.strptime(ticket.find('updated-at').text, '%Y-%m-%dT%H:%M:%S%z').strftime('%Y-%m-%d %H:%M:%S'),
                    'Due by date': datetime.strptime(ticket.find('due-by').text, '%Y-%m-%dT%H:%M:%S%z').strftime('%Y-%m-%d %H:%M:%S'),
                    'Responded Date': datetime.strptime(ticket.find('created-at').text, '%Y-%m-%dT%H:%M:%S%z').strftime('%Y-%m-%d %H:%M:%S'),
                    'Resolution Time': datetime.strptime(ticket.find('frDueBy').text, '%Y-%m-%dT%H:%M:%S%z').strftime('%Y-%m-%d %H:%M:%S'),
                    'Resolved Time': datetime.strptime(ticket.find('updated-at').text, '%Y-%m-%dT%H:%M:%S%z').strftime('%Y-%m-%d %H:%M:%S'),
                    'Subject': subject,
                    'Requester Name': ticket.find('requester-name').text,
                    'Status': 'Closed'
                }

                # Write the data to the CSV file
                writer.writerow(data)
            print(f'Finished processing file: {filename}')

print('CSV file generation completed.')