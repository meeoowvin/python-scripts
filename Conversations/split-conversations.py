import pandas as pd

def split_csv(source_filepath, dest_folder, split_file_prefix,
              records_per_file, max_size):
    # Create a CSV reader that reads the source file in chunks
    reader = pd.read_csv(source_filepath, chunksize=records_per_file, encoding='utf-8')

    total_files = 0
    for i, chunk in enumerate(reader):
        # Convert the chunk of data to CSV
        csv_data = chunk.to_csv(index=False, encoding='utf-8')

        # If the size of the data is larger than the maximum size,
        # decrease the number of records until it fits
        while len(csv_data) > max_size:
            chunk = chunk.iloc[:-1]
            csv_data = chunk.to_csv(index=False, encoding='utf-8')

        # Write the chunk of data to a new CSV file with utf-8 encoding
        with open(f"{dest_folder}/{split_file_prefix}_{i}.csv", "w", encoding='utf-8') as f:
            f.write(csv_data)

        print(f"Generated file {split_file_prefix}_{i}.csv")
        total_files += 1

    print(f"Generated a total of {total_files} files")

split_csv('2017 Conversation Data.csv', '2017 Data', '2017-conversation-data', 3000, 4.65 * 1024 * 1024)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               