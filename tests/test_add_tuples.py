"""
Tests for add_tuples.py
"""
import pytest
from unittest.mock import patch
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from add_tuples import (
    get_validated_columns, validate_campus_rules, 
    add_tuple_to_sql, user_add_tuple, set_based_insertion
)


class TestGetValidatedColumns:
    """Test cases for get_validated_columns function"""
    
    @patch('add_tuples.getTableColumns')
    @patch('add_tuples.getUserInput')
    @patch('add_tuples.GeneralValidator')
    def test_get_validated_columns_phone(self, mock_validator, mock_input, mock_columns):
        """Test column validation for phone number"""
        # Set up mocks
        mock_columns.return_value = ['e_phone']
        mock_input.return_value = '12345678'
        mock_validator.validate_phone.return_value = '12345678'
        
        # Call the function
        result = get_validated_columns('EMPLOYEE')
        
        # Check the result
        assert result == ['12345678']
        # Check that validate_phone was called with the right value
        mock_validator.validate_phone.assert_called_once_with('12345678')
    
    @patch('add_tuples.getTableColumns')
    @patch('add_tuples.getUserInput')
    @patch('add_tuples.GeneralValidator')
    def test_get_validated_columns_email(self, mock_validator, mock_input, mock_columns):
        """Test column validation for email"""
        mock_columns.return_value = ['e_email']
        mock_input.return_value = 'test@example.com'
        mock_validator.validate_email.return_value = 'test@example.com'
        
        result = get_validated_columns('EMPLOYEE')
        assert result == ['test@example.com']
        mock_validator.validate_email.assert_called_once_with('test@example.com')
    
    @patch('add_tuples.getTableColumns')
    @patch('add_tuples.getUserInput')
    def test_get_validated_columns_supervisor_id_null(self, mock_input, mock_columns):
        """Test supervisor_id with empty value (NULL)"""
        mock_columns.return_value = ['supervisor_id']
        mock_input.return_value = ''
        
        result = get_validated_columns('EMPLOYEE')
        assert result == ['NULL']
    
    @patch('add_tuples.getTableColumns')
    @patch('add_tuples.getUserInput')
    @patch('add_tuples.GeneralValidator')
    def test_get_validated_columns_boolean(self, mock_validator, mock_input, mock_columns):
        """Test column validation for boolean"""
        mock_columns.return_value = ['makes_unusable']
        mock_input.return_value = 'true'
        mock_validator.validate_boolean.return_value = '1'
        
        result = get_validated_columns('CMM_ACTIVITY')
        assert result == ['1']
        mock_validator.validate_boolean.assert_called_once_with('true')
    
    @patch('add_tuples.getTableColumns')
    @patch('add_tuples.getUserInput')
    @patch('add_tuples.GeneralValidator')
    @patch('builtins.print')
    def test_get_validated_columns_validation_error(self, mock_print, mock_validator, mock_input, mock_columns):
        """Test handling of validation errors"""
        # Set up mocks
        mock_columns.return_value = ['e_phone']
        # First call returns invalid, second call returns valid
        mock_input.side_effect = ['invalid', '12345678']
        # First validation raises error, second returns valid value
        mock_validator.validate_phone.side_effect = [ValueError("Invalid phone"), '12345678']
        
        # Call the function
        result = get_validated_columns('EMPLOYEE')
        
        # Check that we eventually got a valid result
        assert result == ['12345678']
        # Check that print was called (to show error message)
        assert mock_print.called == True


