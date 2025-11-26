from db import cur, con
from add_tuples import user_add_tuple
from updating_tuples import user_update_tuple
from updating_tuples import user_delete_tuple
from utils import getUserInput, getTableUserInput
print("""
1 | Insert Tuples
2 | Update Tuples
3 | Delete Tuples     

4 | Run SQL Queries
5 | Find Scheduled Cleaning Activities
""")
choice = ''

while True:
    choice = getUserInput("Option: ")
    if len(choice) == 1 and choice in ['1', '2', '3', '4', '5']:
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
        print("still to come :)")
    case '5':
        print("still to come :)")
con.commit()
