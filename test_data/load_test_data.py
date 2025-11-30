#!/usr/bin/env python3
"""
Test Data Loader Script for CMMS
=================================
This script loads comprehensive test data from test_data.sql into the database.

Usage:
    python test_data/load_test_data.py
    OR
    cd test_data && python load_test_data.py

Note: This will DELETE the existing database and create a fresh one with test data.
Make sure to backup your database.db file if you have important data!
"""

import os
import sys
import sqlite3
import time

# Add parent directory to path to import database_initialisations
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database_initialisations import table_definitions

def load_test_data():
    """Load test data from test_data.sql file"""
    
    # Get the script's directory and parent directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(script_dir)
    
    # Paths
    test_data_sql = os.path.join(script_dir, "test_data.sql")
    database_path = os.path.join(parent_dir, "database.db")
    backup_path = os.path.join(parent_dir, "database_backup.db")
    
    # Check if test_data.sql exists
    if not os.path.exists(test_data_sql):
        print("❌ Error: test_data.sql file not found!")
        print(f"   Expected location: {test_data_sql}")
        return False
    
    # Remove existing database if it exists (handles file in use)
    if os.path.exists(database_path):
        try:
            # Try to remove the database file directly
            os.remove(database_path)
            print("🗑️  Removed existing database file")
        except PermissionError:
            print("❌ Error: Database file is currently in use by another process.")
            print("💡 Please close all applications that might be using the database:")
            print("   - Close any running Python scripts")
            print("   - Close any database viewers")
            print("   - Make sure main.py is not running")
            return False
    
    # Remove backup if it exists
    if os.path.exists(backup_path):
        try:
            os.remove(backup_path)
        except:
            pass  # Ignore errors removing backup
    
    # Create new database connection
    try:
        con = sqlite3.connect(database_path)
        cur = con.cursor()
    except sqlite3.Error as e:
        print(f"❌ Error creating database connection: {e}")
        return False
    
    try:
        print("🔨 Creating database tables...")
        # Create all tables
        for table in table_definitions:
            try:
                cur.execute(table)
            except sqlite3.Error as e:
                print(f"❌ Error creating table: {e}")
                return False
        con.commit()
        print("✅ Tables created successfully")
        
        print("\n📥 Loading test data from test_data.sql...")
        
        # Check if SQL file exists and has content
        if not os.path.exists(test_data_sql):
            print(f"❌ Error: {test_data_sql} not found!")
            return False
        
        # Read and execute SQL file
        with open(test_data_sql, "r", encoding="utf-8") as f:
            sql_script = f.read()
        
        if not sql_script.strip():
            print("❌ Error: test_data.sql file is empty!")
            return False
        
        # Use executescript which handles multiple statements better
        try:
            cur.executescript(sql_script)
            con.commit()
            print("✅ Test data loaded successfully!")
        except sqlite3.Error as e:
            print(f"❌ SQL Error executing script: {e}")
            return False
        
        # Verify data was loaded
        print("\n🔍 Verifying loaded data...")
        tables_to_check = [
            'EMPLOYEE', 'CMM_ACTIVITY', 'CAMPUS_AREA', 'SUBCONTRACTOR',
            'E_ASSIGNMENT', 'C_ASSIGNMENT', 'ACTIVITY_LOCATIONS',
            'CHEMICALS', 'CHEMICAL_USAGE', 'BUILDING_SUPERVISION'
        ]
        
        print("\n📊 Data Summary:")
        print("-" * 50)
        total_records = 0
        for table in tables_to_check:
            try:
                cur.execute(f"SELECT COUNT(*) FROM {table}")
                count = cur.fetchone()[0]
                total_records += count
                print(f"   {table:25s}: {count:3d} records")
            except sqlite3.Error as e:
                print(f"   {table:25s}: Error - {e}")
        
        print("-" * 50)
        print(f"   {'TOTAL':25s}: {total_records:3d} records")
        print("\n✅ Test data loaded successfully!")
        print("🚀 You can now run: python main.py")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        return False
    finally:
        con.close()

if __name__ == "__main__":
    print("=" * 60)
    print("CMMS Test Data Loader")
    print("=" * 60)
    print()
    
    # Confirm before proceeding
    response = input("⚠️  This will DELETE your existing database and create a new one with test data.\n   Continue? (yes/no): ")
    
    if response.lower() in ['yes', 'y']:
        print()
        success = load_test_data()
        if not success:
            print("\n❌ Failed to load test data. Please check the error messages above.")
            sys.exit(1)
    else:
        print("\n❌ Operation cancelled.")
        sys.exit(0)
