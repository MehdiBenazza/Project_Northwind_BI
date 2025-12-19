import pyodbc
import pandas as pd

def load_data(query):
    """Charge les données depuis la base de données DW_Northwind"""
    server = r'localhost\SQLEXPRESS'
    database = 'DW_Northwind'
    conn_str = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;TrustServerCertificate=yes;'
    
    try:
        conn = pyodbc.connect(conn_str)
        df = pd.read_sql(query, conn)
        conn.close()
        print("Connexion réussie. Tables trouvées :")
        return df
    except Exception as e:
        print(f"Erreur de connexion : {e}")
        return None
