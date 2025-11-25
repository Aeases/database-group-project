table_definitions = [
    """CREATE TABLE EMPLOYEE(
        employee_id INTEGER PRIMARY KEY AUTOINCREMENT,
        e_name VARCHAR(15) NOT NULL, 
        e_phone VARCHAR(8) NOT NULL, 
        supervisor_id INT,
        level INT,
        FOREIGN KEY (supervisor_id) REFERENCES EMPLOYEE(employee_id)
    );""",
    
    # TO DO: add types to the columns
    """CREATE TABLE CMM_ACTIVITY(
        activity_id INTEGER PRIMARY KEY AUTOINCREMENT,
        activity_desc VARCHAR(30),
        start_date DATE,
        end_date DATE,
        makes_unusable BOOLEAN,
        category VARCHAR(15)
    )""",

    """CREATE TABLE SUBCONTRACTOR(
        c_id INTEGER PRIMARY KEY AUTOINCREMENT,
        c_name VARCHAR(15),
        c_phone VARCHAR(15),
        c_email VARCHAR(30)
    )""",

    """CREATE TABLE E_ASSIGNMENT(
        a_id INTEGER PRIMARY KEY, 
        e_id INTEGER PRIMARY KEY,
        FOREIGN KEY (a_id) REFERENCES CMM_ACTIVITY(activity_id),
        FOREIGN KEY (e_id) REFERENCES EMPLOYEE(employee_id)
    )""",

    """CREATE TABLE C_ASSIGNMENT(
        a_id INTEGER PRIMARY KEY, 
        c_id INTEGER PRIMARY KEY,
        FOREIGN KEY (a_id) REFERENCES CMM_ACTIVITY(activity_id),
        FOREIGN KEY (c_id) REFERENCES SUBCONTRACTOR(c_id)
    )""",
    """CREATE TABLE CAMPUS_AREA(
        area_id INTEGER PRIMARY KEY,
        area_name VARCHAR(15),
        area_type VARCHAR(15),
        last_maintenance_date DATE
    )""",
    """CREATE TABLE ACTIVITY_LOCATIONS(
        location_id INTEGER PRIMARY KEY,
        a_id INTEGER PRIMARY KEY,
        FOREIGN KEY (location_id) REFERENCES CAMPUS_AREA(area_id),
        FOREIGN KEY (a_id) REFERENCES CMM_ACTIVITY(activity_id)
    )""",
    """CREATE TABLE CHEMICALS(
        chemical_id INTEGER PRIMARY KEY,
        chemical_name VARCHAR(15) NOT NUL,
        is_harmful BOOLEAN NOT NULL
    )""",
    """CREATE TABLE CHEMICAL_USAGE(
        chemical_id INTEGER PRIMARY KEY,
        a_id INTEGER NOT NULl,
        FOREIGN KEY (chemical_id) REFERENCES CHEMICALS(chemical_id),
        FOREIGN KEY (a_id) REFERENCES CMM_ACTIVITY(activity_id)
    )""",
    """CREATE TABLE BUILDING_SUPERVISION(
        building_id INTEGER PRIMARY KEY,
        e_id INTEGER PRIMARY KEY,
        FOREIGN KEY (building_id) REFERENCES CAMPUS_AREA(area_id),
        FOREIGN KEY (e_id) REFERENCES CMM_ACTIVITY(activity_id)
    )"""
]

employee_definitions = [
    ""
]