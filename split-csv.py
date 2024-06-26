import os
import csv

def split_csv(input_csv, output_folder, max_rows=3001):
    with open(input_csv, mode="r", newline="", encoding="utf-8") as csv_file:
        csv_reader = csv.reader(csv_file)
        header = next(csv_reader)

        row_count = 0
        file_count = 1
        output_csv = None
        csv_writer = None

        for row in csv_reader:
            if row_count == 0 or not output_csv:
                # Create a new output CSV file
                output_csv = os.path.join(output_folder, f"bankingops-{file_count}.csv")
                csv_writer = csv.writer(open(output_csv, mode="w", newline="", encoding="utf-8"))
                csv_writer.writerow(header)  # Write the header to the new file
                file_count += 1
                row_count = 0

            csv_writer.writerow(row)
            row_count += 1

            if row_count >= max_rows - 1:  # Subtract 1 to account for the header
                row_count = 0

def main():
    input_csv = "BankingOps.csv"  # Specify the input CSV file
    output_folder = "BankingOps-output"  # Specify the output folder for split CSVs

    os.makedirs(output_folder, exist_ok=True)
    split_csv(input_csv, output_folder)

if __name__ == "__main__":
    main()
