"""
Shared test fixtures and configuration
"""
import pytest
import sqlite3
import os
import tempfile
from unittest.mock import Mock, patch
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

@pytest.fixture
def temp_db():
    """Create a temporary database for testing"""
    fd, db_path = tempfile.mkstemp(suffix='.db')
    os.close(fd)
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create minimal schema for testing
    cursor.execute("""
        CREATE TABLE EMPLOYEE(
            employee_id INTEGER PRIMARY KEY AUTOINCREMENT,
            e_name VARCHAR(30) NOT NULL, 
            e_phone VARCHAR(8) NOT NULL, 
            e_email VARCHAR(50),
            supervisor_id INTEGER,
            level VARCHAR(17) CHECK(level IN ('executive officer', 'mid-level manager', 'base-level worker')),
            FOREIGN KEY (supervisor_id) REFERENCES EMPLOYEE(employee_id) ON DELETE SET NULL
        )
    """)
    
    cursor.execute("""
        CREATE TABLE CMM_ACTIVITY(
            activity_id INTEGER PRIMARY KEY AUTOINCREMENT,
            activity_desc VARCHAR(100) NOT NULL,
            start_date DATE NOT NULL,
            end_date DATE NOT NULL,
            makes_unusable BOOLEAN NOT NULL DEFAULT 0,
            category VARCHAR(15) CHECK(category IN ('cleaning', 'repair', 'renovation'))
        )
    """)
    
    cursor.execute("""
        CREATE TABLE SUBCONTRACTOR(
            c_id INTEGER PRIMARY KEY AUTOINCREMENT,
            c_name VARCHAR(50) NOT NULL,
            c_phone VARCHAR(15) NOT NULL,
            c_email VARCHAR(100)
        )
    """)
    
    cursor.execute("""
        CREATE TABLE CAMPUS_AREA(
            area_id INTEGER PRIMARY KEY AUTOINCREMENT,
            area_name VARCHAR(15) NOT NULL,
            area_type VARCHAR(15) CHECK(area_type IN('room', 'level', 'building', 'square', 'gate')),
            last_maintenance_date DATE
        )
    """)
    
    cursor.execute("""
        CREATE TABLE E_ASSIGNMENT(
            a_id INTEGER NOT NULL, 
            e_id INTEGER NOT NULL,
            FOREIGN KEY (a_id) REFERENCES CMM_ACTIVITY(activity_id) ON DELETE RESTRICT,
            FOREIGN KEY (e_id) REFERENCES EMPLOYEE(employee_id) ON DELETE RESTRICT,
            PRIMARY KEY (a_id, e_id)
        )
    """)
    
    cursor.execute("""
        CREATE TABLE C_ASSIGNMENT(
            a_id INTEGER NOT NULL, 
            c_id INTEGER NOT NULL,
            FOREIGN KEY (a_id) REFERENCES CMM_ACTIVITY(activity_id) ON DELETE RESTRICT,
            FOREIGN KEY (c_id) REFERENCES SUBCONTRACTOR(c_id) ON DELETE RESTRICT,
            PRIMARY KEY (a_id, c_id)
        )
    """)
    
    cursor.execute("""
        CREATE TABLE ACTIVITY_LOCATIONS(
            location_id INTEGER, 
            a_id INTEGER,
            FOREIGN KEY (location_id) REFERENCES CAMPUS_AREA(area_id) ON DELETE RESTRICT,
            FOREIGN KEY (a_id) REFERENCES CMM_ACTIVITY(activity_id) ON DELETE RESTRICT,
            PRIMARY KEY (location_id, a_id)
        )
    """)
    
    cursor.execute("""
        CREATE TABLE CHEMICALS(
            chemical_id INTEGER PRIMARY KEY AUTOINCREMENT,
            chemical_name VARCHAR(15) NOT NULL,
            is_harmful BOOLEAN NOT NULL DEFAULT 0
        )
    """)
    
    cursor.execute("""
        CREATE TABLE CHEMICAL_USAGE(
            chemical_id INTEGER NOT NULL,
            a_id INTEGER NOT NULL,
            FOREIGN KEY (chemical_id) REFERENCES CHEMICALS(chemical_id) ON DELETE RESTRICT,
            FOREIGN KEY (a_id) REFERENCES CMM_ACTIVITY(activity_id) ON DELETE RESTRICT,
            PRIMARY KEY (chemical_id, a_id)
        )
    """)
    
    cursor.execute("""
        CREATE TABLE BUILDING_SUPERVISION(
            building_id INTEGER NOT NULL UNIQUE,
            e_id INTEGER NOT NULL UNIQUE,
            FOREIGN KEY (building_id) REFERENCES CAMPUS_AREA(area_id) ON DELETE RESTRICT,
            FOREIGN KEY (e_id) REFERENCES EMPLOYEE(employee_id) ON DELETE RESTRICT,
            PRIMARY KEY (building_id, e_id)
        )
    """)
    
    # Insert test data
    cursor.execute("""
        INSERT INTO EMPLOYEE (e_name, e_phone, e_email, supervisor_id, level) 
        VALUES ('Test Executive', '12345678', 'exec@test.com', NULL, 'executive officer')
    """)
    
    cursor.execute("""
        INSERT INTO EMPLOYEE (e_name, e_phone, e_email, supervisor_id, level) 
        VALUES ('Test Manager', '87654321', 'manager@test.com', 1, 'mid-level manager')
    """)
    
    cursor.execute("""
        INSERT INTO EMPLOYEE (e_name, e_phone, e_email, supervisor_id, level) 
        VALUES ('Test Worker', '11111111', 'worker@test.com', 2, 'base-level worker')
    """)
    
    cursor.execute("""
        INSERT INTO CMM_ACTIVITY (activity_desc, start_date, end_date, makes_unusable, category) 
        VALUES ('test activity', '2025-01-01', '2025-01-02', 0, 'cleaning')
    """)
    
    cursor.execute("""
        INSERT INTO CAMPUS_AREA (area_name, area_type, last_maintenance_date) 
        VALUES ('Test Building', 'building', '2025-01-01')
    """)
    
    cursor.execute("""
        INSERT INTO CHEMICALS (chemical_name, is_harmful) 
        VALUES ('test_chemical', 0)
    """)
    
    conn.commit()
    
    yield conn, cursor
    
    conn.close()
    os.unlink(db_path)

@pytest.fixture
def mock_db():
    """Create mock database connection and cursor"""
    mock_conn = Mock()
    mock_cursor = Mock()
    mock_conn.cursor.return_value = mock_cursor
    return mock_conn, mock_cursor

