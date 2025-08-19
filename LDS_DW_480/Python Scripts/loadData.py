import csv  # Import the CSV module to read and process CSV files
import pyodbc  # Import the pyodbc module for database connectivity
import tqdm as tq  # Import tqdm for progress bars

# Database connection setup
server = 'tcp:lds.di.unipi.it'
database = 'Group_ID_480_DB'
username = 'Group_ID_480'
password = '779ENI6E1'

# Creating a connection string with placeholders for driver, server, database, and user credentials
connectionString = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'

# Print message indicating the attempt to connect to the database
print(f"Connecting to database '{database}' on server '{server}' with user '{username}'...")

# Establish a connection to the database using the connection string
cnxn = pyodbc.connect(connectionString)
cursor = cnxn.cursor()  # Create a cursor object to execute SQL queries

# Enable fast executemany for faster bulk insertions into the database
cursor.fast_executemany = True

# Confirm successful connection
print('Connection established successfully.\n')

# List of dimension tables and corresponding CSV files
dimension_tables_and_files = [
    ('Geography', '../Tables CSV/geography.csv'),
    ('Time', '../Tables CSV/Time.csv'),
    ('Cpu', '../Tables CSV/CPU.csv'),
    ('Gpu', '../Tables CSV/GPU.csv'),
    ('Ram', '../Tables CSV/RAM.csv')
]

# Fact table and corresponding CSV file
fact_table_and_file = ('Computer_sales', '../Tables CSV/computer_sales.csv')

# Batch size for bulk inserts
BATCH_SIZE = 1000

# Function to check if a table exists and create it if it doesn't
def check_and_create_table(table_name, headers, is_fact_table=False):
    # Check if the table exists in the database by querying the information schema
    cursor.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = ?", table_name)
    table_exists = cursor.fetchone()  # Fetch the result (None if the table doesn't exist)

    if not table_exists:  # If the table doesn't exist
        print(f"Table '{table_name}' does not exist. Creating it...")

        if is_fact_table:  # If the table is the fact table, create it with foreign keys
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
        else:  # If the table is a dimension table, create it based on the table name
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
        
        # Execute the create table query
        print(f"Executing Create Table Query: {create_table_query}")
        cursor.execute(create_table_query)
        print(f"Table '{table_name}' created successfully.")
    else:  # If the table already exists
        print(f"Table '{table_name}' already exists. Proceeding to populate it...")

# Function to populate a table with data from a CSV file using batch loading
def populate_table(table_name, file_name):
    print(f"\nProcessing table '{table_name}' with file '{file_name}'...")

    # Open the CSV file
    with open(file_name, 'r') as file:
        reader = csv.reader(file, delimiter=',')  # Create a CSV reader object
        headers = next(reader)  # Read the header row (column names)
        print(f"CSV headers: {headers}")

        # Check if the table exists and create it if necessary
        is_fact_table = (table_name == fact_table_and_file[0])
        check_and_create_table(table_name, headers, is_fact_table)

        # Prepare the SQL insert query dynamically based on the headers
        columns = ", ".join(headers)
        placeholders = ", ".join(['?'] * len(headers))  # '?' placeholders for parameterized query
        insert_query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        print(f"Prepared SQL Insert Query: {insert_query}")

        rows = []  # Initialize an empty list to hold rows for batch insertion
        row_count = 0  # Counter for total rows

        # Display a progress bar during the loading process
        with tq.tqdm(desc=f'Loading {table_name}', unit='rows') as pbar:
            for row in reader:
                rows.append(row)
                row_count += 1

                # If the batch size is reached, insert the batch into the database
                if len(rows) == BATCH_SIZE:
                    cursor.executemany(insert_query, rows)
                    pbar.update(len(rows))  # Update progress bar
                    rows.clear()  # Clear the batch list after insertion

            # Insert any remaining rows that didn't complete a full batch
            if rows:
                cursor.executemany(insert_query, rows)
                pbar.update(len(rows))

        # Commit the transaction to save the inserted data
        print(f"Committing the transactions for table '{table_name}'...")
        cnxn.commit()
        print(f"{row_count} rows inserted into '{table_name}' successfully.")

try:
    # Populate dimension tables first
    for table_name, file_name in dimension_tables_and_files:
        populate_table(table_name, file_name)

    # Populate the fact table after dimension tables
    populate_table(*fact_table_and_file)

finally:
    # Ensure cursor and connection are closed even if an error occurs
    print("\nClosing the cursor and database connection...")
    cursor.close()  # Explicitly close the cursor
    cnxn.close()  # Close the database connection
    print('Data loading completed successfully!')