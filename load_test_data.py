"""
Script to load test data into the database
Run this script to populate the database with test data for demonstration
"""
import sqlite3
import os

def load_test_data():
    """Load test data from SQL file into the database"""
    
    # Check if database exists
    if not os.path.exists('database.db'):
        print("Error: database.db not found!")
        print("Please run database_initialisations.py first to create the database.")
        return False
    
    # Connect to database
    try:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        
        print("Loading test data from test_data/test_data.sql...")
        
        # Read and execute SQL file
        sql_file_path = os.path.join('test_data', 'test_data.sql')
        with open(sql_file_path, 'r', encoding='utf-8') as f:
            sql_script = f.read()
            # Split by semicolon and execute each statement
            statements = sql_script.split(';')
            for statement in statements:
                statement = statement.strip()
                # Skip empty statements and comments
                if statement and not statement.startswith('--') and not statement.startswith('='):
                    try:
                        cursor.execute(statement)
                    except sqlite3.Error as e:
                        # Skip errors for statements that might fail (like DELETE if tables are empty)
                        if 'DELETE' not in statement.upper():
                            print(f"Warning: {e}")
        
        conn.commit()
        
        # Verify data was loaded
        cursor.execute("SELECT COUNT(*) FROM EMPLOYEE")
        employee_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM CMM_ACTIVITY")
        activity_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM CAMPUS_AREA")
        area_count = cursor.fetchone()[0]
        
        print(f"\n✓ Test data loaded successfully!")
        print(f"  - Employees: {employee_count}")
        print(f"  - Activities: {activity_count}")
        print(f"  - Campus Areas: {area_count}")
        
        conn.close()
        return True
        
    except FileNotFoundError:
        print("Error: test_data/test_data.sql not found!")
        print("Please make sure the test_data folder exists and contains test_data.sql")
        return False
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("CMMS Test Data Loader")
    print("=" * 50)
    
    success = load_test_data()
    
    if success:
        print("\n✓ Database is ready for testing and demonstration!")
    else:
        print("\n✗ Failed to load test data. Please check the error messages above.")

