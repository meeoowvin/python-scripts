import os
import pandas as pd

def split_and_save_by_year_month(csv_file, max_file_size_mb=4.65, max_rows_per_file=3000):
    # Read the CSV file
    df = pd.read_csv(csv_file, encoding='utf8')

    # Group the DataFrame by Year and Month
    grouped_data = df.groupby(['Year', 'Month'])

    total_files_generated = 0

    for (year, month), period_group in grouped_data:
        # Create a folder for the year
        year_folder = f"{year}"
        os.makedirs(year_folder, exist_ok=True)

        # Create a folder for the month inside the year folder
        month_folder = os.path.join(year_folder, str(month))
        os.makedirs(month_folder, exist_ok=True)

        # Save the month's data to CSV file(s) inside the month folder
        output_csv = os.path.join(month_folder, f"conversation-data-{month}-{year}.csv")

        # Check if the file exists before getting its size
        if os.path.exists(output_csv):
            file_size_mb = os.path.getsize(output_csv) / (1024 * 1024)

            if file_size_mb > max_file_size_mb or len(period_group) > max_rows_per_file:
                # If the size or rows exceed the limit, create a new CSV file
                count = 1
                while os.path.exists(output_csv):
                    count += 1
                    output_csv = os.path.join(month_folder, f"conversation-data-{month}-{year}-{count}.csv")

                print(f"File size ({file_size_mb:.2f} MB) or row count ({len(period_group)}) exceeds the limit. "
                      f"Saving to a new file: {output_csv}")

        # Split data into chunks of max_rows_per_file
        chunks = [period_group[i:i + max_rows_per_file] for i in range(0, len(period_group), max_rows_per_file)]

        for idx, chunk in enumerate(chunks, start=1):
            chunk_output_csv = output_csv.replace('.csv', f'-part{idx}.csv') if len(chunks) > 1 else output_csv
            chunk.to_csv(chunk_output_csv, index=False, encoding='utf8')
            print(f"Saved {len(chunk)} records to: {chunk_output_csv}")
            total_files_generated += 1

    # Print the count of files generated for each month/year
    print("\nFiles generated for each month/year:")
    for (year, month), _ in grouped_data:
        month_folder = os.path.join(f"{year}", str(month))
        file_count = len([f for f in os.listdir(month_folder) if f.startswith('conversation-data-') and f.endswith('.csv')])
        print(f"{month}-{year}: {file_count} files")

    print(f"\nTotal files generated: {total_files_generated}")

if __name__ == "__main__":
    # Specify the path to the CSV file
    csv_file = "complete-conversations-complete.csv"  # Replace with your CSV file path

    # Call the function to split and save the data
    split_and_save_by_year_month(csv_file)