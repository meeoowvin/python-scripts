import os
import pandas as pd

def split_csv_by_year(source_filepath):
    # Read the source file with utf-8 encoding
    data = pd.read_csv(source_filepath, encoding='utf-8')

    # Get the unique years
    years = data['Year'].unique()

    # Get the directory of the source file
    #directory = os.path.dirname(source_filepath)

    for year in years:
        # Filter the data for the current year
        data_year = data[data['Year'] == year]

        # Create the filename for the current year
        filename = f"{year} Conversation Data.csv"

        # Write the data for the current year to a new CSV file with utf-8 encoding
        data_year.to_csv(filename, index=False, encoding='utf-8')

        print(f"Generated file {filename}")

split_csv_by_year('complete-conversations.csv')