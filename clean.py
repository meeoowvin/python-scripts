import pandas as pd
from bs4 import BeautifulSoup

# Function to clean up rows with long cell values
def cleanup_long_rows(df):
    max_cell_length = 32700  # 32767 Maximum Excel cell length (approximately)
    columns_to_check = ['Description']  # Adjust as needed

    rows_to_remove = set()  # Store rows to be removed

    for col in columns_to_check:
        for index, value in enumerate(df[col]):
            if isinstance(value, str) and len(value) > max_cell_length:
                rows_to_remove.add(index)  # Add the current row index
                # Also remove the two rows below it if they exist
                rows_to_remove.add(index + 1)
                rows_to_remove.add(index + 2)

    # Remove the identified rows
    df = df.drop(index=rows_to_remove).reset_index(drop=True)

    return df

# Function to clean up rows with non-numeric "Ticket Id" values
def cleanup_non_numeric_ticket_ids(df):
    column_to_check = 'Ticket Id'

    # Convert the column to strings and check if each value is numeric
    df[column_to_check] = df[column_to_check].astype(str)
    is_numeric = df[column_to_check].str.isnumeric()

    # Remove rows with non-numeric "Ticket Id" values
    df = df[is_numeric].reset_index(drop=True)

    return df

# Function to clean up rows with non-HTML "Description" values
def cleanup_non_html_description(df):
    column_to_check = 'Description'

    rows_to_remove = set()  # Store rows to be removed

    for index, value in enumerate(df[column_to_check]):
        if isinstance(value, str):
            soup = BeautifulSoup(value, 'html.parser')
            if soup.text == value:  # Check if the content is not HTML (e.g., plain text)
                rows_to_remove.add(index)  # Add the current row index

    # Remove the identified rows
    df = df.drop(index=rows_to_remove).reset_index(drop=True)

    return df

if __name__ == "__main__":
    # Specify the path to the input CSV file and the output CSV file
    input_csv_file = "BankingOps FreshDesk.csv"  # Replace with your input CSV file path
    output_csv_file = "BankingOps.csv"  # Replace with your desired output CSV file path

    # Read the CSV file into a DataFrame
    df = pd.read_csv(input_csv_file)

    initial_row_count = len(df)

    # Call the function to clean up non-numeric "Ticket Id" values
    df = cleanup_non_numeric_ticket_ids(df)

    # Calculate the number of rows removed
    rows_removed_non_numeric = initial_row_count - len(df)
    print(f"Rows with non-numeric 'Ticket Id' values removed: {rows_removed_non_numeric}")

    # Call the function to clean up long cell values in the "Description" column
    df = cleanup_long_rows(df)

    # Calculate the number of rows removed
    rows_removed_long_description = initial_row_count - len(df)
    print(f"Rows with long 'Description' values removed: {rows_removed_long_description}")

    # Call the function to clean up rows with non-HTML "Description" values
    #df = cleanup_non_html_description(df)

    # Calculate the number of rows removed
    #rows_removed_non_html_description = initial_row_count - len(df)
    #print(f"Rows with non-HTML 'Description' values removed: {rows_removed_non_html_description}")

    # Save the cleaned data to a new CSV file
    df.to_csv(output_csv_file, index=False)

    remaining_row_count = len(df)
    print(f"Cleaning completed.")
    print(f"Initial row count: {initial_row_count}")
    print(f"Remaining row count: {remaining_row_count}")