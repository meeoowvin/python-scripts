import os
import pandas as pd

def parse_date(date_str):
    try:
        # Try to parse the date using the provided format
        return pd.to_datetime(date_str, format="%d/%m/%Y %H:%M:%S", errors='raise')
    except ValueError:
        try:
            # Try to parse the date with a different format
            return pd.to_datetime(date_str, errors='raise')
        except ValueError:
            # If parsing fails, return NaT (Not a Time) to indicate missing or invalid date
            return pd.NaT

def split_csv_by_year(source_csv_file, output_folder):
    os.makedirs(output_folder, exist_ok=True)

    try:
        # Read the source CSV file into a DataFrame
        df = pd.read_csv(source_csv_file)

        # Parse the 'Created Time' column using the custom function
        df['Created Time'] = df['Created Time'].apply(parse_date)

        # Drop rows with missing or invalid dates
        df = df.dropna(subset=['Created Time'])

        # Extract the 'Year' from the 'Created Time' column
        df['Year'] = df['Created Time'].dt.year

        # Split the DataFrame by year and save each year's data to a separate CSV file
        for year, year_data in df.groupby('Year'):
            year_csv_file = os.path.join(output_folder, f"{year}-complete.csv")
            year_data.to_csv(year_csv_file, index=False)
            
            # Print information about the generated file
            print(f"CSV file generated: {year_csv_file}")
            print(f"Number of rows in {year_csv_file}: {len(year_data)}")

    except Exception as e:
        print(f"Error processing source CSV file: {str(e)}")

if __name__ == "__main__":
    source_csv_file = "complete-final.csv"  # Replace with the path to your source CSV file
    output_folder = "output"  # Replace with the desired output folder

    # Split the source CSV file by year
    split_csv_by_year(source_csv_file, output_folder)
