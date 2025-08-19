import csv  # Import the csv module for reading and writing CSV files

# Load data from the file 'computer_sales.csv'
cpu_data = {}  # Initialize an empty dictionary to store unique CPU data

with open('../Original data/computer_sales.csv', 'r') as sales_file:
    # Create a CSV reader object that reads rows as dictionaries
    csv_reader = csv.DictReader(sales_file)
    
    cpu_id_set = set()  # Initialize an empty set to keep track of unique CPU identifiers
    
    # Loop through each row in the CSV file
    for row in csv_reader:
        # Create a unique identifier for each CPU based on multiple fields
        cpu_id = (row['cpu_vendor_name'], row['cpu_brand'], row['cpu_series'], row['cpu_name'], row['cpu_n_cores'], row['cpu_socket'])
        
        # Check if this unique CPU identifier has been encountered before
        if cpu_id not in cpu_id_set:
            # If the CPU is unique, add the identifier to the set
            cpu_id_set.add(cpu_id)
            
            # Store the CPU details in the cpu_data dictionary using the unique identifier as the key
            cpu_data[cpu_id] = {
                'cpu_vendor_name': row['cpu_vendor_name'],
                'cpu_brand': row['cpu_brand'],
                'cpu_series': row['cpu_series'],
                'cpu_name': row['cpu_name'],
                'cpu_n_cores': row['cpu_n_cores'],
                'cpu_socket': row['cpu_socket']
            }

with open('../Tables CSV/CPU.csv', 'w', newline='') as output_file:
    # Define the column names (field names) for the output CSV file
    fieldnames = ['cpu_id', 'cpu_vendor_name', 'cpu_brand', 'cpu_series', 'cpu_name', 'cpu_n_cores', 'cpu_socket']
    
    # Create a CSV writer object that writes rows as dictionaries
    writer = csv.DictWriter(output_file, fieldnames=fieldnames)
    
    # Write the header row with column names to the output file
    writer.writeheader()
    
    # Loop through the cpu_data dictionary and write each CPU entry to the CSV file
    for idx, (cpu_id, details) in enumerate(cpu_data.items()):
        # Write a row for each CPU, assigning a sequential integer 'cpu_id' as an index
        writer.writerow({
            'cpu_id': idx,  # Use the loop index as the unique CPU ID in the output file
            'cpu_vendor_name': details['cpu_vendor_name'],
            'cpu_brand': details['cpu_brand'],
            'cpu_series': details['cpu_series'],
            'cpu_name': details['cpu_name'],
            'cpu_n_cores': details['cpu_n_cores'],
            'cpu_socket': details['cpu_socket']
        })

# Print a confirmation message after writing the data
print("CPU table created.")