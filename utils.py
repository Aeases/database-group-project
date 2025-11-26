from db import cur, con

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


def getTableUserInput(prompt):
    table_names = getTableNames()

    print(table_names)
    table_choice = getUserInput(prompt)

    while table_choice not in table_names:
        print("Invalid Table Name");
        table_choice = getUserInput(prompt)

    return table_choice