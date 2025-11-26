table_definitions = [
    """CREATE TABLE EMPLOYEE(
        employee_id INTEGER PRIMARY KEY AUTOINCREMENT,
        e_name VARCHAR(30) NOT NULL, 
        e_phone VARCHAR(8) NOT NULL, 
        supervisor_id INT,
        level INT,
        FOREIGN KEY (supervisor_id) REFERENCES EMPLOYEE(employee_id)
    );""",
    
    # TO DO: add types to the columns
    """CREATE TABLE CMM_ACTIVITY(
        activity_id INTEGER PRIMARY KEY AUTOINCREMENT,
        activity_desc VARCHAR(100),
        start_date DATE,
        end_date DATE,
        makes_unusable BOOLEAN,
        category VARCHAR(15)
    )""",

    """CREATE TABLE SUBCONTRACTOR(
        c_id INTEGER PRIMARY KEY AUTOINCREMENT,
        c_name VARCHAR(15),
        c_phone INTEGER,
        c_email VARCHAR(100)
    )""",

    """CREATE TABLE E_ASSIGNMENT(
        a_id INTEGER, 
        e_id INTEGER,
        FOREIGN KEY (a_id) REFERENCES CMM_ACTIVITY(activity_id),
        FOREIGN KEY (e_id) REFERENCES EMPLOYEE(employee_id),
        PRIMARY KEY (a_id, e_id)
    )""",

    """CREATE TABLE C_ASSIGNMENT(
        a_id INTEGER, 
        c_id INTEGER,
        FOREIGN KEY (a_id) REFERENCES CMM_ACTIVITY(activity_id),
        FOREIGN KEY (c_id) REFERENCES SUBCONTRACTOR(c_id)
        PRIMARY KEY (a_id, c_id)
    )""",
    """CREATE TABLE CAMPUS_AREA(
        area_id INTEGER PRIMARY KEY,
        area_name VARCHAR(15),
        area_type VARCHAR(15),
        last_maintenance_date DATE
    )""",
    #ACTIVITY_LOCATIONS no Primary
    """CREATE TABLE ACTIVITY_LOCATIONS(
        location_id INTEGER, 
        a_id INTEGER,
        FOREIGN KEY (location_id) REFERENCES CAMPUS_AREA(area_id),
        FOREIGN KEY (a_id) REFERENCES CMM_ACTIVITY(activity_id),
        PRIMARY KEY (location_id, a_id)
    )""",
    """CREATE TABLE CHEMICALS(
        chemical_id INTEGER PRIMARY KEY,
        chemical_name VARCHAR(15) NOT NULL,
        is_harmful BOOLEAN NOT NULL
    )""",
    """CREATE TABLE CHEMICAL_USAGE(
        chemical_id INTEGER,
        a_id INTEGER NOT NULL,
        FOREIGN KEY (chemical_id) REFERENCES CHEMICALS(chemical_id),
        FOREIGN KEY (a_id) REFERENCES CMM_ACTIVITY(activity_id),
        PRIMARY KEY (chemical_id, a_id)
    )""",
    """CREATE TABLE BUILDING_SUPERVISION(
        building_id INTEGER,
        e_id INTEGER,
        FOREIGN KEY (building_id) REFERENCES CAMPUS_AREA(area_id),
        FOREIGN KEY (e_id) REFERENCES CMM_ACTIVITY(activity_id),
        PRIMARY KEY (building_id, e_id)
    )""",
]

