import csv  # Import the csv module for reading and writing CSV files

# Define a dictionary mapping countries to their currencies
country_currency_map = {
    'Germany': 'EUR',  # Euro
    'Spain': 'EUR',    # Euro
    'Australia': 'AUD', # Australian Dollar
    'United Kingdom': 'GBP', # British Pound
    'Belgium': 'EUR',   # Euro
    'Canada': 'CAD',    # Canadian Dollar
    'New Zealand': 'NZD', # New Zealand Dollar
    'United States of America': 'USD', # US Dollar
    'France': 'EUR',    # Euro
    'Ireland': 'EUR',   # Euro
    'Italy': 'EUR'      # Euro
}

# Create an empty dictionary to store geography data
geography_data = {}

# Open the input file 'geography.csv' in read mode
with open('../Original data/geography.csv', 'r') as geo_file:
    # Create a CSV reader object that reads rows as dictionaries
    csv_reader = csv.DictReader(geo_file)
    
    # Loop through each row in the CSV file
    for row in csv_reader:
        # Extract the geo_id, continent, country, and region from the current row
        geo_id = int(row['geo_id'])  # Convert geo_id to an integer
        continent = row['continent']
        country = row['country']
        region = row['region']
        
        # Retrieve the currency for the current country from the dictionary.
        # If the country is not found, default to 'USD'
        currency = country_currency_map.get(country, 'USD')
        
        # Store the extracted data and currency in the geography_data dictionary
        geography_data[geo_id] = {
            'continent': continent,
            'country': country,
            'region': region,
            'currency': currency
        }

with open('../Tables CSV/geography.csv', 'w', newline='') as output_file:
    # Define the column names (field names) for the output CSV file
    fieldnames = ['geo_id', 'continent', 'country', 'region', 'currency']
    
    # Create a CSV writer object that writes rows as dictionaries
    writer = csv.DictWriter(output_file, fieldnames=fieldnames)
    
    # Write the header row with column names to the output file
    writer.writeheader()
    
    # Loop through the geography_data dictionary and write each entry to the CSV file
    for geo_id, details in geography_data.items():
        writer.writerow({
            'geo_id': geo_id,
            'continent': details['continent'],
            'country': details['country'],
            'region': details['region'],
            'currency': details['currency']
        })

# Print a confirmation message after writing the data
print("Geography table created.")