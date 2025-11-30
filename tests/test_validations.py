"""
Tests for validations.py
"""
import pytest
from unittest.mock import patch
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from validations import GeneralValidator, CampusRules, EmployeeLimitValidator


class TestGeneralValidator:
    """Test cases for GeneralValidator class"""
    
    def test_validate_phone_valid(self):
        """Test valid phone number"""
        phone = '12345678'
        result = GeneralValidator.validate_phone(phone)
        assert result == '12345678'
    
    def test_validate_phone_too_short(self):
        """Test phone number that is too short"""
        phone = '1234567'
        try:
            GeneralValidator.validate_phone(phone)
            # If we get here, the test failed
            assert False, "Should have raised ValueError"
        except ValueError as e:
            # Check the error message
            assert "Phone number must be exactly 8 digits" in str(e)
    
    def test_validate_phone_too_long(self):
        """Test phone number that is too long"""
        phone = '123456789'
        try:
            GeneralValidator.validate_phone(phone)
            # If we get here, the test failed
            assert False, "Should have raised ValueError"
        except ValueError as e:
            # Check the error message
            assert "Phone number must be exactly 8 digits" in str(e)
    
    def test_validate_phone_has_letters(self):
        """Test phone number with letters"""
        phone = '1234567a'
        try:
            GeneralValidator.validate_phone(phone)
            # If we get here, the test failed
            assert False, "Should have raised ValueError"
        except ValueError:
            # This is expected, test passes
            pass
    
    def test_validate_phone_has_dash(self):
        """Test phone number with dash"""
        phone = '1234-5678'
        try:
            GeneralValidator.validate_phone(phone)
            # If we get here, the test failed
            assert False, "Should have raised ValueError"
        except ValueError:
            # This is expected, test passes
            pass
    
    def test_validate_email_valid_simple(self):
        """Test valid simple email"""
        email = 'test@example.com'
        result = GeneralValidator.validate_email(email)
        assert result == 'test@example.com'
    
    def test_validate_email_valid_complex(self):
        """Test valid complex email"""
        email = 'user.name@domain.co.uk'
        result = GeneralValidator.validate_email(email)
        assert result == 'user.name@domain.co.uk'
    
    def test_validate_email_invalid_no_at(self):
        """Test invalid email with no @ symbol"""
        email = 'invalid'
        try:
            GeneralValidator.validate_email(email)
            assert False, "Should have raised ValueError"
        except ValueError as e:
            assert "Invalid email format" in str(e)
    
    def test_validate_email_invalid_no_domain(self):
        """Test invalid email with no domain"""
        email = 'invalid@'
        try:
            GeneralValidator.validate_email(email)
            assert False, "Should have raised ValueError"
        except ValueError as e:
            assert "Invalid email format" in str(e)
    
    def test_validate_email_invalid_no_username(self):
        """Test invalid email with no username"""
        email = '@example.com'
        try:
            GeneralValidator.validate_email(email)
            assert False, "Should have raised ValueError"
        except ValueError as e:
            assert "Invalid email format" in str(e)
    
    def test_validate_email_empty(self):
        """Test empty email (should be allowed)"""
        assert GeneralValidator.validate_email('') == ''
        assert GeneralValidator.validate_email(None) is None
    
    def test_validate_date_valid(self):
        """Test valid date format"""
        date = '2025-01-01'
        result = GeneralValidator.validate_date(date)
        assert result == '2025-01-01'
    
    def test_validate_date_valid_different_date(self):
        """Test another valid date"""
        date = '2024-12-31'
        result = GeneralValidator.validate_date(date)
        assert result == '2024-12-31'
    
    def test_validate_date_invalid_wrong_format(self):
        """Test invalid date format (DD-MM-YYYY)"""
        date = '01-01-2025'
        try:
            GeneralValidator.validate_date(date)
            assert False, "Should have raised ValueError"
        except ValueError as e:
            assert "Date must be in YYYY-MM-DD" in str(e)
    
    def test_validate_date_invalid_slash_format(self):
        """Test invalid date format with slashes"""
        date = '2025/01/01'
        try:
            GeneralValidator.validate_date(date)
            assert False, "Should have raised ValueError"
        except ValueError as e:
            assert "Date must be in YYYY-MM-DD" in str(e)
    
    def test_validate_date_invalid_text(self):
        """Test invalid date that is just text"""
        date = 'invalid'
        try:
            GeneralValidator.validate_date(date)
            assert False, "Should have raised ValueError"
        except ValueError as e:
            assert "Date must be in YYYY-MM-DD" in str(e)
    
    def test_validate_date_range_valid(self):
        """Test valid date range"""
        start_date = '2025-01-01'
        end_date = '2025-01-02'
        result = GeneralValidator.validate_date_range(start_date, end_date)
        assert result == True
    
    def test_validate_date_range_valid_different_months(self):
        """Test valid date range across months"""
        start_date = '2024-12-01'
        end_date = '2025-01-01'
        result = GeneralValidator.validate_date_range(start_date, end_date)
        assert result == True
    
    def test_validate_date_range_invalid_end_before_start(self):
        """Test invalid date range where end is before start"""
        start_date = '2025-01-02'
        end_date = '2025-01-01'
        try:
            GeneralValidator.validate_date_range(start_date, end_date)
            assert False, "Should have raised ValueError"
        except ValueError as e:
            assert "End date must be after start date" in str(e)
    
    def test_validate_date_range_invalid_same_date(self):
        """Test invalid date range where end equals start"""
        start_date = '2025-01-01'
        end_date = '2025-01-01'
        try:
            GeneralValidator.validate_date_range(start_date, end_date)
            assert False, "Should have raised ValueError"
        except ValueError as e:
            assert "End date must be after start date" in str(e)
    
    def test_validate_boolean_true_lowercase(self):
        """Test boolean validation for 'true'"""
        result = GeneralValidator.validate_boolean('true')
        assert result == '1'
    
    def test_validate_boolean_true_uppercase(self):
        """Test boolean validation for 'TRUE'"""
        result = GeneralValidator.validate_boolean('TRUE')
        assert result == '1'
    
    def test_validate_boolean_true_letter_t(self):
        """Test boolean validation for 't'"""
        result = GeneralValidator.validate_boolean('t')
        assert result == '1'
    
    def test_validate_boolean_true_yes(self):
        """Test boolean validation for 'yes'"""
        result = GeneralValidator.validate_boolean('yes')
        assert result == '1'
    
    def test_validate_boolean_true_letter_y(self):
        """Test boolean validation for 'y'"""
        result = GeneralValidator.validate_boolean('y')
        assert result == '1'
    
    def test_validate_boolean_true_one(self):
        """Test boolean validation for '1'"""
        result = GeneralValidator.validate_boolean('1')
        assert result == '1'
    
    def test_validate_boolean_false_lowercase(self):
        """Test boolean validation for 'false'"""
        result = GeneralValidator.validate_boolean('false')
        assert result == '0'
    
    def test_validate_boolean_false_uppercase(self):
        """Test boolean validation for 'FALSE'"""
        result = GeneralValidator.validate_boolean('FALSE')
        assert result == '0'
    
    def test_validate_boolean_false_letter_f(self):
        """Test boolean validation for 'f'"""
        result = GeneralValidator.validate_boolean('f')
        assert result == '0'
    
    def test_validate_boolean_false_no(self):
        """Test boolean validation for 'no'"""
        result = GeneralValidator.validate_boolean('no')
        assert result == '0'
    
    def test_validate_boolean_false_letter_n(self):
        """Test boolean validation for 'n'"""
        result = GeneralValidator.validate_boolean('n')
        assert result == '0'
    
    def test_validate_boolean_false_zero(self):
        """Test boolean validation for '0'"""
        result = GeneralValidator.validate_boolean('0')
        assert result == '0'
    
    def test_validate_boolean_invalid_maybe(self):
        """Test invalid boolean value 'maybe'"""
        try:
            GeneralValidator.validate_boolean('maybe')
            assert False, "Should have raised ValueError"
        except ValueError as e:
            assert "Must be true/false" in str(e)
    
    def test_validate_boolean_invalid_number(self):
        """Test invalid boolean value '2'"""
        try:
            GeneralValidator.validate_boolean('2')
            assert False, "Should have raised ValueError"
        except ValueError as e:
            assert "Must be true/false" in str(e)
    
    def test_validate_level_executive_officer(self):
        """Test valid executive officer level"""
        level = 'executive officer'
        result = GeneralValidator.validate_level(level)
        assert result == 'executive officer'
    
    def test_validate_level_mid_level_manager(self):
        """Test valid mid-level manager level"""
        level = 'mid-level manager'
        result = GeneralValidator.validate_level(level)
        assert result == 'mid-level manager'
    
    def test_validate_level_base_level_worker(self):
        """Test valid base-level worker level"""
        level = 'base-level worker'
        result = GeneralValidator.validate_level(level)
        assert result == 'base-level worker'
    
    def test_validate_level_invalid_text(self):
        """Test invalid level 'invalid'"""
        level = 'invalid'
        try:
            GeneralValidator.validate_level(level)
            assert False, "Should have raised ValueError"
        except ValueError:
            # This is expected, test passes
            pass
    
    def test_validate_level_invalid_partial(self):
        """Test invalid level 'manager' (partial match)"""
        level = 'manager'
        try:
            GeneralValidator.validate_level(level)
            assert False, "Should have raised ValueError"
        except ValueError:
            # This is expected, test passes
            pass
    
    def test_validate_area_type_room(self):
        """Test valid area type 'room'"""
        area_type = 'room'
        result = GeneralValidator.validate_area_type(area_type)
        assert result == 'room'
    
    def test_validate_area_type_level(self):
        """Test valid area type 'level'"""
        area_type = 'level'
        result = GeneralValidator.validate_area_type(area_type)
        assert result == 'level'
    
    def test_validate_area_type_building(self):
        """Test valid area type 'building'"""
        area_type = 'building'
        result = GeneralValidator.validate_area_type(area_type)
        assert result == 'building'
    
    def test_validate_area_type_square(self):
        """Test valid area type 'square'"""
        area_type = 'square'
        result = GeneralValidator.validate_area_type(area_type)
        assert result == 'square'
    
    def test_validate_area_type_gate(self):
        """Test valid area type 'gate'"""
        area_type = 'gate'
        result = GeneralValidator.validate_area_type(area_type)
        assert result == 'gate'
    
    def test_validate_area_type_invalid(self):
        """Test invalid area type"""
        area_type = 'invalid'
        try:
            GeneralValidator.validate_area_type(area_type)
            assert False, "Should have raised ValueError"
        except ValueError:
            # This is expected, test passes
            pass
    
    def test_validate_area_type_invalid_office(self):
        """Test invalid area type 'office'"""
        area_type = 'office'
        try:
            GeneralValidator.validate_area_type(area_type)
            assert False, "Should have raised ValueError"
        except ValueError:
            # This is expected, test passes
            pass
    
    def test_validate_category_cleaning(self):
        """Test valid category 'cleaning'"""
        category = 'cleaning'
        result = GeneralValidator.validate_category(category)
        assert result == 'cleaning'
    
    def test_validate_category_repair(self):
        """Test valid category 'repair'"""
        category = 'repair'
        result = GeneralValidator.validate_category(category)
        assert result == 'repair'
    
    def test_validate_category_renovation(self):
        """Test valid category 'renovation'"""
        category = 'renovation'
        result = GeneralValidator.validate_category(category)
        assert result == 'renovation'
    
    def test_validate_category_invalid(self):
        """Test invalid category"""
        category = 'invalid'
        try:
            GeneralValidator.validate_category(category)
            assert False, "Should have raised ValueError"
        except ValueError:
            # This is expected, test passes
            pass
    
    def test_validate_category_invalid_maintenance(self):
        """Test invalid category 'maintenance'"""
        category = 'maintenance'
        try:
            GeneralValidator.validate_category(category)
            assert False, "Should have raised ValueError"
        except ValueError:
            # This is expected, test passes
            pass


