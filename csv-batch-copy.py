import os
import csv
import shutil

def copy_files_to_folders(split_csv_folder, all_attachments_folder):
    # Create the "Attachments" folder if it doesn't exist
    attachments_folder = "Attachments-Copied"
    os.makedirs(attachments_folder, exist_ok=True)

    # Iterate through the split CSVs in the specified folder
    for csv_file_name in os.listdir(split_csv_folder):
        if csv_file_name.endswith(".csv"):
            csv_file_path = os.path.join(split_csv_folder, csv_file_name)

            # Read the CSV and copy files listed in the "File Name" column
            with open(csv_file_path, mode="r", newline="") as csv_file:
                csv_reader = csv.DictReader(csv_file)
                for row in csv_reader:
                    file_name = row["File Name"]

                    # Check if the file exists in the all_attachments_folder
                    source_file_path = os.path.join(all_attachments_folder, file_name)
                    if os.path.exists(source_file_path):
                        # Create a folder for each CSV (use the CSV file name as the folder name)
                        folder_name = os.path.splitext(csv_file_name)[0]
                        folder_path = os.path.join(attachments_folder, folder_name)
                        os.makedirs(folder_path, exist_ok=True)

                        # Copy the file to the folder for this CSV
                        destination_file_path = os.path.join(folder_path, file_name)
                        shutil.copy(source_file_path, destination_file_path)

            # Copy the completed CSV to the root folder of the "Attachments" folder
            shutil.copy(csv_file_path, os.path.join(attachments_folder, csv_file_name))

def main():
    split_csv_folder = "split_csvs"  # Specify the folder containing split CSVs
    all_attachments_folder = "all_downloaded_attachments"  # Specify the folder with all attachments

    copy_files_to_folders(split_csv_folder, all_attachments_folder)

if __name__ == "__main__":
    main()