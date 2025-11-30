from db import cur, con
from utils import getUserInput, getTableColumns, getTableUserInput, escapeString, get_validated_columns, validate_campus_rules;
from validations import GeneralValidator, CampusRules, EmployeeLimitValidator
from auth import auth_system



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
    
    insertion_string = f"INSERT INTO {target_table} ({", ".join(getTableColumns(target_table))}) VALUES ({", ".join(escaped_values)})"
    cur.execute(insertion_string)

def set_based_insertion(table_choice):
    if not auth_system.has_permission('executive officer'):
        print("Error: Only executive officers can perform set-based insertion.")
        return

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
