import csv  # Import the csv module for reading and writing CSV files

# Load data from the file 'computer_sales.csv'
gpu_data = {}  # Initialize an empty dictionary to store unique GPU data

with open('../Original data/computer_sales.csv', 'r') as sales_file:
    # Create a CSV reader object that reads rows as dictionaries
    csv_reader = csv.DictReader(sales_file)
    
    gpu_id_set = set()  # Initialize an empty set to keep track of unique GPU identifiers
    
    # Loop through each row in the CSV file
    for row in csv_reader:
        # Create a unique identifier for each GPU based on multiple fields
        gpu_id = (row['gpu_vendor_name'], row['gpu_brand'], row['cpu_series'], 
                  row['gpu_processor_manufacturer'], row['gpu_memory'], row['gpu_memory_type'])
        
        # Check if this unique GPU identifier has been encountered before
        if gpu_id not in gpu_id_set:
            # If the GPU is unique, add the identifier to the set
            gpu_id_set.add(gpu_id)
            
            # Store the GPU details in the gpu_data dictionary using the unique identifier as the key
            gpu_data[gpu_id] = {
                'gpu_vendor_name': row['gpu_vendor_name'],
                'gpu_brand': row['gpu_brand'],
                'cpu_series': row['cpu_series'],  # Note that 'cpu_series' is included, likely related to the GPU
                'gpu_processor_manufacturer': row['gpu_processor_manufacturer'],
                'gpu_memory': row['gpu_memory'],
                'gpu_memory_type': row['gpu_memory_type']
            }

with open('../Tables CSV/GPU.csv', 'w', newline='') as output_file:
    # Define the column names (field names) for the output CSV file
    fieldnames = ['gpu_id', 'gpu_vendor_name', 'gpu_brand', 'cpu_series', 
                  'gpu_processor_manufacturer', 'gpu_memory', 'gpu_memory_type']
    
    # Create a CSV writer object that writes rows as dictionaries
    writer = csv.DictWriter(output_file, fieldnames=fieldnames)
    
    # Write the header row with column names to the output file
    writer.writeheader()
    
    # Loop through the gpu_data dictionary and write each GPU entry to the CSV file
    for idx, (gpu_id, details) in enumerate(gpu_data.items()):
        # Write a row for each GPU, assigning a sequential integer 'gpu_id' as an index
        writer.writerow({
            'gpu_id': idx,  # Use the loop index as the unique GPU ID in the output file
            'gpu_vendor_name': details['gpu_vendor_name'],
            'gpu_brand': details['gpu_brand'],
            'cpu_series': details['cpu_series'],  # The 'cpu_series' is written as part of the GPU data
            'gpu_processor_manufacturer': details['gpu_processor_manufacturer'],
            'gpu_memory': details['gpu_memory'],
            'gpu_memory_type': details['gpu_memory_type']
        })

# Print a confirmation message after writing the data
print("GPU table created.")