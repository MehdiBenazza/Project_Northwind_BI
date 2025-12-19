import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from db import load_data

st.set_page_config(page_title="Northwind BI Dashboard", layout="wide")

st.title("Tableau de Bord Décisionnel – Northwind")

# =======================
# KPI GÉNÉRAUX
# =======================
kpi_query = """
SELECT
    SUM(TotalSales) AS TotalRevenue,
    SUM(Quantity) AS TotalQuantity,
    COUNT(DISTINCT OrderID) AS TotalOrders
FROM FactSales
"""
kpi = load_data(kpi_query)

if kpi is not None and not kpi.empty:
    col1, col2, col3 = st.columns(3)
    col1.metric("Revenue", f"{kpi['TotalRevenue'].iloc[0]:,.2f}")
    col2.metric("Quantity", int(kpi['TotalQuantity'].iloc[0]))
    col3.metric("Orders", int(kpi['TotalOrders'].iloc[0]))

st.divider()

# =======================
# TOP PRODUITS
# =======================
st.subheader("Top 10 Products")

query_top_products = """
SELECT TOP 10
    p.ProductName,
    SUM(f.TotalSales) AS Sales
FROM FactSales f
JOIN DimProducts p ON f.ProductID = p.ProductID
GROUP BY p.ProductName
ORDER BY Sales DESC
"""
df_products = load_data(query_top_products)

if df_products is not None and not df_products.empty:
    fig, ax = plt.subplots(figsize=(10, 6))
    df_sorted = df_products.sort_values('Sales')
    ax.barh(df_sorted['ProductName'], df_sorted['Sales'], color='steelblue')
    ax.set_xlabel("Sales (€)")
    ax.set_ylabel("Product")
    st.pyplot(fig)
else:
    st.warning("No data available")
# =======================
# VENTES PAR PAYS
# =======================
st.subheader("Sales by Country")

query_country = """
SELECT
    c.Country,
    SUM(f.TotalSales) AS Sales
FROM FactSales f
JOIN DimCustomers c ON f.CustomerID = c.CustomerID
GROUP BY c.Country
ORDER BY Sales DESC
"""
df_country = load_data(query_country)

if df_country is not None and not df_country.empty:
    fig, ax = plt.subplots(figsize=(10, 8))
    df_sorted = df_country.sort_values('Sales')
    ax.barh(df_sorted['Country'], df_sorted['Sales'], color='coral')
    ax.set_xlabel("Sales (€)")
    st.pyplot(fig)
else:
    st.warning("No data available")

# =======================
# PERFORMANCE EMPLOYÉS
# =======================
st.subheader("Sales by Employee")

query_employee = """
SELECT
    CONCAT(e.FirstName, ' ', e.LastName) AS EmployeeName,
    SUM(f.TotalSales) AS Sales
FROM FactSales f
JOIN DimEmployees e ON f.EmployeeID = e.EmployeeID
GROUP BY CONCAT(e.FirstName, ' ', e.LastName)
ORDER BY Sales DESC
"""
df_emp = load_data(query_employee)

if df_emp is not None and not df_emp.empty:
    fig, ax = plt.subplots(figsize=(10, 6))
    df_sorted = df_emp.sort_values('Sales')
    ax.barh(df_sorted['EmployeeName'], df_sorted['Sales'], color='lightgreen')
    ax.set_xlabel("Sales (€)")
    ax.set_ylabel("Employee")
    st.pyplot(fig)
else:
    st.warning("No data available")
# =======================
# VENTES PAR CATÉGORIE
# =======================
st.subheader("Sales by Category")
query_category = """
SELECT
    c.CategoryName,
    SUM(f.TotalSales) AS Sales
FROM FactSales f
JOIN DimProducts p ON f.ProductID = p.ProductID
JOIN Categories c ON p.CategoryID = c.CategoryID
GROUP BY c.CategoryName
ORDER BY Sales DESC
"""
df_cat = load_data(query_category)

if df_cat is not None and not df_cat.empty:
    fig, ax = plt.subplots(figsize=(10, 6))
    df_sorted = df_cat.sort_values('Sales')
    ax.barh(df_sorted['CategoryName'], df_sorted['Sales'], color='gold')
    ax.set_xlabel("Sales (€)")
    ax.set_ylabel("Category")
    st.pyplot(fig)
else:
    st.warning("No data available")