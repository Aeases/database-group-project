from db import cur, con
from add_tuples import user_add_tuple
from add_tuples import set_based_insertion
from updating_tuples import user_update_tuple
from updating_tuples import user_delete_tuple
from utils import getUserInput, getTableUserInput
from sqlite_print import print_cursor
from scheduled_activities import getScheduledActivities
from report_generation import generate_reports
import sys

def show_menu():
    print("""
    1 | Insert Tuples
    2 | Set-based Insertion
    3 | Update Tuples
    4 | Delete Tuples
    5 | Run SQL Queries
    6 | Find Scheduled Cleaning Activities
    7 | Generate Reports
    8 | Exit System      
    """)


def process_cmd():
    show_menu()

    choice = ''

    while True:
        choice = getUserInput("Option: ")
        if len(choice) == 1 and choice in ['1', '2', '3', '4', '5', '6', '7', '8']:
            break;
        else:
            print("Invalid Input")


    table_choice = ''
    if choice in ['1', '2', '3', '4']:
        table_choice = getTableUserInput("Table: ")

    match choice:
        case '1':
            user_add_tuple(table_choice)
        case '2':
            set_based_insertion(table_choice)    
        case '3':
            user_update_tuple(table_choice)
        case '4':
            user_delete_tuple(table_choice)
        case '5':
            try:
                user_SQL_query = getUserInput("SQL QUERY: ", ansiStart='')
                print("-- Result --\n")
                print_cursor(cur.execute(user_SQL_query))
            except Exception as e:
                print(f"SQL Error: {e}")
                con.rollback()
        case '6':
            getScheduledActivities()
        case '7':
            generate_reports()
        case '8':
            print("Thank you for using Campus Maintenance Management System. Goodbye!")
            sys.exit(0)
    con.commit()

if __name__ == "__main__":
    print("Welcome to Campus Maintenance Management System!")
    while True:
        process_cmd()
