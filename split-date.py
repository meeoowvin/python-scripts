import os
import pandas as pd

def split_csv_file(file_path, output_dir, row_limit=3000):
    # Make sure output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Read the CSV file
    data = pd.read_csv(file_path)

    # Split the data into chunks
    chunks = [data[i:i+row_limit] for i in range(0, data.shape[0], row_limit)]

    print(f'Total chunks to be created: {len(chunks)}')

    # Write each chunk to a separate CSV file
    for i, chunk in enumerate(chunks):
        output_file_path = os.path.join(output_dir, f'requests-date_{i+1}.csv')
        chunk.to_csv(output_file_path, index=False, encoding='utf-8')
        print(f'Generated file: {output_file_path}')

# Usage
split_csv_file('Requests-Date-Data.csv', 'hello')