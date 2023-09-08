# -*- coding: utf-8 -*-
"""
Created on Wed Sep  6 22:44:58 2023

@author: Marvin John Salazar
"""

import os
import xml.etree.ElementTree as ET
import requests
from time import sleep
import shutil

def sanitize_filename(filename):
    # Replace special characters with underscores
    return "".join([c if c.isalnum() or c in ['.', '_', '-'] else '_' for c in filename])

def process_attachment(attachment_elem, folder_path, display_id, is_note=False):
    # Define basic auth credentials
    username = "lxt4UQcWPeyt4SZ9l7"
    password = "x"
 
    # Define the API endpoint for downloading attachments
    attachment_base_url = "https://ubiquitygs.freshservice.com/api/v2/attachments"
 
    contennt_file_id = attachment_elem.find("id").text
    content_file_name = attachment_elem.find("content-file-name").text
 
    if is_note:
        content_file_name = f"note_{content_file_name}"
 
    # append attachment id to API endpoint
    attachemt_url = f"{attachment_base_url}/{contennt_file_id}"
 
    # Download and save the attachment file using API request
    attachment_response = requests.get(attachemt_url, auth=(username, password))
    content_file_name = sanitize_filename(content_file_name)  # Sanitize the filename
    attachment_file_path = os.path.join(folder_path, display_id, content_file_name)
 
    # Ensure the subfolder exists before saving the attachment
    os.makedirs(os.path.dirname(attachment_file_path), exist_ok=True)
 
    with open(attachment_file_path, "wb") as attachment_file:
        attachment_file.write(attachment_response.content)
 
    return content_file_name
 
def process_xml_file(xml_file_path, base_directory):
    # Read XML content from file
    with open(xml_file_path, "r", encoding="utf8") as xml_file:
        xml_content = xml_file.read()
 
    root = ET.fromstring(xml_content)
    xml_file_name = os.path.basename(xml_file_path)
    file_name = os.path.splitext(xml_file_name)[0]  # Get the file name without extension
 
    # Create a directory for the XML file if it doesn't exist
    file_directory = os.path.join(base_directory, file_name)
    os.makedirs(file_directory, exist_ok=True)
 
    # Iterate through each 'helpdesk-ticket' element
    for idx, ticket_elem in enumerate(root.findall("helpdesk-ticket")):
        counter = idx + 1
        display_id = ticket_elem.find("display-id").text
 
        attachments = []
        attachment_elems = ticket_elem.find("attachments")
        notes_elems = ticket_elem.find("helpdesk-notes")
 
        attachment_count = 0
        note_attachment_count = 0
        if attachment_elems is not None:
            attachment_count = len(attachment_elems)
 
        if notes_elems is not None:
            note_attachment_count = len(notes_elems)
 
        if attachment_count > 0 and note_attachment_count > 0:
            if attachment_elems is not None:
                for attachment_elem in attachment_elems.findall("attachment"):
                    content_file_name = process_attachment(attachment_elem, file_directory, display_id)
                    attachments.append(content_file_name)
 
            if notes_elems is not None:
                for note_elem in notes_elems.findall("helpdesk-note"):
                    note_attachment_elems = note_elem.find("attachments")
                    if note_attachment_elems is not None:
                        for note_attachment_elem in note_attachment_elems.findall("attachment"):
                            content_file_name = process_attachment(note_attachment_elem, file_directory, display_id, is_note=True)
                            attachments.append(content_file_name)
 
        print(f"{counter} - {file_name} - Ticket ID {display_id}: {attachments}")
        sleep(.2)
        
    # Move the processed XML files to the "processed_xmls" folder
    processed_folder = "processed_xmls"
    os.makedirs(processed_folder, exist_ok=True)
    shutil.move(xml_file_path, os.path.join(processed_folder, xml_file_name))
 
def main():
    folder_path = "."  # Specify the path to the folder containing XML files
    base_directory = "all_ticket_attachments"  # Specify the base directory for storing attachments
 
    # Create the base directory if it doesn't exist
    os.makedirs(base_directory, exist_ok=True)
 
    # Iterate through XML files in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith(".xml"):
            xml_file_path = os.path.join(folder_path, filename)
            process_xml_file(xml_file_path, base_directory)
 
if __name__ == "__main__":
    main()
