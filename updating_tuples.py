from db import cur, con
from utils import getUserPrimaryColumns, getUserBinaryInput, searchForRecord, escapeString, getTableUserInput, getTableColumns, getUserInput, searchPkToWhereClause

def user_delete_tuple(table_choice):
    print("Type in the primary keys of the table you want to delete below:")
    search_primary_keys = getUserPrimaryColumns(table_choice)
    table_columns = getTableColumns(table_choice)

    record_values = searchForRecord(table_choice, search_primary_keys)
    print("\nDelete this record: (Y/N)")
    for i in range(0, len(table_columns)):
        print(f"    {table_columns[i]} : {record_values[i]}")
    print("\n")
    where_clause = searchPkToWhereClause(table_choice, search_primary_keys)
    if (getUserBinaryInput("> ")):
        con.execute(f'DELETE FROM {table_choice} WHERE {where_clause}')
    

def user_update_tuple(table_choice):

    print("\nType in the primary keys of the relation to find below:")
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
    con.execute(f"UPDATE {table} SET {set_clause} WHERE {where_clause}")

def perform_deletion(table, search_primary_keys):
    where_clause = searchPkToWhereClause(table, search_primary_keys)
    con.execute(f"DELETE FROM {table} WHERE {where_clause}")
