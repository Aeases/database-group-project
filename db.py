import os
import sqlite3 as sql
from database_initialisations import table_definitions, table_rows

shouldCreateNew = not os.path.exists("./database.db")
con = sql.connect("database.db")

cur = con.cursor()
if shouldCreateNew:
    # Create Tables
    for table in table_definitions:
        cur.execute(table)
    con.commit()
    # Insert Rows into tables
    for new_row in table_rows:
        cur.execute(new_row)
    con.commit()
