import csv  # Import the csv module for reading and writing CSV files

# Load data from the file 'computer_sales.csv'
ram_data = {}  # Initialize an empty dictionary to store unique RAM data

with open('../Original data/computer_sales.csv', 'r') as sales_file:
    # Create a CSV reader object that reads rows as dictionaries
    csv_reader = csv.DictReader(sales_file)
    
    ram_id_set = set()  # Initialize an empty set to keep track of unique RAM identifiers
    
    # Loop through each row in the CSV file
    for row in csv_reader:
        # Create a unique identifier for each RAM module based on multiple fields
        ram_id = (row['ram_vendor_name'], row['ram_brand'], row['ram_name'], 
                  row['ram_type'], row['ram_size'], row['ram_clock'])
        
        # Check if this unique RAM identifier has been encountered before
        if ram_id not in ram_id_set:
            # If the RAM module is unique, add the identifier to the set
            ram_id_set.add(ram_id)
            
            # Store the RAM details in the ram_data dictionary using the unique identifier as the key
            ram_data[ram_id] = {
                'ram_vendor_name': row['ram_vendor_name'],
                'ram_brand': row['ram_brand'],
                'ram_name': row['ram_name'],
                'ram_type': row['ram_type'],
                'ram_size': row['ram_size'],
                'ram_clock': row['ram_clock']
            }

with open('../Tables CSV/RAM.csv', 'w', newline='') as output_file:
    # Define the column names (field names) for the output CSV file
    fieldnames = ['ram_id', 'ram_vendor_name', 'ram_brand', 'ram_name', 'ram_type', 'ram_size', 'ram_clock']
    
    # Create a CSV writer object that writes rows as dictionaries
    writer = csv.DictWriter(output_file, fieldnames=fieldnames)
    
    # Write the header row with column names to the output file
    writer.writeheader()
    
    # Loop through the ram_data dictionary and write each RAM entry to the CSV file
    for idx, (ram_id, details) in enumerate(ram_data.items()):
        # Write a row for each RAM, assigning a sequential integer 'ram_id' as an index
        writer.writerow({
            'ram_id': idx,  # Use the loop index as the unique RAM ID in the output file
            'ram_vendor_name': details['ram_vendor_name'],
            'ram_brand': details['ram_brand'],
            'ram_name': details['ram_name'],
            'ram_type': details['ram_type'],
            'ram_size': details['ram_size'],
            'ram_clock': details['ram_clock']
        })

# Print a confirmation message after writing the data
print("RAM table created.")