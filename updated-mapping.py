import pandas as pd
import os
from datetime import datetime
from pandas.io.formats import excel

# Suppress header styling
excel.ExcelFormatter.header_style = None

# Handle mappings for "Department"
def department_mappings(row):
    department = row['Department']
    if department == 'Admin and Facilities':
        row['Department'] = 'Places'
    elif department == 'Human Resources':
        row['Department'] = 'People'
    elif department == 'USyM':
        row['Department'] = 'Technology'
    elif department == 'Workforce':
        row['Department'] = 'Workforce/RTA'
        
    return row

# Handle mappings for "Impact"
def impact_mappings(row):
    impact = row['Impact']
    if impact == 'High':
        row['Impact'] = '4 - Affects Department'
    elif impact == 'Medium':
        row['Impact'] = '5 - Affects Group'
    elif impact == 'Low':
        row['Impact'] = '6 - Affects User'
        
    return row

# Handle mappings for "Priority"
def priority_mappings(row):
    priority = row['Priority']
    if priority == 'Urgent':
        row['Priority'] = 'P1 Critical'
    elif priority == 'High':
        row['Priority'] = 'P2 High'
    elif priority == 'Medium':
        row['Priority'] = 'P3 Medium'
    elif priority == 'Low':
        row['Priority'] = 'P4 Low'
        
    return row

# Handle mappings for "Source"
def source_mappings(row):
    source = row['Source']
    if source == 'Email':
        row['Source'] = 'E-Mail'
    elif source == 'Phone':
        row['Source'] = 'Phone Call'
    elif source == 'Portal':
        row['Source'] = 'Web Form'
        
    return row

# Handle mappings for "Urgency"
def urgency_mappings(row):
    urgency = row['Urgency']
    if urgency == 'High':
        row['Urgency'] = '2 - High'
    elif urgency == 'Medium':
        row['Urgency'] = '3 - Medium'
    elif urgency == 'Low':
        row['Urgency'] = '4 - Low'
        
    return row

# Handle mappings for "Groups"
def groups_mappings(row):
    group = row['Group']
    if group == 'Application Support':
        row['Group'] = 'Application Support (AppSup)'
    elif group == 'Development':
        row['Group'] = 'Research and Development (R&D)'
    elif group == 'Digital Service':
        row['Group'] = 'Digital Services Team (DST)'
    elif group == 'IAM':
        row['Group'] = 'Identity Access Management (IAM)'
    elif group == 'Information Security':
        row['Group'] = 'Information Security (InfoSec)'
    elif group == 'Noc / T2':
        row['Group'] = 'Network Operations Center (NOC)'
    elif group == 'Outage Response':
        row['Group'] = 'Outage Response Coordination (ORC)'
    elif group == 'Procurement':
        row['Group'] = 'IT Procurement (ITPROC)'
    elif group == 'Service Desk':
        row['Group'] = 'Service Desk Team (SDT)'
    elif group == 'Systems Engineering':
        row['Group'] = 'System Engineering (SysEng)'
    elif group == 'TELCO':
        row['Group'] = 'Telecom Engineering (TelcoEng)'
        
    return row

