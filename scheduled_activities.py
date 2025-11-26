from db import cur, con
from utils import getUserInput

def getScheduledActivities():
    start_date = getUserInput("Activities starting from date (YYYY-MM-DD): ")
    end_date = getUserInput("Activities ending by date (YYYY-MM-DD): ")
    area_name = getUserInput("In which campus area?: ")

    filterConditions = []
    filterParameters = []
    
    sqlQuery = """
    SELECT
        activity.activity_id,
        activity.activity_desc,
        activity.start_date,
        activity.end_date,
        activity.makes_unusable,
        activity.category,
        area.area_id,
        area.area_name,
        area.area_type
    FROM CMM_ACTIVITY activity
    JOIN ACTIVITY_LOCATIONS locations ON activity.activity_id = locations.a_id
    JOIN CAMPUS_AREA area ON locations.location_id = area.area_id
    """

    if start_date:
        filterConditions.append("activity.start_date >= ?")
        filterParameters.append(start_date)
    
    if end_date:
        filterConditions.append("activity.end_date <= ?")
        filterParameters.append(end_date)

    if area_name:
        filterConditions.append("area.area_name LIKE ?")
        filterParameters.append(f'%{area_name}%')
    
    if filterConditions:
        sqlQuery += " WHERE " + " AND ".join(filterConditions)
    
    sqlQuery += " ORDER BY activity.start_date, activity.end_date, area.area_name"

    try:
        cur.execute(sqlQuery, filterParameters)
        allActivities = cur.fetchall()

        if not allActivities:
            print("\nNo activities found matching your input.")
            print("\nCheck for typos or try broadening your search.")
            return
        
        print(f"\nFound {len(allActivities)} scheduled activity(s): ")

        activity_id_list = [str(activity[0]) for activity in allActivities]
        activity_id_sql = ",".join(activity_id_list)

        chemicalQuery = f"""
        SELECT
            cu.a_id,
            chem.chemical_name,
            chem.is_harmful
        FROM CHEMICAL_USAGE cu
        JOIN CHEMICALS chem ON cu.chemical_id = chem.chemical_id
        WHERE cu.a_id IN ({activity_id_sql})
        """

        cur.execute(chemicalQuery)
        allChemicals = cur.fetchall()

        assignmentQuery = f"""
        SELECT
            activity.activity_id,
            COALESCE(
                e.e_name, 
                s.c_name, 
                'No one assigned yet'
            ) as assigned_to
        FROM CMM_ACTIVITY activity
        LEFT JOIN E_ASSIGNMENT ea ON activity.activity_id = ea.a_id
        LEFT JOIN EMPLOYEE e ON ea.e_id = e.employee_id
        LEFT JOIN C_ASSIGNMENT ca ON activity.activity_id = ca.a_id
        LEFT JOIN SUBCONTRACTOR s ON ca.c_id = s.c_id
        WHERE activity.activity_id IN ({activity_id_sql})
        """

        cur.execute(assignmentQuery)
        allAssignments = cur.fetchall()

        chemical = {}
        for chem in allChemicals:
            activity_id = chem[0]
            if activity_id not in chemical:
                chemical[activity_id] = []
            chemical[activity_id].append({
                'name': chem[1],
                'is_harmful': chem[2]
            })
        
        assignment = {}
        for assign in allAssignments:
            assignment[assign[0]] = assign[1]
        
        for activity in allActivities:
            activity_id, activity_desc, start_date, end_date, makes_unusable, category, area_id, area_name, area_type = activity
            print(f"\nActivity ID: {activity_id}")
            print(f"Activity Description: {activity_desc}")
            print(f"\nCategory: {category}")
            print(f"\nLocation: {area_name} ({area_type})")
            print(f"\nTime Period: {start_date} to {end_date}")
            print(f"\nArea Unusable: {'Yes' if makes_unusable else 'No'}")

            assigned_to = assignment.get(activity_id, 'No one assigned yet')
            print(f"Assigned To: {assigned_to}")

            chemicals = chemical.get(activity_id, [])
            if chemicals:
                harmful = [chem for chem in chemicals if chem['is_harmful']]
                print(f"Chemicals Used: {', '.join([chem['name'] for chem in chemicals])}")
                if harmful:
                    print("WARNING: Harmful chemicals are used in this activity.")
                else:
                    print("No harmful chemicals used.")
            else:
                print("Chemicals Used: None")
            
            print("-"*50)

