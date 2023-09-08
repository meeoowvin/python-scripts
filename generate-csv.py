# -*- coding: utf-8 -*-
"""
Created on Fri Sep  8 22:00:53 2023

@author: mervin.salazar
"""

import os
import csv
import shutil
import uuid  # For generating unique identifiers

def get_file_size(file_path):
    try:
        return os.path.getsize(file_path)
    except OSError:
        return ""

def map_attachments_to_csv(base_directory, csv_file_name):
    # Create and open the CSV file for writing
    with open(csv_file_name, mode="w", newline="") as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=",")
        csv_writer.writerow(["Service Desk", "Parent Id", "Attachment Id", "File Name", "File Size", "Attachment", "Comment"])

        attachment_id = 1  # Initialize Attachment Id

        # Iterate through subdirectories in the base directory
        for root, _, files in os.walk(base_directory):
            parent_id = os.path.basename(root)  # Use the folder name as the parent ID

            # Skip the base directory itself
            if parent_id != os.path.basename(base_directory):
                for file_name in files:
                    if not file_name.startswith('.'):  # Skip hidden files
                        file_path = os.path.join(root, file_name)
                        file_size = get_file_size(file_path)  # Get the file size

                        # Write data to CSV
                        csv_writer.writerow(["Requests", parent_id, attachment_id, file_name, file_size, "", ""])
                        attachment_id += 1

def move_downloaded_attachments(base_directory, destination_directory, csv_file_name):
    # Create the destination directory if it doesn't exist
    os.makedirs(destination_directory, exist_ok=True)

    attachment_id_mapping = {}  # Dictionary to store original attachment IDs and their corresponding new names

    # Create and open the updated CSV file for writing
    with open(csv_file_name, mode="w", newline="") as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=",")
        csv_writer.writerow(["Service Desk", "Parent Id", "Attachment Id", "File Name", "File Size", "Attachment", "Comment"])

        attachment_id = 1  # Initialize Attachment Id

        # Iterate through subdirectories in the base directory
        for root, _, files in os.walk(base_directory):
            parent_id = os.path.basename(root)  # Use the folder name as the parent ID

            # Skip the base directory itself
            if parent_id != os.path.basename(base_directory):
                for file_name in files:
                    if not file_name.startswith('.'):  # Skip hidden files
                        file_path = os.path.join(root, file_name)
                        new_file_name = file_name

                        # Handle file name collisions
                        while os.path.exists(os.path.join(destination_directory, new_file_name)):
                            unique_identifier = str(uuid.uuid4())[:8]
                            new_file_name = f"{unique_identifier}_{file_name}"

                        destination_path = os.path.join(destination_directory, new_file_name)
                        # Move the file to the destination directory
                        shutil.move(file_path, destination_path)
                        # Store the original attachment ID and new name in the mapping
                        attachment_id_mapping[file_name] = new_file_name

                        # Write data to updated CSV
                        file_size = get_file_size(destination_path)  # Get the file size of the renamed file
                        csv_writer.writerow(["Requests", parent_id, attachment_id, new_file_name, file_size, "", ""])
                        attachment_id += 1

    return attachment_id_mapping

def gen_csv_marvin():
    base_directory = "all_ticket_attachments"  # Specify the base directory containing subdirectories
    destination_directory = "all_downloaded_attachments"  # Specify the destination directory
    csv_file_name = "attachment_data_all.csv"

    # Map attachments to the CSV
    map_attachments_to_csv(base_directory, csv_file_name)

    # Move the downloaded attachments and handle file name collisions, updating the CSV
    attachment_id_mapping = move_downloaded_attachments(base_directory, destination_directory, csv_file_name)

if __name__ == "__main__":
    gen_csv_marvin()
