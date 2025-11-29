import re
from datetime import datetime
from db import cur, con

class GeneralValidator:
    @staticmethod
    def validate_phone(phone):
        if not re.match(r'^\d{8}$', phone):
            raise ValueError("Phone number must be exactly 8 digits")
        return phone

    @staticmethod
    def validate_email(email):
        if email and not re.match(r'^[^@]+@[^@]+\.[^@]+$', email):
            raise ValueError("Invalid email format")
        return email

    @staticmethod
    def validate_date(date_str):
        try:
            datetime.strptime(date_str, '%Y-%m-%d')
            return date_str
        except ValueError:
            raise ValueError("Date must be in YYYY-MM-DD")

    @staticmethod
    def validate_date_range(start_date, end_date):
        start = datetime.strptime(start_date, '%Y-%m-%d')
        end = datetime.strptime(end_date, '%Y-%m-%d')
        if end <= start:
            raise ValueError("End date must be after start date")
        return True

    @staticmethod
    def validate_boolean(value):
        if value.lower() in ['true', 't', 'yes', 'y', '1']:
            return '1'
        elif value.lower() in ['false', 'f', 'no', 'n', '0']:
            return '0'
        else:
            raise ValueError("Must be true/false, yes/no, or 1/0")

    @staticmethod
    def validate_level(level):
        valid_levels = ['executive officer', 'mid-level manager', 'base-level worker']
        if level not in valid_levels:
            raise ValueError(f"Level must be one of: {', '.join(valid_levels)}")
        return level

    @staticmethod
    def validate_area_type(area_type):
        valid_types = ['room', 'level', 'building', 'square', 'gate']
        if area_type not in valid_types:
            raise ValueError(f"Area type must be one of: {', '.join(valid_types)}")
        return area_type

    @staticmethod
    def validate_category(category):
        valid_categories = ['cleaning', 'repair', 'renovation']
        if category not in valid_categories:
            raise ValueError(f"Category must be one of: {', '.join(valid_categories)}")
        return category

