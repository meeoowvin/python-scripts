import os
import zipfile

def zip_folders_in_attachments(attachments_folder):
    # Iterate through subdirectories in the "Attachments" folder
    for root, _, folders in os.walk(attachments_folder):
        # Skip the root folder itself
        if root != attachments_folder:
            # Create a zip file with the same name as the folder
            folder_name = os.path.basename(root)
            zip_file_path = os.path.join(attachments_folder, f"{folder_name}.zip")

            # Create a zip file and add all files in the folder to it
            with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for folder_root, _, files in os.walk(root):
                    for file in files:
                        file_path = os.path.join(folder_root, file)
                        arcname = os.path.relpath(file_path, root)  # Use relative path in the zip
                        zipf.write(file_path, arcname)
            print(f"Successfully zipped {os.path.basename(zip_file_path)}")

def zipmarvin():
    attachments_folder = "Attachments-Copied"  # Specify the "Attachments" folder

    zip_folders_in_attachments(attachments_folder)

if __name__ == "__main__":
    zipmarvin()
