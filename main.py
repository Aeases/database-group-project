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
# cur.execute("INSERT INTO EMPLOYEE (e_name, e_phone, supervisor_id, level) VALUES ('John Arbuckle', '61929507', NULL, 1)")

#employeeID = getUserInput("Employee ID: ")

def user_add_tuple():
    table_names = getTableNames()

    print(table_names)
    table_choice = getUserInput("Table: ")

    while table_choice not in table_names:
        print("Table not in tables");
        table_choice = getUserInput("Table: ")
    
    numOfInput = int(getUserInput("How many items would you like to insert? #"))

    print(f"\nInserting into {table_choice}\n")

    all_items = []
    
    for i in range(0, numOfInput):
        if i > 0: print(f"\nInsertion #{i+1} into {table_choice}\n")
        all_items.append(get_all_items_in_table(table_choice))



    [add_tuple_to_sql(table_choice, column) for column in all_items]
    # print(all_items)

def get_all_items_in_table(table):
    all_columns = getTableColumns(table)
    all_items = []

    for column in all_columns:
        all_items.append(getUserInput(f"{column} <- "))
    
    return all_items

def add_tuple_to_sql(target_table, tuple):
    getTableColumns(target_table)
    escaped_strings = []

    for item in tuple:
        if type(item) is int:
            escaped_strings.append(item)
        if type(item) is str:
            escaped_strings.append(f"'{item}'")
    
    insertion_string = f"INSERT INTO {target_table} ({", ".join(getTableColumns(target_table))}) VALUES ({", ".join(escaped_strings)})"
    cur.execute(insertion_string)
    print(insertion_string)
    con.commit()


user_add_tuple()