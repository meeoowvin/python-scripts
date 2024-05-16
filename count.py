import csv

# Set a larger field size limit
csv.field_size_limit(1000000000)

def count_rows(csv_files):
    total_rows = 0
    for csv_file in csv_files:
        with open(csv_file, 'r', encoding="utf8") as file:
            csv_reader = csv.reader(file)
            # Skip the header row
            next(csv_reader, None)
            # Count the remaining rows
            row_count = sum(1 for row in csv_reader)
            total_rows += row_count
        print(f"Number of rows in {csv_file}: {row_count}")
    #print(f"Total number of rows across all files: {total_rows}")
    #print("As of 11/30/2023, total tickets on SD+: 425158")

# Replace the list with the actual paths to your CSV files
file_paths = ['output.csv']
count_rows(file_paths)