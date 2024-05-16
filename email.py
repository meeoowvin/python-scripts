import pandas as pd

def generate_requester_email(requester_name):
    if not requester_name or ' ' not in requester_name:
        # Handle blank or single-word names
        return 'noreply@ubiquitygs.com'

    # Split the name into first and last names
    names = requester_name.split()
    first_name = names[0].lower()
    last_name = '.'.join(names[1:]).lower() if len(names) > 1 else ''

    # Check if the name represents a department or a non-name value
    non_name_values = ['IT Support Desk', 'HR Department', 'Finance Team']  # Add more as needed
    if requester_name in non_name_values:
        # Use a generic email pattern for non-name values
        return f"{requester_name.replace(' ', '').lower()}@ubiquity.com"
    else:
        # Generate the email in the required format
        return f"{first_name}.{last_name}@ubiquitygs.com"

def update_requester_email(input_csv_file, output_csv_file):
    try:
        # Read the CSV file into a DataFrame with UTF-8 encoding
        df = pd.read_csv(input_csv_file, encoding='utf-8')

        # Update the 'Requester Email' column based on 'Requester Name'
        #df['Requester Email'] = df['Requester Name'].apply(generate_requester_email)
        df['To Address'] = df['To Address'].apply(generate_requester_email)
        
        # Save the updated DataFrame to a new CSV file with UTF-8 encoding
        df.to_csv(output_csv_file, index=False, encoding='utf-8')

        print(f"CSV file generated: {output_csv_file}")
    except Exception as e:
        print(f"Error processing CSV file: {str(e)}")

if __name__ == "__main__":
    input_csv_file = "complete-conversations.csv"  # Replace with the path to your source CSV file
    output_csv_file = "complete-conversations.csv"  # Replace with the desired output CSV file

    # Call the function to update 'Requester Email'
    update_requester_email(input_csv_file, output_csv_file)