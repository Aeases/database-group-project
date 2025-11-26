from db import cur, con
from utils import getUserInput, getTableColumns, getTableUserInput, escapeString

def user_add_tuple(table_choice):
    
    numOfInput = int(getUserInput("How many items would you like to insert? #"))

    print(f"\nInserting into {table_choice}\n")

    all_items = []
    
    for i in range(0, numOfInput):
        if i > 0: print(f"\nInsertion #{i+1} into {table_choice}\n")
        all_items.append(get_all_columns_in_table(table_choice))

    [add_tuple_to_sql(table_choice, column) for column in all_items]

def get_all_columns_in_table(table):
    all_columns = getTableColumns(table)
    all_items = []

    for column in all_columns:
        all_items.append(getUserInput(f"{column} <- "))
    
    return all_items

def add_tuple_to_sql(target_table, tuple):
    getTableColumns(target_table)

    escaped_values = [escapeString(t) for t in tuple]
    
    insertion_string = f"INSERT INTO {target_table} ({', '.join(getTableColumns(target_table))}) VALUES ({', '.join(escaped_values)})"
    cur.execute(insertion_string)
