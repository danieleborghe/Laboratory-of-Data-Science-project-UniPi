import csv  # Import the csv module for reading CSV files
import pyodbc  # Import the pyodbc module for database operations
import tqdm as tq  # Import the tqdm module for progress bars

# Database connection setup
server = 'tcp:lds.di.unipi.it'  # Server address
database = 'Group_ID_480_DB'  # Database name
username = 'Group_ID_480'  # Username for database authentication
password = '779ENI6E1'  # Password for database authentication

# Connection string for SQL Server
connectionString = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'
print(f"Connecting to database '{database}' on server '{server}' with user '{username}'...")
cnxn = pyodbc.connect(connectionString)  # Establish connection to the database
cursor = cnxn.cursor()  # Create a cursor object for executing SQL commands

cursor.fast_executemany = True  # Enable fast execution for bulk inserts

print('Connection established successfully.\n')

# List of dimension tables and their corresponding CSV files
dimension_tables_and_files = [
    ('Geography', 'Tabelle/geography.csv'),  # (Table name, CSV file path)
    ('Time', 'Tabelle/Time.csv'),
    ('Cpu', 'Tabelle/CPU.csv'),
    ('Gpu', 'Tabelle/GPU.csv'),
    ('Ram', 'Tabelle/RAM.csv')
]

# Fact table and its corresponding CSV file
fact_table_and_file = ('Computer_sales', 'Tabelle/computer_sales.csv')

def check_and_create_table(table_name, headers, is_fact_table=False):
    # Check if the table already exists
    cursor.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = ?", table_name)
    table_exists = cursor.fetchone()

    if table_exists:
        print(f"Table '{table_name}' already exists. Deleting existing data...")
        # Delete all existing data from the table
        cursor.execute(f"DELETE FROM {table_name}")
        print(f"All existing data from table '{table_name}' has been deleted.")
    else:
        print(f"Table '{table_name}' does not exist. Creating it...")
        if is_fact_table:
            # SQL query to create a fact table with foreign key constraints
            create_table_query = f"""
            CREATE TABLE {table_name} (
                sale_id INT PRIMARY KEY,
                geo_id INT,
                time_id INT,
                ram_id INT,
                cpu_id INT,
                gpu_id INT,
                ram_sales FLOAT,
                ram_sales_usd FLOAT,
                cpu_sales FLOAT,
                cpu_sales_usd FLOAT,
                gpu_sales FLOAT,
                gpu_sales_usd FLOAT,
                total_sales FLOAT,
                total_sales_usd FLOAT,
                FOREIGN KEY (geo_id) REFERENCES Geography(geo_id),
                FOREIGN KEY (time_id) REFERENCES Time(time_id),
                FOREIGN KEY (ram_id) REFERENCES Ram(ram_id),
                FOREIGN KEY (cpu_id) REFERENCES Cpu(cpu_id),
                FOREIGN KEY (gpu_id) REFERENCES Gpu(gpu_id)
            )
            """
        else:
            # SQL queries to create dimension tables
            create_table_query = {
                'Cpu': """
                CREATE TABLE Cpu (
                    cpu_id INT PRIMARY KEY,
                    cpu_vendor_name VARCHAR(255),
                    cpu_brand VARCHAR(255),
                    cpu_series VARCHAR(255),
                    cpu_name VARCHAR(255),
                    cpu_n_cores INT,
                    cpu_socket VARCHAR(255)
                )
                """,
                'Gpu': """
                CREATE TABLE Gpu (
                    gpu_id INT PRIMARY KEY,
                    gpu_vendor_name VARCHAR(255),
                    gpu_brand VARCHAR(255),
                    cpu_series VARCHAR(255),
                    gpu_processor_manufacturer VARCHAR(255),
                    gpu_memory FLOAT,
                    gpu_memory_type VARCHAR(255)
                )
                """,
                'Ram': """
                CREATE TABLE Ram (
                    ram_id INT PRIMARY KEY,
                    ram_vendor_name VARCHAR(255),
                    ram_brand VARCHAR(255),
                    ram_name VARCHAR(255),
                    ram_type VARCHAR(255),
                    ram_size FLOAT,
                    ram_clock FLOAT
                )
                """,
                'Time': """
                CREATE TABLE Time (
                    time_id INT PRIMARY KEY,
                    day INT,
                    month INT,
                    year INT,
                    day_of_week VARCHAR(255),
                    week INT,
                    quarter VARCHAR(255)
                )
                """,
                'Geography': """
                CREATE TABLE Geography (
                    geo_id INT PRIMARY KEY,
                    continent VARCHAR(255),
                    country VARCHAR(255),
                    region VARCHAR(255),
                    currency VARCHAR(255)
                )
                """
            }[table_name]
        
        print(f"Executing Create Table Query: {create_table_query}")
        cursor.execute(create_table_query)  # Execute the SQL query to create the table
        print(f"Table '{table_name}' created successfully.")

def populate_table(table_name, file_name, batch_size=1000):
    print(f"\nProcessing table '{table_name}' with file '{file_name}'...")
    with open(file_name, 'r') as file:
        reader = csv.reader(file, delimiter=',')  # Read the CSV file
        headers = next(reader)  # Extract CSV headers
        print(f"CSV headers: {headers}")

        # Check if the table exists and create it if necessary
        is_fact_table = (table_name == fact_table_and_file[0])
        check_and_create_table(table_name, headers, is_fact_table)

        # Prepare the SQL insert query dynamically
        columns = ", ".join(headers)  # List of column names
        placeholders = ", ".join(['?'] * len(headers))  # Placeholder for each column value
        insert_query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        print(f"Prepared SQL Insert Query: {insert_query}")

        # Execute batch insertion of the CSV data
        batch = []  # List to hold rows for batch processing
        row_count = 0  # Counter for the number of rows processed
        with tq.tqdm(desc=f'Loading {table_name}') as pbar:
            for row in reader:
                batch.append(row)  # Add the row to the batch
                row_count += 1

                # Insert the batch when it reaches the specified batch size
                if len(batch) >= batch_size:
                    cursor.executemany(insert_query, batch)  # Execute batch insert
                    cnxn.commit()  # Commit the transaction
                    pbar.update(len(batch))  # Update the progress bar
                    batch = []  # Clear the batch

            # Insert any remaining rows in the final batch
            if batch:
                cursor.executemany(insert_query, batch)
                cnxn.commit()
                pbar.update(len(batch))

        print(f"All rows inserted for table '{table_name}'.")

# Populate dimension tables first
for table_name, file_name in dimension_tables_and_files:
    populate_table(table_name, file_name)  # Process each dimension table

# Populate the fact table last
populate_table(*fact_table_and_file)  # Process the fact table

# Close the database connection
print("\nClosing the database connection...")
cnxn.close()
print('Data loading completed successfully!')