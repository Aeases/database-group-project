from db import cur, con
from utils import getUserInput

def getScheduledActivities():
    # search for campus maintenance activities
    print("\n🔍 FIND SCHEDULED ACTIVITIES")
    print("="*50)
    start_date = getUserInput("Activities starting from date (YYYY-MM-DD): ")
    end_date = getUserInput("Activities ending by date (YYYY-MM-DD): ")
    area_name = getUserInput("Which campus area are you looking for? (Press Enter for all): ")
 
    print("\n📁 Activity Categories:")
    print("     Press Enter for ALL categories")
    print("     - cleaning: Daily cleaning activities")
    print("     - repair: Fixing ageing or weather-related issues")
    print("     - renovation: Major upgrades and changes")
    category_filter = getUserInput("Filter by category (optional): ")

    conditions = []
    params = []
    
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
    JOIN ACTIVITY_LOCATIONS locations 
        ON activity.activity_id = locations.a_id
    JOIN CAMPUS_AREA area 
        ON locations.location_id = area.area_id
    """

    if start_date:
        conditions.append("activity.start_date >= ?")
        params.append(start_date)
    
    if end_date:
        conditions.append("activity.end_date <= ?")
        params.append(end_date)

    if area_name:
        conditions.append("area.area_name LIKE ?")
        params.append(f'%{area_name}%')
    
    if category_filter:
        conditions.append("activity.category = ?")
        params.append(category_filter)
    
    if conditions:
        sqlQuery += " WHERE " + " AND ".join(conditions)
    
    sqlQuery += " ORDER BY activity.start_date, activity.end_date, area.area_name"

    try:
        print("\n⏳ Searching for scheduled activities...")
        cur.execute(sqlQuery, params)
        allActivities = cur.fetchall()

        # exit if no activities found
        if not allActivities:
            print("\n🚫 No matching activities found.")
            print("💡 Please check your search terms or try a different date range.")
            return
        
        category_count = {}
        category_desc = {
            'cleaning': 'Daily Cleaning',
            'repair': 'Repairs & Maintenance',
            'renovation': 'Renovation Projects'
        }

        for activity in allActivities:
            category = activity[5]
            category_count[category] = category_count.get(category, 0) + 1

        print(f"\nWe found {len(allActivities)} scheduled activity(s) that match your search.")
        if category_count:
            category_summary = " | ".join([f"{count}{category_desc[cat]}" for cat, count in category_count.items()])
            print(f"    📊 Breakdown: {category_summary}")
        print("="*60)
       
        activity_id_list = [str(activity[0]) for activity in allActivities]
        activity_id_sql = ",".join(activity_id_list)

        # get chemical usage for all activities
        chemicalQuery = f"""
        SELECT
            cu.a_id,
            chem.chemical_name,
            chem.is_harmful
        FROM CHEMICAL_USAGE cu
        JOIN CHEMICALS chem 
            ON cu.chemical_id = chem.chemical_id
        WHERE cu.a_id IN ({activity_id_sql})
        """

        cur.execute(chemicalQuery)
        allChemicals = cur.fetchall()

        # get assignment information
        assignmentQuery = f"""
        SELECT
            activity.activity_id,
            COALESCE(
                e.e_name, 
                s.c_name, 
                'No one assigned yet'
            ) as assigned_to
        FROM CMM_ACTIVITY activity
        LEFT JOIN E_ASSIGNMENT ea 
            ON activity.activity_id = ea.a_id
        LEFT JOIN EMPLOYEE e 
            ON ea.e_id = e.employee_id
        LEFT JOIN C_ASSIGNMENT ca 
            ON activity.activity_id = ca.a_id
        LEFT JOIN SUBCONTRACTOR s 
            ON ca.c_id = s.c_id
        WHERE activity.activity_id IN ({activity_id_sql})
        """

        cur.execute(assignmentQuery)
        allAssignments = cur.fetchall()

        # organize chemical information by activity ID
        chemical_info = {}
        for chem in allChemicals:
            activity_id = chem[0]
            if activity_id not in chemical_info:
                chemical_info[activity_id] = []
            chemical_info[activity_id].append({
                'name': chem[1],
                'is_harmful': bool(chem[2])
            })

        # organize assignment information by activity ID
        assignment_info = {}
        for assign in allAssignments:
            assignment_info[assign[0]] = {
                'assigned_to': assign[1],
                'type': assign[2]
            }

        # display detailed information for each activity
        for i, activity in enumerate(allActivities, 1):
            activity_id, activity_desc, start_date, end_date, makes_unusable, category, area_id, area_name, area_type = activity
            
            category_details = {
                'cleaning': {'icon': '🧹', 'label': 'DAILY CLEANING'},
                'repair': {'icon': '🛠️', 'label': 'REPAIR & MAINTENANCE'},
                'renovation': {'icon': '🏗️', 'label': 'RENOVATION PROJECT'}
            }
            cat_info = category_details.get(category, {'icon': '📋', 'label': category.upper()})
            
            print(f"\n{cat_info['icon']} ACTIVITY #{i} - {cat_info['label']}")
            print("="*50)
            print(f"🔢 Activity ID: {activity_id}")
            print(f"📝 Activity Description: {activity_desc}")
            print(f"📍 Location: {area_name} ({area_type})")
            print(f"📅 Time Period: {start_date} to {end_date}")

            # show area usability status
            if makes_unusable:
                print(f"🚫 AREA STATUS: This area will be UNAVAILABLE during the activity.")
                if category == 'renovation':
                    print("    ⚠️ Renovation project - extended closure expected")
                elif category == 'repair':
                    print("    🔧 Repair work - temporary closure for safety")
            else:
                print(f"✅ AREA STATUS: Area remains USABLE during the activity.")

            # show assignment information
            assignment = assignment_info.get(activity_id, {'assigned_to': 'No one assigned yet', 'type': 'Unassigned'})
            assignee_icon = "👤" if assignment['type'] == 'Employee' else "🏢" if assignment['type'] == 'Subcontractor' else "❓"
            print(f"{assignee_icon} Assigned To: {assignment['assigned_to']} ({assignment['type']})")

            # show chemical information
            chemicals_used = chemical_info.get(activity_id, [])
            if chemicals_used:
                chemical_names = [chem['name'] for chem in chemicals_used]
                harmful_chems = [chem for chem in chemicals_used if chem['is_harmful']]
                
                print(f"🧪 Chemicals: {', '.join(chemical_names)}")
                
                if harmful_chems:
                    harmful_names = [chem['name'] for chem in harmful_chems]
                    print(f"⚠️  WARNING: Harmful chemicals used: {', '.join(harmful_names)}")
                    
                    if category == 'cleaning':
                        print("   🧤 Use protective equipment during cleaning")
                    elif category == 'renovation':
                        print("   🏗️ Construction area - restricted access required")
                    else:
                        print("   Please ensure proper safety measures are taken!")
                
                else:
                    print(f"✅  SAFETY: All materials used are safe.")
            else:
                print(f"🧪 Chemicals: No chemicals used in this activity.")
            
            print("-"*50)
            
        # summary statistics
        harmful_count = sum(1 for activity in allActivities
                            if any(chem['is_harmful'] for chem in chemical_info.get(activity[0], [])))
        unavailable_count = sum(1 for activity in allActivities if activity[4])

        # count by category for detailed summary
        cleaning_count = sum(1 for activity in allActivities if activity[5] == 'cleaning')
        repair_count = sum(1 for activity in allActivities if activity[5] == 'repair')
        renovation_count = sum(1 for activity in allActivities if activity[5] == 'renovation')

        print(f"\n📊 SEARCH SUMMARY:")
        print(f"    - Total activities found: {len(allActivities)}")
        print(f"    - Cleaning activities: {cleaning_count}")
        print(f"    - Repair & Maintenance: {repair_count}")
        print(f"    - Renovation projects: {renovation_count}")
        print(f"    - Activities with harmful chemicals: {harmful_count}")
        print(f"    - Activities making areas unavailable: {unavailable_count}")

        if harmful_count > 0:
            print(f"\n💡 Safety Notice: {harmful_count} activity(s) use harmful chemicals")
            print("   Please review safety protocols for these activities!")

        if renovation_count > 0:
            print(f"🏗️  Renovation Notice: {renovation_count} major renovation project(s) found")

    except Exception as error:
        print(f"❌ Error searching activities: {error}")
        print("💡 Please check your date format (YYYY-MM-DD) and try again.")
