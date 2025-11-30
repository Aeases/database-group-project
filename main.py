from db import cur, con
from add_tuples import user_add_tuple
from add_tuples import set_based_insertion
from updating_tuples import user_update_tuple
from updating_tuples import user_delete_tuple
from utils import getUserInput, getTableUserInput
from sqlite_print import print_cursor
from scheduled_activities import getScheduledActivities
from report_generation import generate_reports
from auth import auth_system
import sys

def show_menu():
    user_level = auth_system.get_permission_level()
    print(f"\n=== CMMS Main Menu (Logged in as: {user_level}) ===")
    
    menu_items = []
    menu_number = 1
    
    # Add role-specific menu items first
    if auth_system.has_permission('executive officer'):
        menu_items.append(f"{menu_number} | Insert Tuples")
        menu_number += 1
        menu_items.append(f"{menu_number} | Set-based Insertion")
        menu_number += 1
    
    if auth_system.has_permission('mid-level manager'):
        menu_items.append(f"{menu_number} | Update Tuples")
        menu_number += 1
        menu_items.append(f"{menu_number} | Delete Tuples")
        menu_number += 1
    
    # Base menu items available to all levels
    menu_items.append(f"{menu_number} | Run SQL Queries")
    menu_number += 1
    menu_items.append(f"{menu_number} | Find Scheduled Cleaning Activities")
    menu_number += 1
    menu_items.append(f"{menu_number} | Generate Reports")
    menu_number += 1
    
    # Always available
    menu_items.append(f"{menu_number} | Logout")
    menu_number += 1
    menu_items.append(f"{menu_number} | Exit System")
    
    print("\n".join(menu_items))
    return menu_number  # Return the total number of menu items

def process_cmd():
    total_menu_items = show_menu()
    choice = ''

    while True:
        choice = getUserInput("Option: ")
        
        # Generate valid choices based on total menu items
        valid_choices = [str(i) for i in range(1, total_menu_items + 1)]
            
        if choice in valid_choices:
            break
        else:
            print(f"Invalid Input. Please choose 1-{total_menu_items}")

    # Map choice numbers to actual functions
    menu_mapping = {}
    current_choice = 1
    
    # Build mapping based on permissions
    if auth_system.has_permission('executive officer'):
        menu_mapping[str(current_choice)] = ('insert', None)
        current_choice += 1
        menu_mapping[str(current_choice)] = ('set_insert', None)
        current_choice += 1
    
    if auth_system.has_permission('mid-level manager'):
        menu_mapping[str(current_choice)] = ('update', None)
        current_choice += 1
        menu_mapping[str(current_choice)] = ('delete', None)
        current_choice += 1
    
    # Base functions
    menu_mapping[str(current_choice)] = ('sql', None)
    current_choice += 1
    menu_mapping[str(current_choice)] = ('schedule', None)
    current_choice += 1
    menu_mapping[str(current_choice)] = ('reports', None)
    current_choice += 1
    menu_mapping[str(current_choice)] = ('logout', None)
    current_choice += 1
    menu_mapping[str(current_choice)] = ('exit', None)

    # Get table choice for operations that need it
    action, table_choice = menu_mapping[choice]
    if action in ['insert', 'set_insert', 'update', 'delete']:
        table_choice = getTableUserInput("Table: ")

    match action:
        case 'insert':
            user_add_tuple(table_choice)
        case 'set_insert':
            set_based_insertion(table_choice)
        case 'update':
            user_update_tuple(table_choice)
        case 'delete':
            user_delete_tuple(table_choice)
        case 'sql':
            try:
                user_SQL_query = getUserInput("SQL QUERY: ", ansiStart='')
                print("-- Result --\n")
                print_cursor(cur.execute(user_SQL_query))
            except Exception as e:
                print(f"SQL Error: {e}")
                con.rollback()
        case 'schedule':
            getScheduledActivities()
        case 'reports':
            generate_reports()
        case 'logout':
            auth_system.logout()
            return 'logout'
        case 'exit':
            print("Thank you for using Campus Maintenance Management System. Goodbye!")
            sys.exit(0)
    
    con.commit()
    return 'continue'

def login_loop():
    while True:
        if auth_system.login():
            break
        else:
            retry = getUserInput("Login failed. Try again? (y/n): ")
            if retry.lower() not in ['y', 'yes']:
                print("Goodbye!")
                sys.exit(0)

if __name__ == "__main__":
    print("Welcome to Campus Maintenance Management System!")
    
    while True:
        login_loop()
        
        # Main application loop
        while True:
            result = process_cmd()
            if result == 'logout':
                break