class TestValidateCampusRules:
    """Test cases for validate_campus_rules function"""
    
    @patch('add_tuples.getTableColumns')
    @patch('add_tuples.EmployeeLimitValidator')
    def test_validate_campus_rules_employee_within_limit(self, mock_validator, mock_columns):
        """Test employee validation within limits"""
        mock_columns.return_value = ['e_name', 'e_phone', 'level']
        mock_validator.check_employee_limits.return_value = (True, "Within limits")
        
        item_data = ['John Doe', '12345678', 'mid-level manager']
        is_valid, message = validate_campus_rules('EMPLOYEE', item_data)
        assert is_valid is True
    
    @patch('add_tuples.getTableColumns')
    @patch('add_tuples.EmployeeLimitValidator')
    def test_validate_campus_rules_employee_exceeds_limit(self, mock_validator, mock_columns):
        """Test employee validation exceeding limits"""
        mock_columns.return_value = ['e_name', 'e_phone', 'level']
        mock_validator.check_employee_limits.return_value = (False, "Cannot exceed maximum")
        
        item_data = ['John Doe', '12345678', 'mid-level manager']
        is_valid, message = validate_campus_rules('EMPLOYEE', item_data)
        assert is_valid is False
        assert "Cannot exceed maximum" in message
    
    @patch('add_tuples.getTableColumns')
    @patch('add_tuples.CampusRules')
    def test_validate_campus_rules_building_supervision(self, mock_rules, mock_columns):
        """Test building supervision validation"""
        mock_columns.return_value = ['building_id', 'e_id']
        mock_rules.validate_building_supervisor.return_value = (True, "Valid")
        
        item_data = ['1', '2']
        is_valid, message = validate_campus_rules('BUILDING_SUPERVISION', item_data)
        assert is_valid is True
        mock_rules.validate_building_supervisor.assert_called_once_with('1', '2')
    
    @patch('add_tuples.getTableColumns')
    @patch('add_tuples.CampusRules')
    def test_validate_campus_rules_activity_dates(self, mock_rules, mock_columns):
        """Test activity date validation"""
        mock_columns.return_value = ['activity_desc', 'start_date', 'end_date', 'makes_unusable', 'category']
        mock_rules.validate_activity_dates.return_value = (True, "Valid date range")
        
        item_data = ['test', '2025-01-01', '2025-01-02', '0', 'cleaning']
        is_valid, message = validate_campus_rules('CMM_ACTIVITY', item_data)
        assert is_valid is True
        mock_rules.validate_activity_dates.assert_called_once_with('2025-01-01', '2025-01-02')
    
    @patch('add_tuples.getTableColumns')
    def test_validate_campus_rules_no_special_validation(self, mock_columns):
        """Test tables without special validation"""
        mock_columns.return_value = ['c_name', 'c_phone', 'c_email']
        
        item_data = ['Test Corp', '12345678', 'test@corp.com']
        is_valid, message = validate_campus_rules('SUBCONTRACTOR', item_data)
        assert is_valid is True
        assert "Validation passed" in message


class TestAddTupleToSQL:
    """Test cases for add_tuple_to_sql function"""
    
    @patch('add_tuples.getTableColumns')
    @patch('add_tuples.cur')
    @patch('add_tuples.con')
    @patch('add_tuples.escapeString')
    def test_add_tuple_to_sql_success(self, mock_escape, mock_con, mock_cur, mock_columns):
        """Test successful tuple insertion"""
        mock_columns.return_value = ['e_name', 'e_phone']
        mock_escape.side_effect = lambda x: f"'{x}'" if isinstance(x, str) else x
        
        result = add_tuple_to_sql('EMPLOYEE', ['John Doe', '12345678'])
        assert result is True
        mock_cur.execute.assert_called_once()
        mock_con.commit.assert_called_once()
    
    @patch('add_tuples.getTableColumns')
    @patch('add_tuples.cur')
    @patch('add_tuples.con')
    @patch('add_tuples.escapeString')
    @patch('builtins.print')
    def test_add_tuple_to_sql_failure(self, mock_print, mock_escape, mock_con, mock_cur, mock_columns):
        """Test failed tuple insertion"""
        mock_columns.return_value = ['e_name', 'e_phone']
        mock_escape.side_effect = lambda x: f"'{x}'" if isinstance(x, str) else x
        mock_cur.execute.side_effect = Exception("Database error")
        
        result = add_tuple_to_sql('EMPLOYEE', ['John Doe', '12345678'])
        assert result is False
        mock_con.rollback.assert_called_once()
        mock_print.assert_called()
    
    @patch('add_tuples.getTableColumns')
    @patch('add_tuples.cur')
    @patch('add_tuples.con')
    def test_add_tuple_to_sql_with_null(self, mock_con, mock_cur, mock_columns):
        """Test tuple insertion with NULL values"""
        mock_columns.return_value = ['e_name', 'e_phone', 'supervisor_id']
        
        result = add_tuple_to_sql('EMPLOYEE', ['John Doe', '12345678', 'NULL'])
        assert result is True
        # Check that NULL is handled correctly
        call_args = mock_cur.execute.call_args[0][1]
        assert 'NULL' in call_args


