import os
import pandas as pd

# Specify the output folder containing the Excel files
output_folder = 'BankingOps-output'

# Specify the column for which you want to list unique values
column_name = 'Site'  # Change this to the desired column name

# Create an empty set to store unique values
unique_values = set()

# Iterate through each Excel file in the output folder
for filename in os.listdir(output_folder):
    if filename.endswith('.xlsx'):
        excel_path = os.path.join(output_folder, filename)
        df = pd.read_excel(excel_path)

        # Check if the specified column exists in the DataFrame
        if column_name in df:
            column_values = df[column_name].unique()
            unique_values.update(column_values)

# Print the unique values
print(f"Unique values in the '{column_name}' column:")
for value in unique_values:
    print(value)