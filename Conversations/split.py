import os
import pandas as pd

def split_and_save_by_year(csv_file, max_file_size_mb=7.85, max_rows_per_file=3000):
    # Read the CSV file
    df = pd.read_csv(csv_file, encoding='utf8')

    # Group the DataFrame by Year
    grouped_data = df.groupby('Year')

    total_files_generated = 0
    total_tickets = 0

    for year, year_group in grouped_data:
        # Create a folder for the year
        year_folder = f"{year} Conversation Data"
        os.makedirs(year_folder, exist_ok=True)

        # Calculate an initial chunk size based on max_rows_per_file
        chunk_size = min(len(year_group), max_rows_per_file)

        # Split data into chunks of the calculated chunk_size
        chunks = [year_group[i:i + chunk_size] for i in range(0, len(year_group), chunk_size)]

        for idx, chunk in enumerate(chunks, start=1):
            # Save the year's data to CSV file(s) inside the year folder
            output_csv = os.path.join(year_folder, f"{year}-conversation-data-part{idx}.csv")

            # Save the chunk to CSV
            chunk.to_csv(output_csv, index=False, encoding='utf8')
            print(f"Saved {len(chunk)} records to: {output_csv}")
            total_files_generated += 1
            total_tickets += len(chunk)

        # If the loop completes without breaking, the chunk size is acceptable

    # Print the count of files generated for each year
    print("\nFiles generated for each year:")
    for year, _ in grouped_data:
        year_folder = f"{year} Conversation Data"
        file_count = len([f for f in os.listdir(year_folder) if f.startswith(f"{year}-conversation-data-") and f.endswith('.csv')])
        print(f"{year_folder}: {file_count} files")

    print(f"\nTotal files generated: {total_files_generated}")
    print(f"Total tickets in generated files: {total_tickets}")

if __name__ == "__main__":
    # Specify the path to the CSV file
    csv_file = "complete-conversations.csv"  # Replace with your CSV file path

    # Call the function to split and save the data
    split_and_save_by_year(csv_file)