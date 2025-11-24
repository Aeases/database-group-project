table_definitions = [
    """CREATE TABLE EMPLOYEE(
        employee_id INTEGER PRIMARY KEY AUTOINCREMENT,
        e_name, 
        e_phone, 
        supervisor_id,
        level,
        FOREIGN KEY (supervisor_id) REFERENCES EMPLOYEE(employee_id)
    );""",
    # TO DO: add types to the columns
    """CREATE TABLE CMM_ACTIVITY(
        activity_id,
        activity_desc,
        start_date,
        end_date,
        makes_unusable,
        category
    )""",

    """CREATE TABLE SUBCONTRACTOR(
        c_id,
        c_name,
        c_phone,
        c_email
    )""",

    """CREATE TABLE E_ASSIGNMENT(
        a_id, 
        e_id
    )""",

    """CREATE TABLE C_ASSIGNMENT(
        a_id, 
        c_id
    )""",
    """CREATE TABLE CAMPUS_AREA(
        a_id,
        c_id
    )""",
    """CREATE TABLE CHEMICALS(
        chemical_id,
        chemical_name,
        is_harmful
    )""",
    """CREATE TABLE CHEMICAL_USAGE(
        chemical_id,
        a_id
    )""",
    """CREATE TABLE BUILDING_SUPERVISION(
        building_id,
        e_id
    )"""
]

employee_definitions = [
    ""
]