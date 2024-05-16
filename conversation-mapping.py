import pandas as pd
from datetime import datetime
from pandas.io.formats import excel

# Suppress header styling
excel.ExcelFormatter.header_style = None

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
    columns_to_format = ['Send Time']
    
    for col in columns_to_format:
        if pd.notna(row[col]):
            try:
                datetime_obj = datetime.strptime(str(row[col]), "%d%m/%Y %I:%M")
                formatted_datetime = datetime_obj.strftime("%Y-%m-%d %I:%M:%S %p")
                row[col] = formatted_datetime
            except ValueError:
                try:
                    datetime_obj = datetime.strptime(str(row[col]), "%d/%m/%Y %H:%M")
                    formatted_datetime = datetime_obj.strftime("%Y-%m-%d %I:%M:%S %")
                    row[col] = formatted_datetime
                except ValueError:
                    pass  # Handle the case where the value is not in the expected format

    return row
        
def convert_custom_datetime_format(row):
    columns_to_format = ['Send Time']

    for col in columns_to_format:
        try:
            # Parse the input datetime string
            input_datetime = str(row[col])
            parsed_datetime = datetime.strptime(input_datetime, "%Y-%m-%dT%H:%M:%S%z")

            # Convert to the desired format
            formatted_datetime = parsed_datetime.strftime("%Y-%m-%d %I:%M:%S")

            row[col] = formatted_datetime
        except ValueError:
            # Handle the case where the input datetime is not in the expected format
            pass  # Do nothing if parsing fails

    return row

def update_csv(input_csv):
    df = pd.read_csv(input_csv)
    df = df.apply(subject_mapping, axis=1)
    df = df.apply(format_datetime_columns, axis=1)
    df = df.apply(convert_custom_datetime_format, axis=1)
    df.to_csv(input_csv, index=False, encoding='utf8')

    print(f"CSV file '{input_csv}' updated.")
    
# Specify the input CSV file
input_csv = "complete-conversations.csv"

# Update the CSV file
update_csv(input_csv)
    
print("Script complete.")