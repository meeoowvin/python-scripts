import pandas as pd

# Replace 'input.csv' with the path to your CSV file
input_csv = 'Requests_Notifications_3.csv'

# Replace 'output.csv' with the desired output CSV file path
output_csv = '3.csv'

# Read the CSV file into a pandas DataFrame
df = pd.read_csv(input_csv)

# Remove all data from the "description" column
df['Description'] = ''

# Write the modified DataFrame to a new CSV file
df.to_csv(output_csv, index=False)

print(f'Data in the "description" column of CSV file "{input_csv}" has been removed. Result saved to "{output_csv}".')