class TestCampusRules:
    """Test cases for CampusRules class"""
    
    @patch('validations.cur')
    def test_validate_supervisor_hierarchy_no_supervisor_none(self, mock_cur):
        """Test validation when employee has no supervisor (None)"""
        result = CampusRules.validate_supervisor_hierarchy('1', None)
        is_valid = result[0]
        message = result[1]
        
        # Should be valid when no supervisor
        assert is_valid == True
        assert "No supervisor" in message
    
    @patch('validations.cur')
    def test_validate_supervisor_hierarchy_no_supervisor_empty(self, mock_cur):
        """Test validation when employee has no supervisor (empty string)"""
        result = CampusRules.validate_supervisor_hierarchy('1', '')
        is_valid = result[0]
        
        # Should be valid when supervisor is empty string
        assert is_valid == True
    
    @patch('validations.cur')
    def test_validate_supervisor_hierarchy_no_supervisor_null(self, mock_cur):
        """Test validation when employee has no supervisor (NULL string)"""
        result = CampusRules.validate_supervisor_hierarchy('1', 'NULL')
        is_valid = result[0]
        
        # Should be valid when supervisor is 'NULL'
        assert is_valid == True
    
    @patch('validations.cur')
    def test_validate_supervisor_hierarchy_executive_officer(self, mock_cur):
        """Test that executive officers cannot have supervisors"""
        mock_cur.fetchone.return_value = ('executive officer',)
        is_valid, message = CampusRules.validate_supervisor_hierarchy('1', '2', 'executive officer')
        assert is_valid is False
        assert "Executive officer cannot have a supervisor" in message
    
    @patch('validations.cur')
    def test_validate_supervisor_hierarchy_mid_level_manager_valid(self, mock_cur):
        """Test mid-level manager supervised by executive officer (valid)"""
        # Set up mock to return executive officer level
        mock_cur.fetchone.return_value = ('executive officer',)
        
        # Test the validation
        result = CampusRules.validate_supervisor_hierarchy('2', '1', 'mid-level manager')
        is_valid = result[0]
        
        # Should be valid
        assert is_valid == True
    
    @patch('validations.cur')
    def test_validate_supervisor_hierarchy_mid_level_manager_invalid(self, mock_cur):
        """Test mid-level manager supervised by another mid-level manager (invalid)"""
        # Set up mock to return mid-level manager level
        mock_cur.fetchone.return_value = ('mid-level manager',)
        
        # Test the validation
        result = CampusRules.validate_supervisor_hierarchy('2', '3', 'mid-level manager')
        is_valid = result[0]
        message = result[1]
        
        # Should be invalid
        assert is_valid == False
        assert "Mid-level managers can only be supervised by executive officers" in message
    
    @patch('validations.cur')
    def test_validate_supervisor_hierarchy_base_level_worker_valid(self, mock_cur):
        """Test base-level worker supervised by mid-level manager (valid)"""
        # Set up mock to return mid-level manager level
        mock_cur.fetchone.return_value = ('mid-level manager',)
        
        # Test the validation
        result = CampusRules.validate_supervisor_hierarchy('3', '2', 'base-level worker')
        is_valid = result[0]
        
        # Should be valid
        assert is_valid == True
    
    @patch('validations.cur')
    def test_validate_supervisor_hierarchy_base_level_worker_invalid(self, mock_cur):
        """Test base-level worker supervised by executive officer (invalid)"""
        # Set up mock to return executive officer level
        mock_cur.fetchone.return_value = ('executive officer',)
        
        # Test the validation
        result = CampusRules.validate_supervisor_hierarchy('3', '1', 'base-level worker')
        is_valid = result[0]
        message = result[1]
        
        # Should be invalid
        assert is_valid == False
        assert "Base-level workers can only be supervised by mid-level managers" in message
    
    @patch('validations.cur')
    def test_validate_supervisor_hierarchy_employee_not_found(self, mock_cur):
        """Test validation when employee is not found"""
        mock_cur.fetchone.return_value = None
        is_valid, message = CampusRules.validate_supervisor_hierarchy('999', '1')
        assert is_valid is False
        assert "Employee not found" in message
    
    @patch('validations.cur')
    def test_validate_supervisor_hierarchy_supervisor_not_found(self, mock_cur):
        """Test validation when supervisor is not found"""
        # When employee_level is provided, only one database call is made (for supervisor)
        mock_cur.fetchone.return_value = None
        is_valid, message = CampusRules.validate_supervisor_hierarchy('2', '999', 'mid-level manager')
        assert is_valid is False
        assert "Supervisor not found" in message
    
    @patch('validations.cur')
    def test_validate_building_supervisor_valid(self, mock_cur):
        """Test valid building supervisor assignment"""
        mock_cur.fetchone.side_effect = [
            ('mid-level manager',),  # Employee level
            (0,),  # Employee not already supervising
            (0,),  # Building not already supervised
            ('building',)  # Area type
        ]
        is_valid, message = CampusRules.validate_building_supervisor(1, 2)
        assert is_valid is True
    
    @patch('validations.cur')
    def test_validate_building_supervisor_wrong_level(self, mock_cur):
        """Test building supervisor with wrong employee level"""
        mock_cur.fetchone.return_value = ('base-level worker',)
        is_valid, message = CampusRules.validate_building_supervisor(1, 2)
        assert is_valid is False
        assert "Only mid-level managers can supervise buildings" in message
    
    @patch('validations.cur')
    def test_validate_building_supervisor_already_supervising(self, mock_cur):
        """Test building supervisor already supervising another building"""
        mock_cur.fetchone.side_effect = [
            ('mid-level manager',),
            (1,)  # Already supervising
        ]
        is_valid, message = CampusRules.validate_building_supervisor(1, 2)
        assert is_valid is False
        assert "already supervises a building" in message
    
    @patch('validations.cur')
    def test_validate_building_supervisor_building_has_supervisor(self, mock_cur):
        """Test building that already has a supervisor"""
        mock_cur.fetchone.side_effect = [
            ('mid-level manager',),
            (0,),  # Employee not supervising
            (1,)  # Building already has supervisor
        ]
        is_valid, message = CampusRules.validate_building_supervisor(1, 2)
        assert is_valid is False
        assert "already has a supervisor" in message
    
    @patch('validations.cur')
    def test_validate_building_supervisor_not_building(self, mock_cur):
        """Test assigning supervisor to non-building area"""
        mock_cur.fetchone.side_effect = [
            ('mid-level manager',),
            (0,),
            (0,),
            ('room',)  # Not a building
        ]
        is_valid, message = CampusRules.validate_building_supervisor(1, 2)
        assert is_valid is False
        assert "Only buildings can have supervisors" in message
    
    @patch('validations.cur')
    def test_validate_activity_assignment_valid_employee(self, mock_cur):
        """Test valid activity assignment with employee"""
        mock_cur.fetchone.side_effect = [(1,), (1,)]  # Activity exists, employee exists
        is_valid, message = CampusRules.validate_activity_assignment(1, employee_id=2)
        assert is_valid is True
    
    @patch('validations.cur')
    def test_validate_activity_assignment_valid_subcontractor(self, mock_cur):
        """Test valid activity assignment with subcontractor"""
        mock_cur.fetchone.side_effect = [(1,), (1,)]  # Activity exists, subcontractor exists
        is_valid, message = CampusRules.validate_activity_assignment(1, subcontractor_id=2)
        assert is_valid is True
    
    @patch('validations.cur')
    def test_validate_activity_assignment_both_assigned(self, mock_cur):
        """Test invalid assignment with both employee and subcontractor"""
        is_valid, message = CampusRules.validate_activity_assignment(1, employee_id=2, subcontractor_id=3)
        assert is_valid is False
        assert "Cannot assign both employee and subcontractor" in message
    
    @patch('validations.cur')
    def test_validate_activity_assignment_activity_not_found(self, mock_cur):
        """Test assignment with non-existent activity"""
        mock_cur.fetchone.return_value = (0,)
        is_valid, message = CampusRules.validate_activity_assignment(999, employee_id=2)
        assert is_valid is False
        assert "Activity not found" in message
    
    def test_validate_activity_dates_valid(self):
        """Test valid activity date range"""
        is_valid, message = CampusRules.validate_activity_dates('2025-01-01', '2025-01-02')
        assert is_valid is True
    
    def test_validate_activity_dates_invalid(self):
        """Test invalid activity date range"""
        is_valid, message = CampusRules.validate_activity_dates('2025-01-02', '2025-01-01')
        assert is_valid is False
        assert "End date must be after start date" in message
    
    def test_validate_activity_dates_invalid_format(self):
        """Test invalid date format"""
        is_valid, message = CampusRules.validate_activity_dates('invalid', '2025-01-01')
        assert is_valid is False
        assert "Invalid date format" in message
    
    @patch('validations.cur')
    def test_validate_chemical_usage_valid(self, mock_cur):
        """Test valid chemical usage"""
        mock_cur.fetchone.side_effect = [(1,), (1,)]  # Chemical exists, activity exists
        is_valid, message = CampusRules.validate_chemical_usage(1, 2)
        assert is_valid is True
    
    @patch('validations.cur')
    def test_validate_chemical_usage_chemical_not_found(self, mock_cur):
        """Test chemical usage with non-existent chemical"""
        mock_cur.fetchone.return_value = (0,)
        is_valid, message = CampusRules.validate_chemical_usage(999, 1)
        assert is_valid is False
        assert "Chemical not found" in message
    
    @patch('validations.cur')
    def test_validate_activity_location_valid(self, mock_cur):
        """Test valid activity location"""
        mock_cur.fetchone.side_effect = [(1,), (1,)]  # Location exists, activity exists
        is_valid, message = CampusRules.validate_activity_location(1, 2)
        assert is_valid is True
    
    @patch('validations.cur')
    def test_validate_activity_location_not_found(self, mock_cur):
        """Test activity location with non-existent location"""
        mock_cur.fetchone.return_value = (0,)
        is_valid, message = CampusRules.validate_activity_location(999, 1)
        assert is_valid is False
        assert "Location not found" in message


