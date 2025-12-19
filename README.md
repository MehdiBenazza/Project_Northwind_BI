# Northwind Data Warehouse & Business Intelligence Project

## Academic Context
This project was developed as part of a **Business Intelligence / Data Warehousing** academic module.  
Its objective is to design, implement, and analyze a **Data Warehouse (DW)** built from the transactional **Northwind** database, and to visualize business insights **without using proprietary BI tools such as Power BI**.

The project covers the **full BI lifecycle**, from data modeling to decision-oriented reporting.

---

## Project Objectives
- Design a decision-oriented **Data Warehouse**
- Transform operational data into analytical data
- Build a **Star Schema** (Fact & Dimension tables)
- Compute and analyze **Key Performance Indicators (KPIs)**
- Visualize results using **Python and Streamlit**
- Justify architectural and technological choices

---

## Global Architecture

Northwind (OLTP Database)
│
▼
ETL Process (SQL)
│
▼
DW_Northwind (Data Warehouse)
│
▼
Python + Streamlit (Analytics & Reporting)


---

## Data Sources
- Primary data source: **Northwind Database**
- DBMS: **Microsoft SQL Server**
- Main operational tables:
  - Customers
  - Orders
  - Order Details
  - Products
  - Employees
  - Suppliers
  - Shippers
  - Categories

Although only one database is used, the project integrates **multiple heterogeneous tables** with different granularities, which is sufficient for BI learning objectives.

---

## Data Warehouse Modeling

### Star Schema Design

#### Fact Table
**FactSales**
- FactID
- OrderID
- ProductID
- CustomerID
- EmployeeID
- ShipperID
- OrderDate
- Quantity
- UnitPrice
- Discount
- TotalSales

This table stores measurable business events (sales).

---

#### Dimension Tables
- **DimCustomers**
- **DimProducts**
- **DimEmployees**
- **DimSuppliers**
- **DimShippers**

This design allows:
- Fast analytical queries
- Clear separation between facts and descriptive attributes
- Easy KPI computation

---

## ETL Process (Extract – Transform – Load)

### 1 Extraction
Data is extracted from the **Northwind OLTP database** using SQL queries.

### 2️ Transformation
- Data type conversion
- Data cleaning
- Calculation of business metrics (e.g., `TotalSales`)
- Key mapping between fact and dimension tables

### 3️ Loading
- Dimensions are populated first
- The fact table `FactSales` is loaded afterward

 Data volume after loading:
- Orders: **830 rows**
- Order Details: **2155 rows**
- FactSales: **2155 rows**

---

## Key Performance Indicators (KPIs)

### Global KPIs
- Total Revenue
- Total Quantity Sold
- Total Number of Orders

### Analytical Indicators
- Top-selling products
- Sales by country
- Sales by employee
- Sales by product category

These indicators support **strategic and operational decision-making**.

---

## Data Visualization with Python & Streamlit

### Why Streamlit?
- Open-source
- Lightweight and fast to deploy
- No dependency on proprietary BI tools
- Suitable for academic and professional BI projects

### Technologies Used
- Python
- Streamlit
- Pandas
- Matplotlib / Seaborn
- pyodbc
- Microsoft SQL Server

---

## How to Run the Application

### 1️ Install dependencies
```bash
pip install streamlit pandas pyodbc matplotlib seaborn
```
### 2 Run the Streamlit app
```bash
python -m streamlit run scripts/app.py
```