class CampusRules:
    @classmethod
    def validate_supervisor_hierarchy(cls, employee_id, supervisor_id, employee_level=None):
        if not supervisor_id or supervisor_id == '' or supervisor_id == 'NULL':
            return True, "No supervisor (executive officer)"

        try:
            if employee_level:
                emp_level = employee_level
            else:
                cur.execute("SELECT level FROM EMPLOYEE WHERE employee_id = ?", (employee_id,))
                employee_result = cur.fetchone()
                if not employee_result:
                    return False, "Employee not found"
                emp_level = employee_result[0]

            cur.execute("SELECT level FROM EMPLOYEE WHERE employee_id = ?", (supervisor_id,))
            supervisor_result = cur.fetchone()
            if not supervisor_result:
                return False, "Supervisor not found"
            supervisor_level = supervisor_result[0]

            if emp_level == 'executive officer' and supervisor_id:
                return False, "Executive officer cannot have a supervisor"
            elif emp_level == 'mid-level manager' and supervisor_level != 'executive officer':
                return False, "Mid-level managers can only be supervised by executive officers"
            elif emp_level == 'base-level worker' and supervisor_level != 'mid-level manager':
                return False, "Base-level workers can only be supervised by mid-level managers"

            return True, "Valid supervisor hierarchy"

        except Exception as e:
            return False, f"Error validating hierarchy: {e}"

    @classmethod
    def validate_building_supervisor(cls, building_id, employee_id):
        """Validate building supervisor assignment"""
        try:
            cur.execute("SELECT level FROM EMPLOYEE WHERE employee_id = ?", (employee_id,))
            result = cur.fetchone()
            if not result:
                return False, "Employee not found"
            if result[0] != 'mid-level manager':
                return False, "Only mid-level managers can supervise buildings"

            cur.execute("SELECT COUNT(*) FROM BUILDING_SUPERVISION WHERE e_id = ?", (employee_id,))
            if cur.fetchone()[0] > 0:
                return False, "This manager already supervises a building"

            cur.execute("SELECT COUNT(*) FROM BUILDING_SUPERVISION WHERE building_id = ?", (building_id,))
            if cur.fetchone()[0] > 0:
                return False, "This building already has a supervisor"

            cur.execute("SELECT area_type FROM CAMPUS_AREA WHERE area_id = ?", (building_id,))
            building_result = cur.fetchone()
            if not building_result:
                return False, "Building not found"
            if building_result[0] != 'building':
                return False, "Only buildings can have supervisors"

            return True, "Valid building supervision assignment"

        except Exception as e:
            return False, f"Error validating building supervision: {e}"

    @classmethod
    def validate_activity_assignment(cls, activity_id, employee_id=None, subcontractor_id=None):
        try:
            cur.execute("SELECT COUNT(*) FROM CMM_ACTIVITY WHERE activity_id = ?", (activity_id,))
            if cur.fetchone()[0] == 0:
                return False, "Activity not found"

            if employee_id:
                cur.execute("SELECT COUNT(*) FROM EMPLOYEE WHERE employee_id = ?", (employee_id,))
                if cur.fetchone()[0] == 0:
                    return False, "Employee not found"

            if subcontractor_id:
                cur.execute("SELECT COUNT(*) FROM SUBCONTRACTOR WHERE c_id = ?", (subcontractor_id,))
                if cur.fetchone()[0] == 0:
                    return False, "Subcontractor not found"

            if employee_id and subcontractor_id:
                return False, "Cannot assign both employee and subcontractor in same assignment"

            return True, "Valid activity assignment"

        except Exception as e:
            return False, f"Error validating activity assignment: {e}"

    @classmethod
    def validate_activity_dates(cls, start_date, end_date):
        try:
            start = datetime.strptime(start_date, '%Y-%m-%d')
            end = datetime.strptime(end_date, '%Y-%m-%d')
            if end <= start:
                return False, "End date must be after start date"
            return True, "Valid date range"
        except ValueError as e:
            return False, f"Invalid date format: {e}"
        
    @classmethod
    def validate_chemical_usage(cls, chemical_id, activity_id):
        try:
            cur.execute("SELECT COUNT(*) FROM CHEMICALS WHERE chemical_id = ?", (chemical_id,))
            if cur.fetchone()[0] == 0:
                return False, "Chemical not found"

            cur.execute("SELECT COUNT(*) FROM CMM_ACTIVITY WHERE activity_id = ?", (activity_id,))
            if cur.fetchone()[0] == 0:
                return False, "Activity not found"

            return True, "Valid chemical usage"
        except Exception as e:
            return False, f"Error validating chemical usage: {e}"

    @classmethod
    def validate_activity_location(cls, location_id, activity_id):
        try:
            cur.execute("SELECT COUNT(*) FROM CAMPUS_AREA WHERE area_id = ?", (location_id,))
            if cur.fetchone()[0] == 0:
                return False, "Location not found"

            cur.execute("SELECT COUNT(*) FROM CMM_ACTIVITY WHERE activity_id = ?", (activity_id,))
            if cur.fetchone()[0] == 0:
                return False, "Activity not found"

            return True, "Valid activity location"
        except Exception as e:
            return False, f"Error validating activity location: {e}"

class EmployeeLimitValidator:
    MAX_MID_LEVEL_MANAGERS = 30
    MAX_BASE_LEVEL_WORKERS = 100

    @classmethod
    def check_employee_limits(cls, level, operation='insert'):
        try:
            if level == 'mid-level manager':
                cur.execute("SELECT COUNT(*) FROM EMPLOYEE WHERE level = 'mid-level manager'")
                count = cur.fetchone()[0]
                if operation == 'insert' and count >= cls.MAX_MID_LEVEL_MANAGERS:
                    return False, f"Cannot exceed maximum of {cls.MAX_MID_LEVEL_MANAGERS} mid-level managers"

            elif level == 'base-level worker':
                cur.execute("SELECT COUNT(*) FROM EMPLOYEE WHERE level = 'base-level worker'")
                count = cur.fetchone()[0]
                if operation == 'insert' and count >= cls.MAX_BASE_LEVEL_WORKERS:
                    return False, f"Cannot exceed maximum of {cls.MAX_BASE_LEVEL_WORKERS} base-level workers"

            return True, "Within limits"
        except Exception as e:
            return False, f"Error checking limits: {e}"
