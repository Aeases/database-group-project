import sqlite3 as sql
import os
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

def getTableNames():
    cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
    table_names = [result[0] for result in cur.fetchall()]
    return table_names

def getTableColumns(table_name):
    cur.execute(f"PRAGMA table_info({table_name})")
    table_columns = [result[1] for result in cur.fetchall()]
    return table_columns

def getUserInput(prompt: str):
    print(f"{prompt}\033[33;4m", end="")
    res = input("")
    print("\033[0m", end="")
    return res

print("Employee Table Rows: " + str(getTableColumns(getTableNames()[0])))
cur.execute("INSERT INTO EMPLOYEE (e_name, e_phone, supervisor_id, level) VALUES ('John Arbuckle', '61929507', NULL, 1)")

#employeeID = getUserInput("Employee ID: ")

