import os
import csv
import shutil
import uuid  # For generating unique identifiers

def get_file_size(file_path):
    try:
        return os.path.getsize(file_path)
    except OSError:
        return ""

def map_attachments_to_csv(base_directory, csv_file_name, delimiter=","):
    # Create and open the initial CSV file for writing
    with open(csv_file_name, mode="w", newline="") as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=delimiter)
        csv_writer.writerow(["Service Desk", "Parent Id", "Attachment Id", "File Name", "File Size", "Attachment", "Comment"])

        attachment_id = 1  # Initialize Attachment Id
        parent_id = None  # Initialize Parent Id

        # Iterate through subdirectories in the base directory
        for root, _, files in os.walk(base_directory):
            current_parent_id = os.path.basename(root)  # Use the folder name as the parent ID

            # Skip the base directory itself
            if current_parent_id != os.path.basename(base_directory):
                for file_name in files:
                    if not file_name.startswith('.'):  # Skip hidden files
                        file_path = os.path.join(root, file_name)
                        file_size = get_file_size(file_path)  # Get the file size

                        # Check if the parent ID has changed
                        if current_parent_id != parent_id:
                            attachment_id = 1  # Reset Attachment Id for the new parent
                            parent_id = current_parent_id

                        # Handle file name collisions
                        original_file_name = file_name
                        while os.path.exists(os.path.join(root, file_name)):
                            unique_identifier = str(uuid.uuid4())[:8]
                            name, extension = os.path.splitext(original_file_name)
                            file_name = f"{name}_{unique_identifier}{extension}"

                        # Move the file to the correct location with the updated name
                        destination_path = os.path.join(root, file_name)
                        shutil.move(file_path, destination_path)

                        # Write data to CSV with the updated file name
                        csv_writer.writerow(["Requests", parent_id, attachment_id, file_name, file_size, "", ""])
                        attachment_id += 1

def main():
    base_directory = "all_ticket_attachments"  # Specify the base directory containing subdirectories
    csv_file_name = "attachment_data.csv"  # Initial CSV file
    delimiter = ","

    # Map attachments to the initial CSV
    map_attachments_to_csv(base_directory, csv_file_name, delimiter)

if __name__ == "__main__":
    main()
