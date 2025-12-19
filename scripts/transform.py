import pandas as pd
import os

# Obtenir le répertoire parent du script (racine du projet)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)

RAW_DIR = os.path.join(PROJECT_DIR, "data", "raw")
PROC_DIR = os.path.join(PROJECT_DIR, "data", "processed")
os.makedirs(PROC_DIR, exist_ok=True)

# Chargement CSV (avec séparateur point-virgule)
customers = pd.read_csv(os.path.join(RAW_DIR, "Customers.csv"), sep=';')
employees = pd.read_csv(os.path.join(RAW_DIR, "Employees.csv"), sep=';')
suppliers = pd.read_csv(os.path.join(RAW_DIR, "Suppliers.csv"), sep=';')
categories = pd.read_csv(os.path.join(RAW_DIR, "Categories.csv"), sep=';')
products = pd.read_csv(os.path.join(RAW_DIR, "Products.csv"), sep=';')
shippers = pd.read_csv(os.path.join(RAW_DIR, "Shippers.csv"), sep=';')
orders = pd.read_csv(os.path.join(RAW_DIR, "Orders.csv"), sep=';')
order_details = pd.read_csv(os.path.join(RAW_DIR, "Order_Details.csv"), sep=';')

# --- Nettoyage / harmonisation de base ---
# Renommer colonnes si nécessaire
order_details.columns = [c.replace(" ", "_").replace("(", "").replace(")", "") for c in order_details.columns]
orders.columns = [c.replace(" ", "_").replace("(", "").replace(")", "") for c in orders.columns]
products.columns = [c.replace(" ", "_").replace("(", "").replace(")", "") for c in products.columns]

# S'assurer des types
orders['OrderDate'] = pd.to_datetime(orders['OrderDate'], errors='coerce')

# Calculer TotalPrice dans order_details (si UnitPrice & Quantity existent)
if {'UnitPrice','Quantity'}.issubset(order_details.columns):
    order_details['TotalPrice'] = order_details['UnitPrice'] * order_details['Quantity'] * (1 - order_details.get('Discount', 0).fillna(0))
else:
    order_details['TotalPrice'] = None

# Ajouter Year/Month/Day à orders
orders['Year'] = orders['OrderDate'].dt.year
orders['Month'] = orders['OrderDate'].dt.month
orders['Day'] = orders['OrderDate'].dt.day
orders['OrderDate_iso'] = orders['OrderDate'].dt.date

# Construire la table FactSales en joignant orders + order_details + products (pour UnitPrice si besoin)
fact = order_details.merge(orders, how='left', left_on='OrderID', right_on='OrderID', suffixes=('_detail','_order'))
fact = fact.merge(products[['ProductID','ProductName','CategoryID','SupplierID']], how='left', left_on='ProductID', right_on='ProductID')

# Normaliser champs clés
fact['CustomerID'] = fact['CustomerID'].astype(str)
fact['ProductID'] = fact['ProductID'].astype(int)
fact['EmployeeID'] = pd.to_numeric(fact['EmployeeID'], errors='coerce').fillna(0).astype(int)
# Renommer ShipVia en ShipperID s'il existe
if 'ShipVia' in fact.columns:
    fact['ShipperID'] = pd.to_numeric(fact['ShipVia'], errors='coerce').fillna(0).astype(int)
elif 'ShipperID' in fact.columns:
    fact['ShipperID'] = pd.to_numeric(fact['ShipperID'], errors='coerce').fillna(0).astype(int)

# Calculs KPI supplémentaires
fact['TotalSales'] = fact['TotalPrice'].fillna(fact.get('UnitPrice',0) * fact.get('Quantity',0))

# Sauvegarde des tables transformées
customers.to_csv(os.path.join(PROC_DIR, "DimCustomers.csv"), index=False)
products.to_csv(os.path.join(PROC_DIR, "DimProducts.csv"), index=False)
employees.to_csv(os.path.join(PROC_DIR, "DimEmployees.csv"), index=False)
suppliers.to_csv(os.path.join(PROC_DIR, "DimSuppliers.csv"), index=False)
shippers.to_csv(os.path.join(PROC_DIR, "DimShippers.csv"), index=False)
categories.to_csv(os.path.join(PROC_DIR, "DimCategories.csv"), index=False)
orders.to_csv(os.path.join(PROC_DIR, "Orders_prepared.csv"), index=False)
fact.to_csv(os.path.join(PROC_DIR, "FactSales.csv"), index=False)

print("Transformation terminée. Fichiers dans data/processed/")
