from db import cur, con
from sqlite_print import print_cursor
from utils import getUserInput

def generate_reports():
    print("\nAdministrative Reports")
    print("1. Worker Assignments")
    print("2. Chemical Safety Analysis")
    print("3. Campus Area Status")
    print("4. Employee Workload")
    print("5. Upcoming Maintenance")

    choice = getUserInput("Pick a report (1-5): ")
    if choice == "1":
        show_worker_assignments()
    elif choice == "2":
        show_chemical_safety()
    elif choice == "3":
        show_area_status()
    elif choice == "4":
        show_employee_workload()
    elif choice == "5":
        show_upcoming_maintenance()
    else:
        print("Invalid choice. Please pick 1-5 only")

def show_worker_assignments():
    print("\nWorker Assignments")
    print("-"*50)
    query1 = """
    SELECT
        category as "Category",
        COUNT(DISTINCT employee_id) as "Workers",
        COUNT(*) as "Total Jobs"
    FROM CMM_ACTIVITY
    LEFT JOIN E_ASSIGNMENT
        ON activity_id = a_id
    LEFT JOIN EMPLOYEE
        ON e_id = employee_id
    GROUP BY category
    ORDER BY COUNT(DISTINCT employee_id) DESC
    """
    cur.execute(query1)
    print_cursor(cur)

def show_chemical_safety():
    print("\nChemical Safety Analysis")
    print("-"*50)
    query2 = """
    SELECT
        area_name as "Location",
        chemical_name as "Chemical",
        CASE
            WHEN is_harmful THEN 'Harmful'
            ELSE 'Safe'
        END as "Safety"
    FROM CAMPUS_AREA
    JOIN ACTIVITY_LOCATIONS
        ON area_id = location_id
    JOIN CHEMICAL_USAGE
        ON ACTIVITY_LOCATIONS.a_id = CHEMICAL_USAGE.a_id
    JOIN CHEMICALS
        ON CHEMICAL_USAGE.chemical_id = CHEMICALS.chemical_id
    GROUP BY area_name, chemical_name, is_harmful
    ORDER BY is_harmful DESC, COUNT(*) DESC
    """
    cur.execute(query2)
    print_cursor(cur)

def show_area_status():
    print("\nCampus Area Status")
    print("-"*50)
    query3 = """
    SELECT
        area_name as "Area",
        area_type as "Type",
        CASE
            WHEN EXISTS(
                SELECT 1
                FROM CMM_ACTIVITY
                JOIN ACTIVITY_LOCATIONS ON activity_id = a_id
                WHERE location_id = area_id
                AND makes_unusable = 1
                AND date('now') BETWEEN start_date AND end_date
            ) THEN 'Closed for work'
            ELSE 'Open'
        END as "Status",
        COUNT(DISTINCT activity_id) as "Past Activities"
    FROM CAMPUS_AREA
    LEFT JOIN ACTIVITY_LOCATIONS
        ON area_id = location_id
    LEFT JOIN CMM_ACTIVITY
        ON a_id = activity_id
    GROUP BY area_id, area_name, area_type
    ORDER BY
        CASE
            WHEN EXISTS(
                SELECT 1
                FROM CMM_ACTIVITY
                JOIN ACTIVITY_LOCATIONS ON activity_id = a_id
                WHERE location_id = area_id
                AND makes_unusable = 1
                AND date('now') BETWEEN start_date AND end_date
            ) THEN 0
            ELSE 1
        END,
        area_name
    """
    cur.execute(query3)
    print_cursor(cur)

def show_employee_workload():
    print("\nEmployee Workload")
    print("-"*50)
    query4 = """
    SELECT
        e_name as "Employee",
        level as "Level",
        COUNT(DISTINCT a_id) as "Jobs Assigned",
        COUNT(DISTINCT building_id) as "Buildings Supervised"
    FROM EMPLOYEE
    LEFT JOIN E_ASSIGNMENT
        ON employee_id = E_ASSIGNMENT.e_id
    LEFT JOIN BUILDING_SUPERVISION
        ON employee_id = BUILDING_SUPERVISION.e_id
    GROUP BY employee_id, e_name, level
    ORDER BY
        COUNT(DISTINCT a_id) DESC,
        COUNT(DISTINCT building_id) DESC
    """
    cur.execute(query4)
    print_cursor(cur)

def show_upcoming_maintenance():
    print("\nUpcoming Maintenance")
    print("-"*50)

    limitCount = getUserInput("How many activities to show (Press 'Enter' for first 10 activities): ")
    if limitCount == "":
        limitCount = 10
    else:
        try:
            limitCount = int(limitCount)
        except:
            print("Invalid input, showing 10 activites instead.")
            limitCount = 10

    query5 = f"""
    SELECT
        activity_desc as "Job Description",
        start_date as "Starting Date",
        end_date as "Ending Date",
        area_name as "Location"
    FROM CMM_ACTIVITY
    JOIN ACTIVITY_LOCATIONS
        ON activity_id = a_id
    JOIN CAMPUS_AREA
        ON location_id = area_id
    WHERE start_date >= date('now')
    ORDER BY start_date
    LIMIT {limitCount}
    """
    cur.execute(query5)
    print_cursor(cur)
