import os
import pandas as pd
import xml.etree.ElementTree as ET
import numpy as np
import csv
import sys
from datetime import datetime
from pandas.io.formats import excel

# Suppress header styling
excel.ExcelFormatter.header_style = None

# Increase the field size limit
maxInt = sys.maxsize
while True:
    try:
        csv.field_size_limit(maxInt)
        break
    except OverflowError:
        maxInt = int(maxInt/10)

def extract_conversations(helpdesk_notes, parent_display_id, subject, requester_name, year, month):
    conversations = []
    for note_elem in helpdesk_notes.findall(".//helpdesk-note"):
        try:
            pre = str(1708850000)
            post = str(note_elem.find('id').text)
            conversation_id = f"{pre}{post}"
            sender = note_elem.find('user-id').text
            body = note_elem.find('body-html').text
            send_time = note_elem.find('created-at').text
            private_value = note_elem.find('private').text.upper()
            is_public = 'FALSE' if private_value == 'TRUE' else 'TRUE'
        except AttributeError:
            sender = send_time = is_public = ''
        conversation_type = np.random.choice(['CONVERSATION', 'REQREPLY'])
        conversation = {
            'ServiceDesk Plus Module': 'Requests',
            'Parent Id': parent_display_id,
            'Conversation Id': conversation_id,
            'Conversation Type': conversation_type,
            'Sender': sender,
            'To Address': requester_name,
            'Cc Address': 'help@ubiquitygs.com',
            'Bcc Address': '',
            'Send Time': send_time,
            'Subject': subject,
            'Description': body,
            'Message Id': '',
            'IsPublic': is_public,
            'Month': month,
            'Year': year
        }
        conversations.append(conversation)
    return conversations

def extract_data_from_xml(xml_file):
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()
    except ET.ParseError as e:
        print(f"Error parsing XML file {xml_file}: {str(e)}")
        return None
    data_list = []
    for ticket_elem in root.findall(".//helpdesk-ticket"):
        parent_display_id = ticket_elem.find('display-id').text
        subject = ticket_elem.find('subject').text
        requester_name = ticket_elem.find('requester-name').text
        date_str = ticket_elem.find('created-at').text
        date_obj = pd.to_datetime(date_str)
        year = date_obj.year
        month = date_obj.strftime('%B')
        helpdesk_notes = ticket_elem.find(".//helpdesk-notes")
        if helpdesk_notes is not None:
            conversations = extract_conversations(helpdesk_notes, parent_display_id, subject, requester_name, year, month)
            data_list.extend(conversations)
    return data_list

def generate_csv(xml_folder, csv_file):
    data_list = []
    for entry in os.scandir(xml_folder):
        if entry.is_file() and entry.name.endswith(".xml"):
            xml_file_path = entry.path
            try:
                ticket_data = extract_data_from_xml(xml_file_path)
                if ticket_data:
                    data_list.extend(ticket_data)
                    print(f"Extracted {len(ticket_data)} tickets from: {xml_file_path}")
            except Exception as e:
                print(f"Error processing file {xml_file_path}: {str(e)}")
    df = pd.DataFrame(data_list)
    df.to_csv(csv_file, index=False, encoding='utf8')
    print(f"CSV file generated: {csv_file}")

def update_csv_with_user_mapping(xml_folder, csv_path):
    id_name_mapping = {}
    for filename in os.listdir(xml_folder):
        if filename.endswith(".xml"):
            xml_path = os.path.join(xml_folder, filename)
            tree = ET.parse(xml_path)
            root = tree.getroot()
            id_name_mapping.update({user.find('id').text: user.find('name').text for user in root.findall('.//user')})
    with open(csv_path, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        fieldnames = reader.fieldnames
        updated_rows = []
        for row in reader:
            sender_id = str(row.get('Sender', '')).split('.')[0]
            if sender_id in id_name_mapping:
                row['Sender'] = id_name_mapping[sender_id]
                print(f"Updated Sender ID {sender_id} with Name {row['Sender']}")
            else:
                print(f"Sender ID {sender_id} not found in XML")
            # Check if all keys in the row exist in fieldnames
            if all(key in fieldnames for key in row.keys()):
                updated_rows.append(row)
    with open(csv_path, 'w', newline='', encoding='utf-8') as updated_csvfile:
        writer = csv.DictWriter(updated_csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(updated_rows)
    print(f"CSV file '{csv_path}' updated successfully.")

def subject_mapping(row):
    subject_row = row['Subject']
    if pd.isna(subject_row) or subject_row == '':
        row['Subject'] = 'Untitled'
    else:
        row['Subject'] = subject_row.replace('<', '(').replace('>', ')')
    if len(row['Subject']) > 250:
        row['Subject'] = row['Subject'][:250]
    return row

def format_datetime_columns(row):
    columns_to_format = ['Send Time']
    for col in columns_to_format:
        if pd.notna(row[col]):
            try:
                datetime_obj = datetime.strptime(str(row[col]), "%d%m/%Y %I:%M")
                formatted_datetime = datetime_obj.strftime("%Y-%m-%d %H:%M:%S")
                row[col] = formatted_datetime
            except ValueError:
                try:
                    datetime_obj = datetime.strptime(str(row[col]), "%d/%m/%Y %H:%M")
                    formatted_datetime = datetime_obj.strftime("%Y-%m-%d %H:%M:%S")
                    row[col] = formatted_datetime
                except ValueError:
                    pass
    return row

def convert_custom_datetime_format(row):
    columns_to_format = ['Send Time']
    for col in columns_to_format:
        try:
            input_datetime = str(row[col])
            parsed_datetime = datetime.strptime(input_datetime, "%Y-%m-%dT%H:%M:%S%z")
            formatted_datetime = parsed_datetime.strftime("%Y-%m-%d %H:%M:%S")
            row[col] = formatted_datetime
        except ValueError:
            pass
    return row

def remove_large_descriptions(df, column='Description', max_length=60000):
    df = df[df[column].str.len() <= max_length]
    return df

def remove_invalid_datetime_rows(df, column='Send Time'):
    valid_datetime_format = "%Y-%m-%d %H:%M:%S"
    mask = pd.to_datetime(df[column], format=valid_datetime_format, errors='coerce').notna()
    df = df.loc[mask]
    return df

def update_csv_with_datetime_format(input_csv):
    df = pd.read_csv(input_csv)
    df = df.apply(subject_mapping, axis=1)
    df = df.apply(format_datetime_columns, axis=1)
    df = df.apply(convert_custom_datetime_format, axis=1)
    df = remove_large_descriptions(df)
    df = remove_invalid_datetime_rows(df)
    df.to_csv(input_csv, index=False, encoding='utf8')
    print(f"CSV file '{input_csv}' updated.")

if __name__ == "__main__":
    xml_folder = "XML_Folder"
    csv_file = "complete-conversations.csv"
    user_xml_folder = 'Users'

    generate_csv(xml_folder, csv_file)
    update_csv_with_user_mapping(user_xml_folder, csv_file)
    update_csv_with_datetime_format(csv_file)

    # Load the final CSV file and print the total number of rows and unique conversation IDs per year
    df = pd.read_csv(csv_file)
    print(f"Total number of rows: {len(df)}")
    print("Number of unique conversation IDs per year:")
    print(df.groupby('Year')['Conversation Id'].nunique())

    print("Script complete.")
