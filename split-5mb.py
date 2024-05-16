import os
import csv

def get_file_size(file_path):
    return os.path.getsize(file_path)

def split_csv(input_csv, output_folder, max_rows=3001, max_file_size_mb=4.65, max_tickets=3000):
    with open(input_csv, mode="r", newline="", encoding="utf-8") as csv_file:
        csv_reader = csv.reader(csv_file)
        header = next(csv_reader)

        row_count = 0
        file_count = 1
        output_csv = None
        csv_writer = None
        current_file_size = 0
        current_ticket_count = 0

        for row in csv_reader:
            if row_count == 0 or not output_csv:
                # Create a new output CSV file
                output_csv = os.path.join(output_folder, f"2017-conversations-{file_count}.csv")
                csv_writer = csv.writer(open(output_csv, mode="w", newline="", encoding="utf-8"))
                csv_writer.writerow(header)  # Write the header to the new file
                file_count += 1
                row_count = 0
                current_file_size = get_file_size(output_csv)
                current_ticket_count = 0
                print(f"Generating file: {output_csv}")

            csv_writer.writerow(row)
            row_count += 1
            current_ticket_count += 1

            if row_count >= max_rows - 1 or current_ticket_count >= max_tickets:  # Subtract 1 to account for the header
                row_count = 0

            current_file_size = get_file_size(output_csv)
            if current_file_size >= max_file_size_mb * (1024 * 1024):
                print(f"File {output_csv} completed. Size: {current_file_size / (1024 * 1024):.2f} MB, Tickets: {current_ticket_count}")
                # Start a new file
                output_csv = os.path.join(output_folder, f"2017-conversations-{file_count}.csv")
                csv_writer = csv.writer(open(output_csv, mode="w", newline="", encoding="utf-8"))
                csv_writer.writerow(header)
                file_count += 1
                current_file_size = get_file_size(output_csv)
                current_ticket_count = 0
                print(f"Generating file: {output_csv}")
                
        print(f"Total files generated: {file_count - 1}")

def main():
    input_csv = "output-final.csv"  # Specify the input CSV file
    output_folder = "conversation-test"  # Specify the output folder for split CSVs

    os.makedirs(output_folder, exist_ok=True)
    split_csv(input_csv, output_folder, max_file_size_mb=4.65, max_tickets=3000)

if __name__ == "__main__":
    main()
