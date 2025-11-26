from db import cur, con

def getTableNames():
    cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
    table_names = [result[0] for result in cur.fetchall()]
    return table_names

def getTableColumns(table_name):
    cur.execute(f"PRAGMA table_info({table_name})")
    table_columns = [result[1] for result in cur.fetchall()]
    return table_columns

def getTablePrimaryColumns(table_name):
    cur.execute(f"SELECT name FROM pragma_table_info('{table_name}') WHERE pk > 0")
    table_columns = [result[0] for result in cur.fetchall()]
    return table_columns

def getUserPrimaryColumns(table):
    primary_columns = getTablePrimaryColumns(table)

    search_primary_columns = []
    for key in primary_columns:
        search_primary_columns.append(getUserInput(f"{key} : "))

    return search_primary_columns


# Takes in array of primary keys e.g. for EMPLOYEE, [employee_id],
# or for ACTIVITY_LOCATIONS, [location_id, a_id]
def searchPkToWhereClause(table, search_primary_keys,):
    primary_keys = getTablePrimaryColumns(table)
    where_clause = ''
    if (search_primary_keys.__len__() > 1):
        where_clause = ' AND '.join(
            [f'{primary_keys[i]} = {search_primary_keys[i]}' for i in range(0, search_primary_keys.__len__())]
        )
    else:
        where_clause = f'{primary_keys[0]} = {search_primary_keys[0]}'
    return where_clause

def searchForRecord(table, search_primary_keys):
    where_clause = searchPkToWhereClause(table, search_primary_keys)
    cur.execute(f'SELECT * FROM {table} WHERE {where_clause}')
    result = cur.fetchall()

    return result[0] # <- Assume only one result

def getUserInput(prompt: str):
    print(f"{prompt}\033[33;4m", end="")
    res = input("")
    print("\033[0m", end="")
    return res

def escapeString(item):
    if type(item) is int: return item
    if type(item) is str: return f"'{item}'"

def getTableUserInput(prompt):
    table_names = getTableNames()

    print(table_names)
    table_choice = getUserInput(prompt)

    while table_choice not in table_names:
        print("Invalid Table Name");
        table_choice = getUserInput(prompt)

    return table_choice