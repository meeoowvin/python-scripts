import csv
import json

# Replace 'input.csv' with the path to your CSV file
csv_path = '2021.csv'

# Replace 'output.json' with the desired output JSON file path
output_json = '2021-complete.json'

# Read the CSV file into a list of dictionaries
csv_data = []
with open(csv_path, mode='r', newline='', encoding='utf-8') as csvfile:
    csv_reader = csv.DictReader(csvfile)
    for row in csv_reader:
        csv_data.append(row)

# Write the list of dictionaries to a JSON file
with open(output_json, mode='w', encoding='utf-8') as jsonfile:
    json.dump(csv_data, jsonfile, indent=2)

print(f'CSV file "{csv_path}" has been successfully converted to JSON file "{output_json}".')
