from db import cur, con

def get_validated_columns(table):
    all_columns = getTableColumns(table)
    all_items = []

    for column in all_columns:
        if table == 'EMPLOYEE' and column == 'employee_id':
            continue
        while True:
            try:
                value = getUserInput(f"{column} <- ")
                
                if column in ['supervisor_id'] and value == '':
                    all_items.append('NULL')
                    break
                
                if 'phone' in column.lower():
                    value = GeneralValidator.validate_phone(value)
                elif 'email' in column.lower():
                    value = GeneralValidator.validate_email(value)
                elif 'date' in column.lower():
                    if value:
                        value = GeneralValidator.validate_date(value)
                elif any(x in column.lower() for x in ['is_', 'makes_']):
                    value = GeneralValidator.validate_boolean(value)
                elif column == 'level':
                    value = GeneralValidator.validate_level(value)
                elif column == 'area_type':
                    value = GeneralValidator.validate_area_type(value)
                elif column == 'category':
                    value = GeneralValidator.validate_category(value)
                
                all_items.append(value)
                break
                
            except ValueError as e:
                print(f"Invalid input: {e}")
    
    return all_items

def validate_campus_rules(table, item_data):
    columns = getTableColumns(table)
    data_dict = dict(zip(columns, item_data))
    
    try:
        if table == 'EMPLOYEE':
            if 'level' in data_dict:
                is_valid, message = EmployeeLimitValidator.check_employee_limits(data_dict['level'])
                if not is_valid:
                    return False, message
            
            if 'supervisor_id' in data_dict and data_dict['supervisor_id'] != 'NULL':
                employee_level = None
                if 'level' in data_dict:
                    employee_level = data_dict['level']
                
                is_valid, message = CampusRules.validate_supervisor_hierarchy(
                    'NEW',  
                    data_dict['supervisor_id'],
                    employee_level  
                )
                if not is_valid:
                    return False, message
        
        elif table == 'BUILDING_SUPERVISION':
            building_id = data_dict.get('building_id')
            employee_id = data_dict.get('e_id')
            if building_id and employee_id:
                return CampusRules.validate_building_supervisor(building_id, employee_id)
        
        elif table == 'E_ASSIGNMENT':
            activity_id = data_dict.get('a_id')
            employee_id = data_dict.get('e_id')
            if activity_id and employee_id:
                return CampusRules.validate_activity_assignment(activity_id, employee_id=employee_id)
        
        elif table == 'C_ASSIGNMENT':
            activity_id = data_dict.get('a_id')
            subcontractor_id = data_dict.get('c_id')
            if activity_id and subcontractor_id:
                return CampusRules.validate_activity_assignment(activity_id, subcontractor_id=subcontractor_id)
        
        elif table == 'CMM_ACTIVITY':
            start_date = data_dict.get('start_date')
            end_date = data_dict.get('end_date')
            if start_date and end_date:
                return CampusRules.validate_activity_dates(start_date, end_date)
        
        elif table == 'CHEMICAL_USAGE':
            chemical_id = data_dict.get('chemical_id')
            activity_id = data_dict.get('a_id')
            if chemical_id and activity_id:
                return CampusRules.validate_chemical_usage(chemical_id, activity_id)
        
        elif table == 'ACTIVITY_LOCATIONS':
            location_id = data_dict.get('location_id')
            activity_id = data_dict.get('a_id')
            if location_id and activity_id:
                return CampusRules.validate_activity_location(location_id, activity_id)
        
        return True, "Validation passed"
        
    except Exception as e:
        return False, f"Validation error: {e}"

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
def searchPkToWhereClause(table, search_primary_keys):
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

def getUserInput(prompt: str, ansiStart = '\033[1;32m'):
    print(f"{prompt}{ansiStart}", end="")
    res = input("")
    print('\033[0m', end="")
    return res

def getUserBinaryInput(prompt):
    while True:

        res = getUserInput(prompt, '\033[1;31m')

        if res.lower() in ['y', '1', 'yes', 'true', 't']:
            return True
        if res.lower() in ['n', '0', 'no', 'false', 'f']:
            return False
        else:
            print("Invalid Input");


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
