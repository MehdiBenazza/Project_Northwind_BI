import pyodbc
import pandas as pd
import os
import sys

# Répertoires (chemins absolus par rapport au projet)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)
output_dir = os.path.join(PROJECT_DIR, 'data', 'raw')
os.makedirs(output_dir, exist_ok=True)

# Connexion
server = r'localhost\\SQLEXPRESS'
database = 'Northwind'

# Choisir automatiquement un driver ODBC disponible
preferred = ['ODBC Driver 18 for SQL Server', 'ODBC Driver 17 for SQL Server', 'SQL Server']
available = pyodbc.drivers()
conn = None
last_err = None
for drv in preferred:
    if drv in available:
        conn_str = f"DRIVER={{{drv}}};SERVER=(local)\\SQLEXPRESS;DATABASE={database};Trusted_Connection=yes;TrustServerCertificate=yes;"
        try:
            conn = pyodbc.connect(conn_str)
            print(f'Connexion OK avec le driver: {drv}')
            break
        except Exception as e:
            print(f'Pilote {drv} trouvé mais connexion échouée: {e}')
            last_err = e

if conn is None:
    # Essayer avec tous les drivers disponibles si les préférés ont échoué
    for drv in available:
        conn_str = f"DRIVER={{{drv}}};SERVER=(local)\\SQLEXPRESS;DATABASE={database};Trusted_Connection=yes;TrustServerCertificate=yes;"
        try:
            conn = pyodbc.connect(conn_str)
            print(f'Connexion OK avec le driver: {drv}')
            break
        except Exception as e:
            print(f'Pilote {drv} testé, erreur: {e}')
            last_err = e

if conn is None:
    print('Aucun driver n’a permis de se connecter. Dernière erreur :', last_err)
    raise last_err

# Tables à extraire
tables = [
    "Customers",
    "Employees",
    "Suppliers",
    "Categories",
    "Products",
    "Shippers",
    "Orders",
    "[Order Details]"
]

for table in tables:
    print(f"Début extraction : {table}")
    sys.stdout.flush()
    try:
        query = f"SELECT * FROM {table}"
        df = pd.read_sql(query, conn)

        filename = table.replace(" ", "_").replace("[", "").replace("]", "") + ".csv"
        outpath = os.path.join(output_dir, filename)
        # Sauvegarde avec séparateur point-virgule pour compatibilité locale
        df.to_csv(outpath, index=False, sep=';')

        print(f" OK — {table} exportée vers {filename} ({len(df)} lignes)")
    except Exception as e:
        print(f" ERREUR — extraction de {table} échouée : {e}")
    finally:
        sys.stdout.flush()

conn.close()
print("\nExtraction terminée avec succès !")
