import pandas as pd
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
    elif group == 'Escalation':
        row['Group'] = 'No Group'
        
    return row

# Handle mappings for "Site Affected" / "Group"
def group_mappings(row):
    site_affected = row['Site Affected']
    group = row['Group']
    if site_affected == 'Bacolod' or site_affected == 'Phiippines Manila Bacolod' or site_affected == 'Bac Support' or site_affected == 'Philippines (Manila & Bacolod)' or site_affected == 'Philippines Manila Amp Bacolod' or site_affected == 'Bacolodcred' or site_affected == 'Bacolodc' or site_affected == 'Bacolodb' or site_affected == 'Bacolodn' or site_affected == 'Bacolodf' or site_affected == 'Bac' or site_affected == 'Bacolodba' or site_affected == 'Bacolodbac' or site_affected == 'Ac':
        row['Site Affected'] = '["BCD Cyber Centre"]'
        if group == 'Field Support':
            row['Group'] = 'End User Support (EUS-BCD-CYBER)'
    elif site_affected == 'Budapest':
        row['Site Affected'] = '["BUD Váci út"]'
        if group == 'Field Support':
            row['Group'] = 'End User Support (EUS-BUD)'
    elif site_affected == 'CA Datacenter' or site_affected == 'Ca Datacenter':
        row['Site Affected'] = '["CA Gillette AVE"]'
        if group == 'Field Support':
            row['Group'] = 'End User Support (EUS-AMERICAS)'
    elif site_affected == 'Cagayan de Oro' or site_affected == 'Cagayan De Oro':
        row['Site Affected'] = '["CDO Limketkai BPO Bldg"]'
        if group == 'Field Support':
            row['Group'] = 'End User Support (EUS-CDO)'
    elif site_affected == 'Colombia':
        row['Site Affected'] = '["BOG CCI Building"]'
        if group == 'Field Support':
            row['Group'] = 'End User Support (EUS-COL)'
    elif site_affected == 'El Salvador' or site_affected == 'Es Support' or site_affected == 'El Salvadorel Sa':
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
    elif site_affected == 'Manila' or site_affected == 'Manilan' or site_affected == 'Mnl Support' or site_affected == 'Global' or site_affected == 'Globalg':
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
    elif site_affected == 'NJ Datacenter' or site_affected == 'NJ-Datacenter' or site_affected == 'New Jersey' or site_affected == 'Nj Datacenter':
        row['Site Affected'] = '["NJ 300 boulevard East"]'
        if group == 'Field Support':
            row['Group'] = 'End User Support (EUS-AMERICAS)'
    elif site_affected == 'Omaha' or site_affected == 'Omh Support':
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
    elif site_affected == 'USA' or site_affected == 'Usa' or site_affected == 'Wilkes Barre':
        row['Site Affected'] = '["NYC Avenue of the Americas"]'
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
    elif category == 'Monitoring':
        row['Category'] = 'Infrastructure'
        row['Item'] = row['Sub-Category']
        row['Sub-Category'] = 'Monitoring Alerts'
    elif category == 'TELCO':
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

# Handle mappings for "Last Updated Time"
def last_updated_time_mapping(row):
    ct_row = row['Closed Time']
    row['Last Updated Time'] = ct_row
    return row

# Handle mappings for "Technician"
def technician_mapping(row):
    agent = row['Agent']
    row['Technician'] = agent
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
                formatted_datetime = datetime_obj.strftime("%Y/%m/%d %I%M%S %p")
                row[col] = formatted_datetime
            except ValueError:
                try:
                    datetime_obj = datetime.strptime(str(row[col]), "%d/%m/%Y %H:%M")
                    formatted_datetime = datetime_obj.strftime("%Y/%m/%d %I%M%S %p")
                    row[col] = formatted_datetime
                except ValueError:
                    pass  # Handle the case where the value is not in the expected format

    return row
        
def convert_custom_datetime_format(row):
    columns_to_format = ['Initial Response Time']

    for col in columns_to_format:
        try:
            # Parse the input datetime string
            input_datetime = str(row[col])
            parsed_datetime = datetime.strptime(input_datetime, "%Y-%m-%dT%H:%M:%S%z")

            # Convert to the desired format
            formatted_datetime = parsed_datetime.strftime("%Y/%m/%d %I:%M:%S %p")

            row[col] = formatted_datetime
        except ValueError:
            # Handle the case where the input datetime is not in the expected format
            pass  # Do nothing if parsing fails

    return row

def update_csv(input_csv):
    # Read the CSV into a DataFrame
    df = pd.read_csv(input_csv)

    # Set "Item" column to empty string for all rows
    df['Template Name'] = ''
    df['Technician'] = ''
        
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
    df = df.apply(technician_mapping, axis=1)
    df = df.apply(convert_custom_datetime_format, axis=1)
    df = df.apply(last_updated_time_mapping, axis=1)
    df = df.apply(format_datetime_columns, axis=1)
    
    # Rename specific headers
    df.rename(columns={'Ticket Id': 'Request ID', 'Agent': 'Freshservice Technician', 'Initial Response Time': 'Responded Date', 'Site Affected' : 'Freshservice Site/s Affected', 'Requester Email': 'Email id', 'Sub-Category' : 'Sub Category', 'Source' : 'Mode', 'Client affected' : 'Freshservice Client Affected', 'Closed Time' : 'Completed Date', 'Created Time' : 'Created Date', 'Due by Time': 'Due by date', 'Type' : 'Request Type'}, inplace=True)
    
    # Save the updated DataFrame back to the original CSV file, overwriting it
    df.to_csv(input_csv, index=False, encoding='utf8')

    print(f"CSV file '{input_csv}' updated.")
    
# Specify the input CSV file
input_csv = "2014-complete.csv"

# Update the CSV file
update_csv(input_csv)
    
print("Script complete.")