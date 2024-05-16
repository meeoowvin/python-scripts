import csv
from datetime import datetime

# Input and output file paths
input_csv_path = 'updated-requests part1.csv'
output_csv_path = 'updated-requests_part1.csv'

def format_date(date_str):
    try:
        # Parse the date string
        dt = datetime.strptime(date_str, '%b %d, %Y %I:%M %p')
        # Format as "yyyy-MM-dd HH:mm:ss"
        return dt.strftime('%Y-%m-%d %H:%M:%S')
    except ValueError:
        # Handle invalid date strings (optional)
        return ''  # You can customize this behavior

def main():
    try:
        with open(input_csv_path, 'r', newline='') as source:
            with open(output_csv_path, 'w', newline='', encoding='utf-8') as result:
                reader = csv.DictReader(source)
                fieldnames = reader.fieldnames

                writer = csv.DictWriter(result, fieldnames=fieldnames)
                writer.writeheader()

                for row in reader:
                    # Format the date fields
                    row['Created Date'] = format_date(row['Created Date'])
                    row['Due by date'] = format_date(row['Due by date'])

                    # Write the row to the output file
                    writer.writerow(row)

        print(f"Formatted CSV saved to {output_csv_path}")
    except FileNotFoundError:
        print(f"Input CSV file '{input_csv_path}' not found.")

if __name__ == '__main__':
    main()