# Handle mappings for "Site Affected" / "Group"
def group_mappings(row):
    site_affected = row['Site Affected']
    group = row['Group']
    if site_affected == 'Bacolod':
        row['Site Affected'] = '["BCD Cyber Centre"]'
        if group == 'Field Support':
            row['Group'] = 'End User Support (EUS-BCD-CYBER)'
    elif site_affected == 'Budapest':
        row['Site Affected'] = '["BUD Váci út"]'
        if group == 'Field Support':
            row['Group'] = 'End User Support (EUS-BUD)'
    elif site_affected == 'CA Datacenter':
        row['Site Affected'] = '["CA Gillette AVE"]'
        if group == 'Field Support':
            row['Group'] = 'End User Support (EUS-AMERICAS)'
    elif site_affected == 'Cagayan de Oro':
        row['Site Affected'] = '["CDO Limketkai BPO Bldg"]'
        if group == 'Field Support':
            row['Group'] = 'End User Support (EUS-CDO)'
    elif site_affected == 'Colombia':
        row['Site Affected'] = '["BOG CCI Building"]'
        if group == 'Field Support':
            row['Group'] = 'End User Support (EUS-COL)'
    elif site_affected == 'El Salvador':
        row['Site Affected'] = '["SAL Salvador"]'
        if group == 'Field Support':
            row['Group'] = 'End User Support (EUS-ELSAL)'
    elif site_affected == 'India':
        row['Site Affected'] = '["IND - 101-A 1st Floor,D-Mall Netaji Subash Palace"]'
        if group == 'Field Support':
            row['Group'] = 'End User Support (EUS-IND)'
    elif site_affected == 'Laguna':
        row['Site Affected'] = '["LGN Southwoods Mall"]'
        if group == 'Field Support':
            row['Group'] = 'End User Support (EUS-SW)'
    elif site_affected == 'Manila':
        row['Site Affected'] = '["MNL Bench Tower"]'
        if group == 'Field Support':
            row['Group'] = 'End User Support (EUS-BENCH)'
    elif site_affected == 'Manilan':
        row['Site Affected'] = '["MNL Bench Tower"]'
        if group == 'Field Support':
            row['Group'] = 'End User Support (EUS-BENCH)'
    elif site_affected == 'New York':
        row['Site Affected'] = '["NYC Avenue of the Americas"]'
        if group == 'Field Support':
            row['Group'] = 'End User Support (EUS-AMERICAS)'
    elif site_affected == 'Wilkes-Barre':
        row['Site Affected'] = '["NYC Avenue of the Americas"]'
        if group == 'Field Support':
            row['Group'] = 'End User Support (EUS-AMERICAS)'
    elif site_affected == 'NJ Datacenter':
        row['Site Affected'] = '["NJ 300 boulevard East"]'
        if group == 'Field Support':
            row['Group'] = 'End User Support (EUS-AMERICAS)'
    elif site_affected == 'Omaha':
        row['Site Affected'] = '["OMH 81st Street"]'
        if group == 'Field Support':
            row['Group'] = 'End User Support (EUS-OMH)'
    elif site_affected == 'Other':
        row['Site Affected'] = '["WAH Work At Home"]'
        if group == 'Field Support':
            row['Group'] = 'Digital Services Team (DST)'
    elif site_affected == 'Tulsa':
        row['Site Affected'] = '["TUL 2488 E. 81 st Street, Suite 1700"]'
        if group == 'Field Support':
            row['Group'] = 'End User Support (EUS-TUL)'
    elif site_affected == 'USA':
        row['Site Affected'] = '["NYC Avenue of the Americas"]'
        if group == 'Field Support':
            row['Group'] = 'End User Support (EUS-AMERICAS)'
    elif site_affected == 'Global':
        row['Site Affected'] = '["MNL Bench Tower"]'
        if group == 'Field Support':
            row['Group'] = 'End User Support (EUS-BENCH)'
    elif site_affected == 'Global ':
        row['Site Affected'] = '["MNL Bench Tower"]'
        if group == 'Field Support':
            row['Group'] = 'End User Support (EUS-BENCH)'
    elif site_affected == 'Philippines (Manila & Bacolod)':
        row['Site Affected'] = '["BCD Cyber Centre"]'
        if group == 'Field Support':
            row['Group'] = 'End User Support (EUS-BCD-CYBER)'
    elif site_affected == 'Bac Support':
        row['Site Affected'] = '["BCD Cyber Centre"]'
        if group == 'Field Support':
            row['Group'] = 'End User Support (EUS-BCD-CYBER)'
    elif site_affected == 'NJ-Datacenter':
        row['Site Affected'] = '["NJ 300 boulevard East"]'
        if group == 'Field Support':
            row['Group'] = 'End User Support (EUS-AMERICAS)'
            
    return row
 
# Handle mappings for "Category" / "Sub-Category"
def category_mappings(row):
    category = row['Category']
    if category == 'SysEng':
        row['Category'] = 'Infrastructure'
    elif category == 'User Accounts':
        row['Category'] = 'WFH'
    elif category == 'Application Support':
        row['Category'] = 'Ubiquity Tools'
    elif category == 'InTouch':
        row['Category'] = 'Client Tools'
        row['Item'] = row['Sub-Category']
        row['Sub-Category'] = 'InTouch'
    elif category == 'MDM Installation':
        row['Category'] = 'Ubiquity Tools'
        row['Item'] = row['Sub-Category']
        row['Sub-Category'] = 'Endpoint Central MDM'
    if category == 'Monitoring':
        row['Category'] = 'Infrastructure'
        row['Item'] = row['Sub-Category']
        row['Sub-Category'] = 'Monitoring Alerts'
    if category == 'TELCO':
        row['Category'] = 'Ubiquity Tools'
        row['Item'] = row['Sub-Category']
        row['Sub-Category'] = 'Telco'
        
    return row

# Handle mappings for "Template"
def type_template_mapping(row):
    type_row = row['Type']
    if type_row == 'Service Request':
        row['Template Name'] = 'GENERAL SERVICE REQUEST'
    elif type_row == 'Incident':
        row['Template Name'] = 'New Incident Request'
        
    return row

# Handle mappings for "Template"
def status_template_mapping(row):
    status_row = row['Status']
    if status_row == 'Pending':
        row['Status'] = 'Closed'
        
    return row

# Handle null "Subject" value
def subject_mapping(row):
    subject_row = row['Subject']
    if pd.isna(subject_row) or subject_row == '':
        row['Subject'] = 'Untitled'
    else:
        row['Subject'] = subject_row.replace('<', '(').replace('>', ')')

    # Limit the length to 250 characters
    if len(row['Subject']) > 250:
        row['Subject'] = row['Subject'][:250]
        
    return row
    
