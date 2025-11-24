import sqlite3 as sql

con = sql.connect("database.db")
cur = con.cursor()

table_definitions = [
    "CREATE TABLE EMPLOYEE(employee_id, e_name, e_phone, supervisor_id, level)",
    "CREATE TABLE CMM_ACTIVITY(activity_id, activity_desc, start_date, end_date, makes_unusable, category)",
    "CREATE TABLE SUBCONTRACTOR(c_id, c_name, c_phone, c_email)",
    "CREATE TABLE E_ASSIGNMENT(a_id, e_id)",
    "CREATE TABLE C_ASSIGNMENT(a_id, c_id)",
    "CREATE TABLE CAMPUS_AREA(a_id, c_id)",
    "CREATE TABLE CHEMICALS(chemical_id, chemical_name, is_harmful)",
    "CREATE TABLE CHEMICAL_USAGE(chemical_id, a_id)",
    "CREATE TABLE BUILDING_SUPERVISION(building_id, e_id)"
]

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

def getUserInput():
    print("\033[33;4m", "")
    input("")
    print("\033[0m", "")


print(getTableColumns(getTableNames()[0]))

print("Employee ID ↓ ", "");
getUserInput()

