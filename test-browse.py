import os
import time
import pyautogui

# Replace this with the actual path to your CSV files directory
csv_directory = r'f:\SD-FS\2014-final'

# Open Firefox and navigate to the data import page
firefox_path = r'C:\Program Files\Mozilla Firefox\firefox.exe'  # Update with your Firefox path
data_import_url = 'https://sdpondemand.manageengine.com/app/itdesk/AdminDetails.cc?forwardTo=dataImport'

# Wait for Firefox to open
time.sleep(1)

# Open Firefox with the provided URL
pyautogui.hotkey('win', 'r')    
pyautogui.write(firefox_path)
pyautogui.press('enter')

# Wait for Firefox to open
time.sleep(1)

# Open a new tab and navigate to the data import page
pyautogui.hotkey('ctrl', 't')
pyautogui.write(data_import_url)
pyautogui.press('enter')

# Wait for the page to load
time.sleep(10)

pyautogui.click(x=795, y=693)
pyautogui.press('r')
pyautogui.press('r')
pyautogui.press('enter')

time.sleep(1)

# Get the list of CSV files in the directory
csv_files = [file for file in os.listdir(csv_directory) if file.endswith('.csv')]

print(f"Total files to upload: {len(csv_files)}")

# Iterate over each CSV file in the directory
for file_index, csv_file in enumerate(csv_files, start=1):
    print(f"\nUploading file {file_index} of {len(csv_files)}: {csv_file}")
    
    # Click the "Browse" button to open the file upload dialog
    pyautogui.click(x=867, y=817)  # Replace with the actual coordinates of the "Browse" button

    # Wait for the file dialog to open
    time.sleep(1)

    # Perform your file selection using PyAutoGUI
    file_path = os.path.join(csv_directory, csv_file)
    pyautogui.write(file_path)
    time.sleep(1)
    pyautogui.press('enter')

    # Wait for the file dialog to close
    time.sleep(1)

    # Click the necessary buttons to proceed (replace with your actual actions)
    pyautogui.click(x=761, y=941)
    time.sleep(25)
    pyautogui.click(x=1017, y=1196)

    # Scroll to the bottom of the page (if needed)
    scroll_distance = 4  # Adjust the number of scrolls as needed
    for _ in range(scroll_distance):
        pyautogui.press('space')

    # Click the necessary buttons to proceed (replace with your actual actions)
    time.sleep(1)
    pyautogui.click(x=1017, y=1196)
    time.sleep(2)
    pyautogui.click(x=942, y=828)
    time.sleep(2)

    # Navigate back to the import page
    pyautogui.hotkey('ctrl', 'l')
    pyautogui.write(data_import_url)
    pyautogui.press('enter')
    
    # Wait for the page to load
    time.sleep(10)

    pyautogui.click(x=795, y=693)
    pyautogui.press('r')
    pyautogui.press('r')
    pyautogui.press('enter')

# Done uploading all files
print(f"\nAll files uploaded successfully. Total files uploaded: {len(csv_files)}")
