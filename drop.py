import pandas as pd

def remove_rows_by_request_id(source_csv, request_id_csv, output_csv):
    # Read the source CSV file
    df_source = pd.read_csv(source_csv)

    # Read the CSV file containing Request IDs to be removed
    df_request_ids = pd.read_csv(request_id_csv)

    # Extract Request IDs from the column (assuming the column name is 'Request ID')
    request_ids_to_remove = df_request_ids['Request ID'].tolist()

    # Remove rows from the source CSV based on Request IDs
    df_result = df_source[~df_source['Request ID'].isin(request_ids_to_remove)]

    # Save the result to a new CSV file
    df_result.to_csv(output_csv, index=False)

if __name__ == "__main__":
    # Set the paths for your source CSV, Request ID CSV, and the output CSV
    source_csv_path = "path/to/source.csv"
    request_id_csv_path = "path/to/request_ids.csv"
    output_csv_path = "path/to/output.csv"

    # Call the function to remove rows by Request ID
    remove_rows_by_request_id(source_csv_path, request_id_csv_path, output_csv_path)
