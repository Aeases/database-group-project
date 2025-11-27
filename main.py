from db import cur, con
from add_tuples import user_add_tuple
from updating_tuples import user_update_tuple
from updating_tuples import user_delete_tuple
from utils import getUserInput, getTableUserInput
from sqlite_print import print_cursor
from scheduled_activities import getScheduledActivities
from report_generation import generate_reports

print("""
1 | Insert Tuples
2 | Update Tuples
3 | Delete Tuples
4 | Run SQL Queries
5 | Find Scheduled Cleaning Activities
6 | Generate Reports
""")
choice = ''

while True:
    choice = getUserInput("Option: ")
    if len(choice) == 1 and choice in ['1', '2', '3', '4', '5', '6']:
        break;
    else:
        print("Invalid Input")


table_choice = ''
if choice in ['1', '2', '3']:
    table_choice = getTableUserInput("Table: ")

match choice:
    case '1':
        user_add_tuple(table_choice)
    case '2':
        user_update_tuple(table_choice)
    case '3':
        user_delete_tuple(table_choice)
    case '4':
        user_SQL_query = getUserInput("SQL QUERY: ", ansiStart='')
        print("-- Result --\n")
        print_cursor(cur.execute(user_SQL_query))
    case '5':
        getScheduledActivities()
    case '6':
        generate_reports()
con.commit()
