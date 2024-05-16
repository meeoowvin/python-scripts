import os
import time
import subprocess
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select

# Set the path to the directory containing your CSV files
files_directory = '2012-final'

# Check if the CSV directory exists
if not os.path.exists(files_directory):
    print(f"Directory '{files_directory}' does not exist.")
    exit()

# List all CSV files to upload
csv_files = [filename for filename in os.listdir(files_directory) if filename.endswith('.csv')]

# Display the total count of files to upload
total_files = len(csv_files)
print(f"Total files to upload: {total_files}")

# Initialize the Firefox WebDriver with the specified options
firefox_options = webdriver.FirefoxOptions()
firefox_options.add_argument('-profile')
firefox_options.add_argument(r'C:\Users\mjsal\AppData\Roaming\Mozilla\Firefox\Profiles\95dn06is.default-release-1701701215116')  # Specify your profile directory

# Initialize the Firefox WebDriver
driver = webdriver.Firefox(options=firefox_options)

# 1. Go to the data import page
driver.get('https://sdpondemand.manageengine.com/app/itdesk/AdminDetails.cc?forwardTo=dataImport')

# AutoIt script path
autoit_script_path = r'F:\SD-FS\upload_script.au3'

# Iterate through each file in the directory
for file_index, filename in enumerate(csv_files, start=1):
    print(f"\nUploading file {file_index} of {total_files}: {filename}")
    file_path = os.path.join(files_directory, filename)

    # 2. Select "Request" from the module dropdown
    try:
        module_dropdown = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'module'))
        )
        # Use Select class to handle dropdown
        module_select = Select(module_dropdown)
        module_select.select_by_value('Requests')
    except TimeoutException:
        print("Module dropdown not found within the specified time.")
        break

    # Select "Request" option directly without using XPATH
    request_option = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'select#module option[value="Request"]'))
    )
    request_option.click()

    # 3. Locate the file input element and open the file selection dialog
    try:
        file_input_element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'theFile'))
        )
        file_input_element.click()
    
        # Wait for the file dialog to open
        time.sleep(1)
    
        # Run the AutoIt script to handle the file upload dialog
        autoit_script_path = r'C:\Program Files (x86)\AutoIt3\AutoIt3.exe'  # Update with your AutoIt script path
        subprocess.run([autoit_script_path], shell=True)
    except Exception as e:
        print(f"Error uploading file '{filename}': {e}")
        continue

    # 4. Click "Next" button
    next_button_1 = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, 'nextId'))
    )
    next_button_1.click()

    # 5. Click "Next" button on the second page
    next_button_2 = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//button[contains(text(),"Next") and @class="active-button formstylebutton"]'))
    )
    next_button_2.click()

    # 6. Click "Import Now" button on the final page
    import_now_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//button[@id="importbutton" and contains(text(),"Import Now") and @class="active-button formstylebutton button active"]'))
    )
    import_now_button.click()

    # Introduce a 3-second sleep before uploading the next file
    time.sleep(3)

    print(f"File '{filename}' uploaded successfully.")

# Display the list of files that have been uploaded
print("\nFiles uploaded:")
for filename in csv_files:
    print(filename)

# Close the browser
driver.quit()
