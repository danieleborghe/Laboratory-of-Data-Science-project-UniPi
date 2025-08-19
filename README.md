# Business Intelligence for Computer Sales Analysis

This repository contains an end-to-end Business Intelligence (BI) project designed to analyze computer sales data. The project implements a full BI pipeline, including data generation, an ETL process, the construction of a Data Warehouse and an OLAP Data Cube, and the creation of an interactive dashboard for data exploration and decision-making.

This project was developed for the "Laboratory of Data Science" course at the **University of Pisa (UniPi)**.

[![Read the Report (Italian)](https://img.shields.io/badge/Read_the_Full-Report-red?style=for-the-badge&logo=adobeacrobatreader)](Group%20ID%20480%20Report.pdf)

---

## 📝 Table of Contents

- [Project Goal: From Raw Data to Actionable Insights](#-project-goal-from-raw-data-to-actionable-insights)
- [Methodology: A Classic Business Intelligence Pipeline](#-methodology-a-classic-business-intelligence-pipeline)
- [Technical Stack & Architecture](#-technical-stack--architecture)
- [Dataset: Simulated Computer Sales Data](#-dataset-simulated-computer-sales-data)
- [Project Workflow & Components](#-project-workflow--components)
- [Key Analyses & Dashboard Features](#-key-analyses--dashboard-features)
- [Repository Structure](#-repository-structure)
- [How to Run This Project](#-how-to-run-this-project)
- [Authors](#-authors)

---

## 🎯 Project Goal: From Raw Data to Actionable Insights

In today's market, understanding sales trends is crucial for any business. This project aims to build a robust BI system to help a fictional computer hardware company analyze its sales performance. The central question we address is: **"How can we transform raw, transactional sales data into a structured, multidimensional format that enables managers to easily explore trends, identify top-performing products, and make data-driven strategic decisions?"**

Our goal is to create a system that allows for fast, interactive analysis of sales across different dimensions like product components (CPU, GPU, RAM), geography, and time.

---

## 💡 Methodology: A Classic Business Intelligence Pipeline

The project is built around a traditional, yet powerful, Business Intelligence architecture. This multi-stage process ensures that data is cleaned, structured, and aggregated efficiently for analysis.

1.  **Data Generation & Staging**: Raw data is programmatically generated and loaded into a staging database.
2.  **ETL (Extract, Transform, Load)**: An automated ETL process extracts data from the source, cleans and transforms it, and loads it into a structured Data Warehouse.
3.  **Data Warehousing**: The data is stored in a dimensional model (Star Schema) optimized for analytical queries.
4.  **OLAP Cube**: A multidimensional cube is built on top of the warehouse to provide pre-aggregated data and enable rapid, complex queries (slicing, dicing, drilling down).
5.  **Dashboarding & Visualization**: An interactive dashboard provides a user-friendly interface for non-technical users to explore the data and uncover insights.

---

## 💻 Technical Stack & Architecture

This project utilizes the **Microsoft BI Stack** alongside Python for data generation, providing a complete solution from data creation to visualization.

-   **Data Generation**: **Python** (`pandas`, `numpy`, `Faker`) is used to create a realistic, synthetic dataset of computer sales.
-   **Database**: **Microsoft SQL Server** serves as the relational database for both the source data and the final Data Warehouse.
-   **ETL Tool**: **SQL Server Integration Services (SSIS)** is used to design and execute the ETL workflow that populates the Data Warehouse from the source database.
-   **Data Cube (OLAP)**: **SQL Server Analysis Services (SSAS)** is used to build the multidimensional OLAP cube based on the star schema of the Data Warehouse.
-   **Query Language**: **MDX (Multidimensional Expressions)** is used to write queries against the SSAS cube to perform complex analytical calculations.
-   **Dashboarding Tool**: **Microsoft Power BI** is used to connect to the SSAS cube and create an interactive, visually rich dashboard.

---

## 📊 Dataset: Simulated Computer Sales Data

The data for this project is synthetically generated to simulate the sales records of a computer retailer. The core of the dataset is a **fact table** (`Computer_Sales`) containing transactional information. This table is linked to several **dimension tables**:

-   **`Time`**: Provides a temporal hierarchy (year, month, day).
-   **`Geography`**: Contains location data for sales (continent, country, city).
-   **`Cpu`**: Details about the computer's processor (brand, model, clock speed).
-   **`Gpu`**: Details about the graphics card (brand, model, memory).
-   **`Ram`**: Details about the system memory (brand, model, size).

This structure forms a **Star Schema**, which is ideal for BI and data warehousing applications.

---

## ⚙️ Project Workflow & Components

The project is divided into three main parts, each corresponding to a stage in the BI pipeline.

1.  **Data Warehouse Creation (`LDS_DW_480`)**:
    -   A series of **Python scripts** are used to generate synthetic data for each dimension and the fact table.
    -   Another script loads this data into a source database (`LDS_480_DB`) on SQL Server.
    -   The target Data Warehouse (`LDS_480_DW`) is also created with the star schema structure.

2.  **ETL Process (`LDS_ETL_480`)**:
    -   An **SSIS project** (`ETL process Group 480 Solution`) contains the ETL package.
    -   The package extracts data from the source database, performs necessary transformations (e.g., data type conversions, lookups for foreign keys), and loads it into the dimension and fact tables of the Data Warehouse.

3.  **Data Cube & Dashboard (`LDS_DC_480`)**:
    -   An **SSAS project** (`Data Cube`) defines the dimensions, measure groups, and the OLAP cube itself, connecting to the Data Warehouse as its source.
    -   A set of **MDX queries** are provided to demonstrate how to perform analytical queries on the cube (e.g., finding the top 5 best-selling CPUs).
    -   A **Power BI Dashboard** (`Dashboard.pbix`) connects directly to the deployed SSAS cube, allowing for interactive visualization of the sales data.

---

## 📈 Key Analyses & Dashboard Features

The final Power BI dashboard allows users to interactively explore the sales data and answer critical business questions, such as:

-   What are the total sales over time, and can we identify any seasonal trends?
-   Which CPU, GPU, and RAM models are the top sellers?
-   What is the geographical distribution of our sales? Which countries or cities are our biggest markets?
-   How does the choice of one component (e.g., an Intel CPU) affect the sales of another component (e.g., an NVIDIA GPU)?

---

## 📂 Repository Structure

```

.
├── LDS\_DW\_480/
│   ├── Python Scripts/       \# Scripts to generate and load source data
│   └── Tables CSV/           \# The generated data in CSV format
├── LDS\_ETL\_480/
│   └── ETL process Group 480 Solution/ \# The SSIS project for the ETL process
├── LDS\_DC\_480/
│   ├── Data Cube/            \# The SSAS project for the OLAP Cube
│   ├── MDX Queries/          \# Example MDX queries
│   └── Dashboard Power BI/   \# The Power BI dashboard file
├── Group ID 480 Report.pdf     \# The final, detailed project report
└── README.md                   \# This file

```

---

## 🚀 How to Run This Project

To set up and run this project, you will need the Microsoft BI suite (SQL Server, SSIS, SSAS) and Microsoft Power BI Desktop.

1.  **Set up the Database**:
    -   Run the Python scripts in `LDS_DW_480/Python Scripts/` to generate the data and load it into a source SQL Server database. Ensure you have created the target Data Warehouse schema as well.
    -   Update the connection strings in the Python scripts to point to your SQL Server instance.

2.  **Run the ETL Process**:
    -   Open the `ETL process group 480 Solution.sln` file in Visual Studio with the SSIS extension installed.
    -   Configure the database connections in the SSIS package to point to your source and destination databases.
    -   Execute the SSIS package (`Package.dtsx`) to populate the Data Warehouse.

3.  **Deploy the Data Cube**:
    -   Open the `lds480_cube.sln` file in Visual Studio with the SSAS extension installed.
    -   Configure the data source to connect to your Data Warehouse.
    -   Deploy the cube to your SSAS instance.

4.  **View the Dashboard**:
    -   Open the `Dashboard.pbix` file in Power BI Desktop.
    -   Connect the dashboard to your deployed SSAS cube to view the interactive visualizations.

---

## 👥 Authors

- **Daniele Borghesi**
- **Francesco Pio Capoccello**
