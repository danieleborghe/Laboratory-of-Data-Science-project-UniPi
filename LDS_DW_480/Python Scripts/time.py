import csv  # Import the csv module for reading and writing CSV files
from datetime import datetime  # Import the datetime module to handle date and time operations

def parse_time_code(time_code):
    # Convert the time code (in 'YYYYMMDD' format) to a datetime object
    dt = datetime.strptime(str(time_code), "%Y%m%d")
    
    # Extract and return different components of the date
    return {
        'day': dt.day,  # Day of the month
        'month': dt.month,  # Month of the year
        'year': dt.year,  # Year
        'day_of_week': dt.strftime('%A'),  # Day of the week as a full name (e.g., 'Monday')
        'week': dt.isocalendar()[1],  # ISO calendar week of the year
        'quarter': f"Q{(dt.month - 1) // 3 + 1}"  # Quarter of the year formatted as 'Q1', 'Q2', etc.
    }

# Load data from the file 'computer_sales.csv'
time_data = {}  # Initialize an empty dictionary to store unique time data

with open('../Original data/computer_sales.csv', 'r') as sales_file:
    # Create a CSV reader object that reads rows as dictionaries
    csv_reader = csv.DictReader(sales_file)
    
    time_id_set = set()  # Initialize an empty set to keep track of unique time codes
    
    # Loop through each row in the CSV file
    for row in csv_reader:
        time_code = row['time_code']  # Extract the 'time_code' field from the current row
        
        # Check if the time code is not empty and hasn't been encountered before
        if time_code and time_code not in time_id_set:
            # If the time code is unique, add it to the set
            time_id_set.add(time_code)
            
            # Parse the time code into its components using the parse_time_code function
            time_components = parse_time_code(time_code)
            
            # Store the parsed time components in the time_data dictionary with the time_code as the key
            time_data[time_code] = time_components

with open('../Tables CSV/Time.csv', 'w', newline='') as output_file:
    # Define the column names (field names) for the output CSV file
    fieldnames = ['time_id', 'day', 'month', 'year', 'day_of_week', 'week', 'quarter']
    
    # Create a CSV writer object that writes rows as dictionaries
    writer = csv.DictWriter(output_file, fieldnames=fieldnames)
    
    # Write the header row with column names to the output file
    writer.writeheader()
    
    # Loop through the time_data dictionary and write each time entry to the CSV file
    for time_id, components in time_data.items():
        # Write a row for each time entry, using the components parsed earlier
        writer.writerow({
            'time_id': time_id,  # The original time code (e.g., '20230901')
            'day': components['day'],  # Extracted day component
            'month': components['month'],  # Extracted month component
            'year': components['year'],  # Extracted year component
            'day_of_week': components['day_of_week'],  # Extracted day of the week component
            'week': components['week'],  # Extracted ISO calendar week component
            'quarter': components['quarter']  # Extracted quarter as 'Q1', 'Q2', etc.
        })

# Print a confirmation message after writing the data
print("Time table created.")