class TestUserAddTuple:
    """Test cases for user_add_tuple function"""
    
    @patch('add_tuples.getUserInput')
    @patch('add_tuples.get_validated_columns')
    @patch('add_tuples.validate_campus_rules')
    @patch('add_tuples.add_tuple_to_sql')
    @patch('builtins.print')
    def test_user_add_tuple_success(self, mock_print, mock_add, mock_validate, mock_get_cols, mock_input):
        """Test successful tuple addition"""
        mock_input.return_value = '1'  # Number of items
        mock_get_cols.return_value = ['John Doe', '12345678', 'test@test.com', 'NULL', 'executive officer']
        mock_validate.return_value = (True, "Valid")
        mock_add.return_value = True
        
        user_add_tuple('EMPLOYEE')
        mock_add.assert_called_once()
        assert any("successfully" in str(call).lower() for call in mock_print.call_args_list)
    
    @patch('add_tuples.getUserInput')
    @patch('add_tuples.get_validated_columns')
    @patch('add_tuples.validate_campus_rules')
    @patch('builtins.print')
    def test_user_add_tuple_validation_error(self, mock_print, mock_validate, mock_get_cols, mock_input):
        """Test tuple addition with validation error"""
        mock_input.return_value = '1'
        mock_get_cols.side_effect = ValueError("Invalid phone number")
        mock_validate.return_value = (True, "Valid")
        
        user_add_tuple('EMPLOYEE')
        # Should handle error gracefully
        assert any("error" in str(call).lower() or "validation" in str(call).lower() 
                  for call in mock_print.call_args_list)
    
    @patch('add_tuples.getUserInput')
    @patch('add_tuples.get_validated_columns')
    @patch('add_tuples.validate_campus_rules')
    @patch('builtins.print')
    def test_user_add_tuple_campus_rule_violation(self, mock_print, mock_validate, mock_get_cols, mock_input):
        """Test tuple addition with campus rule violation"""
        mock_input.return_value = '1'
        mock_get_cols.return_value = ['John Doe', '12345678', 'test@test.com', 'NULL', 'executive officer']
        mock_validate.return_value = (False, "Rule violation")
        
        user_add_tuple('EMPLOYEE')
        assert any("violation" in str(call).lower() for call in mock_print.call_args_list)


class TestSetBasedInsertion:
    """Test cases for set_based_insertion function"""
    
    @patch('add_tuples.getTableColumns')
    @patch('add_tuples.getUserInput')
    @patch('add_tuples.GeneralValidator')
    @patch('add_tuples.validate_campus_rules')
    @patch('add_tuples.add_tuple_to_sql')
    @patch('builtins.print')
    def test_set_based_insertion_success(self, mock_print, mock_add, mock_validate, 
                                         mock_validator, mock_input, mock_columns):
        """Test successful set-based insertion"""
        mock_columns.return_value = ['e_name', 'e_phone']
        mock_input.side_effect = ['John Doe,12345678', 'DONE', 'y']  # Row data, DONE, confirm
        mock_validator.validate_phone.return_value = '12345678'
        mock_validate.return_value = (True, "Valid")
        mock_add.return_value = True
        
        set_based_insertion('EMPLOYEE')
        mock_add.assert_called_once()
    
    @patch('add_tuples.getTableColumns')
    @patch('add_tuples.getUserInput')
    @patch('builtins.print')
    def test_set_based_insertion_cancel(self, mock_print, mock_input, mock_columns):
        """Test set-based insertion cancellation"""
        mock_columns.return_value = ['e_name', 'e_phone']
        mock_input.return_value = 'CANCEL'
        
        set_based_insertion('EMPLOYEE')
        assert any("cancelled" in str(call).lower() for call in mock_print.call_args_list)
    
    @patch('add_tuples.getTableColumns')
    @patch('add_tuples.getUserInput')
    @patch('builtins.print')
    def test_set_based_insertion_wrong_column_count(self, mock_print, mock_input, mock_columns):
        """Test set-based insertion with wrong number of columns"""
        mock_columns.return_value = ['e_name', 'e_phone', 'e_email']
        mock_input.side_effect = ['John Doe,12345678', 'DONE']  # Only 2 values for 3 columns
        
        set_based_insertion('EMPLOYEE')
        assert any("expected" in str(call).lower() or "values" in str(call).lower() 
                  for call in mock_print.call_args_list)