table_rows = [
#EMPLOYEE
"""INSERT INTO EMPLOYEE (e_name, e_phone, supervisor_id, level) VALUES ('John Arbuckle', '61929507', NULL, 1)""",
"""INSERT INTO EMPLOYEE (e_name, e_phone, supervisor_id, level) VALUES ('Skibidi Sigma', '22712679', 1, 2)""",
"""INSERT INTO EMPLOYEE (e_name, e_phone, supervisor_id, level) VALUES ('Garfield Rizz', '37058588', 1, 2)""" ,
"""INSERT INTO EMPLOYEE (e_name, e_phone, supervisor_id, level) VALUES ('Quandale Fortnite', '52523057', 2, 3)""",
"""INSERT INTO EMPLOYEE (e_name, e_phone, supervisor_id, level) VALUES ('Usagi Rabbit', '36452595', 3, 3)""",

#CMM_ACTIVITY 
"""INSERT INTO CMM_ACTIVITY (activity_desc, start_date, end_date, makes_unusable, category) VALUES ('window cleaning', '2025-11-25', '2025-11-26', TRUE, 'cleaning')""",
"""INSERT INTO CMM_ACTIVITY (activity_desc, start_date, end_date, makes_unusable, category) VALUES ('gate cleaning', '2025-11-27', '2025-11-28', FALSE, 'cleaning')""",
"""INSERT INTO CMM_ACTIVITY (activity_desc, start_date, end_date, makes_unusable, category) VALUES ('door repair', '2025-11-29', '2025-11-30', TRUE, 'repair')""",
"""INSERT INTO CMM_ACTIVITY (activity_desc, start_date, end_date, makes_unusable, category) VALUES ('light repair', '2025-12-01', '2025-12-02', TRUE, 'repair')""",
"""INSERT INTO CMM_ACTIVITY (activity_desc, start_date, end_date, makes_unusable, category) VALUES ('speaker repair', '2025-12-03', '2025-12-04', TRUE, 'repair')""",

#SUBCONTRACTOR
"""INSERT INTO SUBCONTRACTOR (c_name, c_phone, c_email) VALUES ('Hachiware Musk', '34671097', 'hachiwaremusk@gmail.com')""",
"""INSERT INTO SUBCONTRACTOR (c_name, c_phone, c_email) VALUES ('Elon Ma', '56846438', 'elonma@outlook.com')""",

#E_ASSIGNMENT
"""INSERT INTO E_ASSIGNMENT (a_id, e_id) VALUES ('1', '3')""", #1 for window cleaning, 3 for Garfield Rizz 
"""INSERT INTO E_ASSIGNMENT (a_id, e_id) VALUES ('2', '5')""", #2 for gate cleaning, 5 for Usagi Rabbit 
"""INSERT INTO E_ASSIGNMENT (a_id, e_id) VALUES ('3', '4')""", #3 for door repair, 4 for Quandale Fortnite

#C_ASSIGNMENT
"""INSERT INTO C_ASSIGNMENT (a_id, c_id) VALUES ('2', '1')""", #2 for gate cleaning, 1 for Hachiware Musk
"""INSERT INTO C_ASSIGNMENT (a_id, c_id) VALUES ('5', '2')""", #5 for speaker repair, 2 for Elon Ma

#CAMPUS_AREA
"""INSERT INTO CAMPUS_AREA (area_id, area_name, area_type, last_maintenance_date) VALUES ('1', 'front gate', 'outdoors', '2025-11-20')""",
"""INSERT INTO CAMPUS_AREA (area_id, area_name, area_type, last_maintenance_date) VALUES ('2', 'class room 5', 'indoors', '2025-11-17')""",
"""INSERT INTO CAMPUS_AREA (area_id, area_name, area_type, last_maintenance_date) VALUES ('3', 'office', 'indoors', '2025-11-18')""",

#ACTIVITY_LOCATIONS | location id > Campus Area
"""INSERT INTO ACTIVITY_LOCATIONS (location_id, a_id) VALUES ('1', '2')""", # front gate for gate cleaning
"""INSERT INTO ACTIVITY_LOCATIONS (location_id, a_id) VALUES ('2', '1')""", # class room 5 for window cleaning
"""INSERT INTO ACTIVITY_LOCATIONS (location_id, a_id) VALUES ('2', '3')""", # class room 5 for door repair
"""INSERT INTO ACTIVITY_LOCATIONS (location_id, a_id) VALUES ('3', '4')""", # office for light repair
"""INSERT INTO ACTIVITY_LOCATIONS (location_id, a_id) VALUES ('2', '5')""", # class room 5 for speaker repair

#CHEMICALS
"""INSERT INTO CHEMICALS (chemical_id, chemical_name, is_harmful) VALUES ('1', 'windex', TRUE)""",
"""INSERT INTO CHEMICALS (chemical_id, chemical_name, is_harmful) VALUES ('2', 'soap mix', FALSE)""",
"""INSERT INTO CHEMICALS (chemical_id, chemical_name, is_harmful) VALUES ('3', 'degreaser', TRUE)""",
"""INSERT INTO CHEMICALS (chemical_id, chemical_name, is_harmful) VALUES ('4', 'lubricant oil', FALSE)""",

#CHEMICAL_USAGE
"""INSERT INTO CHEMICAL_USAGE (chemical_id, a_id) VALUES ('1', '1')""",
"""INSERT INTO CHEMICAL_USAGE (chemical_id, a_id) VALUES ('2', '2')""",
"""INSERT INTO CHEMICAL_USAGE (chemical_id, a_id) VALUES ('4', '3')""",

#BUILDING_SUPERVISION
"""INSERT INTO BUILDING_SUPERVISION (building_id, e_id) VALUES ('1', '4')""", #1 for front gate, 4 for quandale fortnite
"""INSERT INTO BUILDING_SUPERVISION (building_id, e_id) VALUES ('2', '3')""", #2 for class room 5, 3 for garfield rizz
"""INSERT INTO BUILDING_SUPERVISION (building_id, e_id) VALUES ('3', '5')"""  #3 for office, 5 for usagi rabbit

]