class TestEmployeeLimitValidator:
    """Test cases for EmployeeLimitValidator class"""
    
    @patch('validations.cur')
    def test_check_employee_limits_mid_level_within_limit(self, mock_cur):
        """Test mid-level manager count within limit"""
        mock_cur.fetchone.return_value = (29,)  # Below limit of 30
        is_valid, message = EmployeeLimitValidator.check_employee_limits('mid-level manager')
        assert is_valid is True
    
    @patch('validations.cur')
    def test_check_employee_limits_mid_level_at_limit(self, mock_cur):
        """Test mid-level manager count at limit"""
        mock_cur.fetchone.return_value = (30,)  # At limit
        is_valid, message = EmployeeLimitValidator.check_employee_limits('mid-level manager')
        assert is_valid is False
        assert "Cannot exceed maximum of 30 mid-level managers" in message
    
    @patch('validations.cur')
    def test_check_employee_limits_base_level_within_limit(self, mock_cur):
        """Test base-level worker count within limit"""
        mock_cur.fetchone.return_value = (99,)  # Below limit of 100
        is_valid, message = EmployeeLimitValidator.check_employee_limits('base-level worker')
        assert is_valid is True
    
    @patch('validations.cur')
    def test_check_employee_limits_base_level_at_limit(self, mock_cur):
        """Test base-level worker count at limit"""
        mock_cur.fetchone.return_value = (100,)  # At limit
        is_valid, message = EmployeeLimitValidator.check_employee_limits('base-level worker')
        assert is_valid is False
        assert "Cannot exceed maximum of 100 base-level workers" in message
    
    @patch('validations.cur')
    def test_check_employee_limits_executive_officer(self, mock_cur):
        """Test executive officer (no limit)"""
        is_valid, message = EmployeeLimitValidator.check_employee_limits('executive officer')
        assert is_valid is True

