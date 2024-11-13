import streamlit as st
import pandas as pd

import psycopg2
from psycopg2 import sql
import os

# -----------------------------------------------------------------------------
# Declare some useful functions

def connect_db():
    """Connects to the PostgreSQL database hosted on Aiven."""
    
    # Configuración de conexión con datos proporcionados por Aiven
    conn = psycopg2.connect(
        dbname=os.getenv("DB_NAME"),         # nombre de la base de datos
        user=os.getenv("DB_USER"),           # usuario
        password=os.getenv("DB_PASSWORD"),   # contraseña
        host=os.getenv("DB_HOST"),           # host de Aiven
        port=os.getenv("DB_PORT")            # puerto de Aiven
    )

    # Verifica si la conexión es exitosa
    db_was_just_created = False  # Por lo general, PostgreSQL no requiere verificación del archivo de BD

    return conn, db_was_just_created

def load_data(conn):
    """Loads the inventory data from the PostgreSQL database without predefined structure."""
    cursor = conn.cursor()

    try:
        # Ejecuta la consulta para obtener todos los datos de la tabla 'inventory'
        cursor.execute("SELECT * FROM almacenaje")
        data = cursor.fetchall()
        
        # Obtiene los nombres de las columnas de la consulta
        colnames = [desc[0] for desc in cursor.description]

        # Crea el DataFrame usando los datos y los nombres de las columnas obtenidos
        df = pd.DataFrame(data, columns=colnames)

    except Exception as e:
        print(f"Error loading data: {e}")
        return None
    finally:
        cursor.close()  # Cierra el cursor después de la consulta

    return df

# -----------------------------------------------------------------------------
# Draw the actual page, starting with the inventory table.

# Set the title that appears at the top of the page.
"""
# :shopping_bags: Inventory tracker

**Welcome to Alice's Corner Store's intentory tracker!**
This page reads and writes directly from/to our inventory database.
"""

st.info(
    """
    Use the table below to add, remove, and edit items.
    And don't forget to commit your changes when you're done.
    """
)

# Load data from database
df = load_data(conn)

# -----------------------------------------------------------------------------
# Now some cool charts

# Add some space
""
""
""

st.subheader("Units left", divider="red")