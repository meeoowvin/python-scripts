import pandas as pd

def show_unique_values(csv_file, column_name):
    try:
        df = pd.read_csv(csv_file)
        unique_values = df[column_name].unique()
        
        print(f"Unique values in '{column_name}' column:")
        for value in unique_values:
            print(value)
            
    except Exception as e:
        print(f"Error: {e}")

def main():
    csv_file = "Ubiquity Organizational Employee Data.csv"  # Specify the CSV file
    column_name = "Location"  # Specify the column name
    #column_name = "Freshservice Site/s Affected"

    show_unique_values(csv_file, column_name)

if __name__ == "__main__":
    main()