# Format date and time columns#
def format_datetime_columns(row):
    columns_to_format = ['Closed Time', 'Created Time', 'Due by Time', 'Initial Response Time', 'Resolved Time', 'Last Updated Time']
    
    for col in columns_to_format:
        if pd.notna(row[col]):
            try:
                datetime_obj = datetime.strptime(str(row[col]), "%d/%m/%Y %I:%M")
                formatted_datetime = datetime_obj.strftime("%m-%d-%Y %I:%M:%S")
                row[col] = formatted_datetime
            except ValueError:
                try:
                    datetime_obj = datetime.strptime(str(row[col]), "%d/%m/%Y %H:%M")
                    formatted_datetime = datetime_obj.strftime("%m-%d-%Y %H:%M:%S")
                    row[col] = formatted_datetime
                except ValueError:
                    pass  # Handle the case where the value is not in the expected format

    return row


# Function to clean up rows with long cell values
def cleanup_long_rows(df):
    max_cell_length = 32700  # 32767 Maximum Excel cell length (approximately)
    columns_to_check = ['Description']  # Adjust as needed

    rows_to_remove = set()  # Store rows to be removed

    for col in columns_to_check:
        for index, value in enumerate(df[col]):
            if isinstance(value, str) and len(value) > max_cell_length:
                rows_to_remove.add(index)  # Add the current row index
                # Also remove the two rows below it if they exist
                rows_to_remove.add(index + 1)
                rows_to_remove.add(index + 2)

    # Remove the identified rows
    df = df.drop(index=rows_to_remove).reset_index(drop=True)

    return df

# Function to clean up rows with non-numeric "Ticket Id" values
def cleanup_non_numeric_ticket_ids(df):
    column_to_check = 'Ticket Id'

    # Convert the column to strings and check if each value is numeric
    df[column_to_check] = df[column_to_check].astype(str)
    is_numeric = df[column_to_check].str.isnumeric()

    # Remove rows with non-numeric "Ticket Id" values
    df = df[is_numeric].reset_index(drop=True)

    return df

# Function to save removed rows to a single Excel file
def save_removed_rows_to_excel(removed_rows, output_directory, output_filename):
    if removed_rows:
        # Concatenate the removed rows into a single DataFrame
        removed_rows_df = pd.concat(removed_rows, ignore_index=True)

        # Create the output Excel file path
        excel_path = os.path.join(output_directory, output_filename)

        # Save the removed rows DataFrame to an Excel file
        removed_rows_df.to_excel(excel_path, index=False, engine='openpyxl')
        
# Define the input and output directory
input_directory = 'pending'
output_directory = 'pending-output'

# Create the output directory if it doesn't exist
os.makedirs(output_directory, exist_ok=True)

all_removed_rows = []

# Iterate through each CSV file in the input directory
for filename in os.listdir(input_directory):
    if filename.endswith('.csv'):
        # Read the CSV into a DataFrame
        csv_path = os.path.join(input_directory, filename)
        df = pd.read_csv(csv_path)

        # Set "Item" column to empty string for all rows
        df['Template Name'] = ''
        
        # Set "Item" column to empty string for all rows
        df['Item'] = ''
        df['Status'] = 'Closed'
                
        # Apply the replacements and modifications to the DataFrame
        df = df.apply(department_mappings, axis=1)
        df = df.apply(impact_mappings, axis=1)
        df = df.apply(priority_mappings, axis=1)
        df = df.apply(source_mappings, axis=1)
        df = df.apply(urgency_mappings, axis=1)
        df = df.apply(groups_mappings, axis=1)
        df = df.apply(group_mappings, axis=1)
        df = df.apply(category_mappings, axis=1)
        df = df.apply(type_template_mapping, axis=1)
        df = df.apply(subject_mapping, axis=1)
        df = df.apply(format_datetime_columns, axis=1)
        #df = df.apply(status_template_mapping, axis=1)
        #df = cleanup_non_numeric_ticket_ids(df)
        
        # Store removed rows for later
        is_numeric = df['Ticket Id'].str.isnumeric()
        removed_rows = pd.read_csv(csv_path)[~is_numeric]
        all_removed_rows.append(removed_rows)
        
        # Rename specific headers
        df.rename(columns={'Ticket Id': 'Request ID', 'Agent': 'Freshservice Technician', 'Initial Response Time': 'Responded Date', 'Site Affected' : 'Freshservice Site/s Affected', 'Requester Email': 'Email id', 'Sub-Category' : 'Sub Category', 'Source' : 'Mode', 'Client affected' : 'Freshservice Client Affected', 'Closed Time' : 'Completed Date', 'Created Time' : 'Created Date', 'Due by Time': 'Due by date', 'Type' : 'Request Type'}, inplace=True)
        
        # Create the output Excel file path
        excel_filename = os.path.splitext(filename)[0] + '.xlsx'
        excel_path = os.path.join(output_directory, excel_filename)

        # Save the DataFrame to an Excel file
        df.to_excel(excel_path, index=False, engine='openpyxl')
    
        print(f"CSV data formatted and saved as {excel_filename}")

# Save all removed rows to a single Excel file
#if all_removed_rows:
    #all_removed_rows_df = pd.concat(all_removed_rows, ignore_index=True)
    #all_removed_rows_df.to_excel(os.path.join(output_directory, 'all_removed_rows.xlsx'), index=False, engine='openpyxl')
    
print("Conversion complete.")