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

    user_primary_columns = []
    for key in primary_columns:
        user_primary_columns.append(getUserInput(f"{key} : "))

    return user_primary_columns

def searchForRecord(table, search_primary_keys):
    primary_keys = getTablePrimaryColumns(table)

    where_clause = ''
    if (search_primary_keys.__len__() > 1):
        where_clause = ' AND '.join(
            [f'{primary_keys[i]} = {search_primary_keys[i]}' for i in range(0, search_primary_keys.__len__())]
        )
    else:
        where_clause = f'{primary_keys[0]} = {search_primary_keys[0]}'
    
    cur.execute(f'SELECT * FROM {table} WHERE {where_clause}')
    result = cur.fetchall()

    return result

def getUserInput(prompt: str):
    print(f"{prompt}\033[33;4m", end="")
    res = input("")
    print("\033[0m", end="")
    return res


def getTableUserInput(prompt):
    table_names = getTableNames()

    print(table_names)
    table_choice = getUserInput(prompt)

    while table_choice not in table_names:
        print("Invalid Table Name");
        table_choice = getUserInput(prompt)

    return table_choice