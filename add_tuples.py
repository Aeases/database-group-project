from db import cur, con
from utils import getUserInput, getTableColumns, getTableUserInput, escapeString
from validations import GeneralValidator, CampusRules, EmployeeLimitValidator

def user_add_tuple(table_choice):
    numOfInput = int(getUserInput("How many items would you like to insert? #"))
    print(f"\nInserting into {table_choice}\n")

    all_items = []
    
    for i in range(numOfInput):
        if i > 0: 
            print(f"\nInsertion #{i+1} into {table_choice}\n")
        try:
            item = get_validated_columns(table_choice)
            
            validation_result = validate_campus_rules(table_choice, item)
            if not validation_result[0]:
                print(f"Campus rule violation: {validation_result[1]}")
                continue
            
            all_items.append(item)
            
        except ValueError as e:
            print(f"Validation error: {e}")
            print("Please try again with correct values.")
            continue
    
    success_count = 0
    for column in all_items:
        if add_tuple_to_sql(table_choice, column):
            success_count += 1
            print("Record added successfully!")
        else:
            print("Failed to add record.")
    
    print(f"\nSuccessfully added {success_count} out of {numOfInput} records.")

def set_based_insertion(table_choice):
    print(f"\n=== Set-based Insertion for {table_choice} ===")
    print("Enter multiple rows at once using CSV format")
    print("Format: value1,value2,value3,... (one row per line)")
    print("Type 'DONE' on a new line when finished")
    print("Type 'CANCEL' to abort insertion\n")
    
    columns = getTableColumns(table_choice)
    print(f"Table columns: {', '.join(columns)}")
    print("Enter data in the same order as columns above")
    print("For NULL values, just leave empty between commas\n")
    
    rows = []
    row_count = 0
    
    while True:
        row_count += 1
        row_input = getUserInput(f"Row {row_count}: ")
        
        if row_input.upper() == 'DONE':
            break
        if row_input.upper() == 'CANCEL':
            print("Insertion cancelled.")
            return
        if not row_input.strip():
            continue
            
        # Split the CSV input
        row_data = [x.strip() for x in row_input.split(',')]
        
        # Validate column count
        if len(row_data) != len(columns):
            print(f"Error: Expected {len(columns)} values, got {len(row_data)}")
            print(f"Please enter exactly {len(columns)} values separated by commas")
            row_count -= 1
            continue
            
        # Process each value with validation
        processed_row = []
        try:
            for i, value in enumerate(row_data):
                column = columns[i]
                
                # Handle empty values as NULL
                if value == '':
                    processed_row.append('NULL')
                    continue
                
                # Apply validation based on column type
                if 'phone' in column.lower():
                    validated_value = GeneralValidator.validate_phone(value)
                elif 'email' in column.lower():
                    validated_value = GeneralValidator.validate_email(value)
                elif 'date' in column.lower():
                    validated_value = GeneralValidator.validate_date(value)
                elif any(x in column.lower() for x in ['is_', 'makes_']):
                    validated_value = GeneralValidator.validate_boolean(value)
                elif column == 'level':
                    validated_value = GeneralValidator.validate_level(value)
                elif column == 'area_type':
                    validated_value = GeneralValidator.validate_area_type(value)
                elif column == 'category':
                    validated_value = GeneralValidator.validate_category(value)
                else:
                    validated_value = value  # No special validation
                    
                processed_row.append(validated_value)
                
            rows.append(processed_row)
            print(f"Row {row_count} accepted")
            
        except ValueError as e:
            print(f"Validation error in row {row_count}: {e}")
            print("Please fix and re-enter this row")
            row_count -= 1
            continue
    
    if not rows:
        print("No rows to insert.")
        return
    
    print(f"\nReady to insert {len(rows)} rows into {table_choice}")
    print("Final review:")
    print("-" * 50)
    
    # Show preview
    for i, row in enumerate(rows, 1):
        print(f"Row {i}: {row}")
    
    print("-" * 50)
    
    # Confirm insertion
    confirm = getUserInput("Proceed with insertion? (y/n): ")
    if confirm.lower() not in ['y', 'yes']:
        print("Insertion cancelled.")
        return
    
    # Perform the insertion
    success_count = 0
    for row in rows:
        # Validate campus rules for each row
        validation_result = validate_campus_rules(table_choice, row)
        if not validation_result[0]:
            print(f"Campus rule violation: {validation_result[1]}")
            continue
            
        if add_tuple_to_sql(table_choice, row):
            success_count += 1
            print(f"Inserted row {success_count} successfully")
        else:
            print(f"Failed to insert row")
    print(f"\n=== Insertion Complete ===")
    print(f"Successfully inserted {success_count} out of {len(rows)} rows")

def get_validated_columns(table):
    all_columns = getTableColumns(table)
    all_items = []

    for column in all_columns:
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

def add_tuple_to_sql(target_table, tuple_data):
    try:
        processed_values = []
        for value in tuple_data:
            if value == 'NULL':
                processed_values.append('NULL')
            else:
                processed_values.append(escapeString(value))
        
        columns = getTableColumns(target_table)
        insertion_string = f"INSERT INTO {target_table} ({', '.join(columns)}) VALUES ({', '.join(['?'] * len(processed_values))})"
        cur.execute(insertion_string, processed_values)


        con.commit()
        return True
    except Exception as e:
        print(f"Database error: {e}")
        con.rollback()
        return False
