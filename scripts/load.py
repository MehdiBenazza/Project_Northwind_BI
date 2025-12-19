import pandas as pd
import pyodbc
import os

# Répertoires
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)
PROC_DIR = os.path.join(PROJECT_DIR, "data", "processed")

# Connexion au DW
server = r'localhost\SQLEXPRESS'
database = 'DW_Northwind'

conn_str = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;TrustServerCertificate=yes;'

conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

# ============================================================
# FONCTION D'INSERTION SECURISEE
# ============================================================

def insert_rows(table, columns, df):
    placeholders = ",".join("?" * len(columns))
    colnames = ",".join(columns)
    sql = f"INSERT INTO {table} ({colnames}) VALUES ({placeholders})"
    
    for _, row in df.iterrows():
        values = [None if pd.isna(row[col]) else row[col] for col in columns]
        cursor.execute(sql, values)
    conn.commit()
    print(f" {table} chargé ({len(df)} lignes)")

# ============================================================
# CHARGEMENT DES DIMENSIONS
# ============================================================

print("\n=== Chargement des dimensions ===\n")

dim_customers = pd.read_csv(os.path.join(PROC_DIR, "DimCustomers.csv"))
insert_rows("DimCustomers", ["CustomerID", "CompanyName", "ContactName", "Country"], dim_customers)

dim_products = pd.read_csv(os.path.join(PROC_DIR, "DimProducts.csv"))
insert_rows("DimProducts", ["ProductID", "ProductName", "CategoryID", "SupplierID", "UnitPrice"], dim_products)

dim_employees = pd.read_csv(os.path.join(PROC_DIR, "DimEmployees.csv"))
insert_rows("DimEmployees", ["EmployeeID", "LastName", "FirstName", "Title", "Country"], dim_employees)

dim_suppliers = pd.read_csv(os.path.join(PROC_DIR, "DimSuppliers.csv"))
insert_rows("DimSuppliers", ["SupplierID", "CompanyName", "Country"], dim_suppliers)

dim_shippers = pd.read_csv(os.path.join(PROC_DIR, "DimShippers.csv"))
insert_rows("DimShippers", ["ShipperID", "CompanyName"], dim_shippers)

# ============================================================
# CHARGEMENT DE LA TABLE DE FAITS
# ============================================================

print("\n=== Chargement de FactSales ===\n")

fact = pd.read_csv(os.path.join(PROC_DIR, "FactSales.csv"))

# Nom correct de la colonne date
if "OrderDate_iso" in fact.columns:
    fact["OrderDate"] = fact["OrderDate_iso"]

insert_rows(
    "FactSales",
    ["OrderID", "ProductID", "CustomerID", "EmployeeID", "ShipperID", "OrderDate", "Quantity", "UnitPrice", "Discount", "TotalSales"],
    fact
)

cursor.close()
conn.close()

print("\n Chargement complet du Data Warehouse !")
