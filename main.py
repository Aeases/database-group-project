import sqlite3 as sql
import os
from database_initialisations import table_definitions, employee_definitions

shouldCreateNew = not os.path.exists("./database.db")
con = sql.connect("database.db")

cur = con.cursor()
if shouldCreateNew:
    for table in table_definitions:
        cur.execute(table) 

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

#employeeID = getUserInput("Employee ID: ")

