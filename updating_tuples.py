from db import cur, con
from utils import getUserPrimaryColumns, searchForRecord, escapeString, getTableUserInput, getTableColumns, getUserInput, searchPkToWhereClause

def update_tuple():
    table_choice = getTableUserInput("Table to update: ")

    print("\nType in the primary keys of the relation to find below")
    search_primary_keys = getUserPrimaryColumns(table_choice)

    # Search for the record's values, and get the column names
    record_values = searchForRecord(table_choice, search_primary_keys)
    table_columns = getTableColumns(table_choice)


    print("\nLeave blank for columns you do not wish to overwrite\n")

    updated_values = []
    for i in range(0, len(table_columns)):
        updated_values.append(getUserInput(f"{table_columns[i]} ({record_values[i]}) <- "))
    
    perform_update(table_choice, search_primary_keys, updated_values)
    return updated_values

def perform_update(table, search_primary_keys, updated_values):
    table_columns = getTableColumns(table)

    if len(updated_values) != len(table_columns):
        print("bad happened")
    
    set_clause = []
    for i, key in enumerate(updated_values):
        if key != '':
            set_clause.append(f'{table_columns[i]} = {escapeString(updated_values[i])}')
    if len(set_clause) > 1:
        set_clause = ', '.join(set_clause)
    else:
        set_clause = set_clause[0]
    
    where_clause = searchPkToWhereClause(table, search_primary_keys)
    print(f"UPDATE {table} SET {set_clause} WHERE {where_clause}")
    con.execute(f"UPDATE {table} SET {set_clause} WHERE {where_clause}")





update_tuple()
con.commit()