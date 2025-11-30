"""
Tests for updating_tuples.py
"""
import pytest
from unittest.mock import patch
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from updating_tuples import (
    user_delete_tuple, user_update_tuple, 
    perform_update, perform_deletion
)


class TestUserDeleteTuple:
    """Test cases for user_delete_tuple function"""
    
    @patch('updating_tuples.getUserPrimaryColumns')
    @patch('updating_tuples.getTableColumns')
    @patch('updating_tuples.searchForRecord')
    @patch('updating_tuples.searchPkToWhereClause')
    @patch('updating_tuples.getUserBinaryInput')
    @patch('updating_tuples.con')
    @patch('builtins.print')
    def test_user_delete_tuple_confirm(self, mock_print, mock_con, mock_binary, 
                                      mock_where, mock_search, mock_columns, mock_primary):
        """Test deletion with user confirmation"""
        mock_primary.return_value = ['1']
        mock_columns.return_value = ['employee_id', 'e_name', 'e_phone']
        mock_search.return_value = (1, 'John Doe', '12345678')
        mock_where.return_value = 'employee_id = 1'
        mock_binary.return_value = True  # User confirms deletion
        
        user_delete_tuple('EMPLOYEE')
        mock_con.execute.assert_called_once()
    
    @patch('updating_tuples.getUserPrimaryColumns')
    @patch('updating_tuples.getTableColumns')
    @patch('updating_tuples.searchForRecord')
    @patch('updating_tuples.searchPkToWhereClause')
    @patch('updating_tuples.getUserBinaryInput')
    @patch('updating_tuples.con')
    def test_user_delete_tuple_cancel(self, mock_con, mock_binary, mock_where, 
                                      mock_search, mock_columns, mock_primary):
        """Test deletion cancellation"""
        mock_primary.return_value = ['1']
        mock_columns.return_value = ['employee_id', 'e_name']
        mock_search.return_value = (1, 'John Doe')
        mock_where.return_value = 'employee_id = 1'
        mock_binary.return_value = False  # User cancels
        
        user_delete_tuple('EMPLOYEE')
        mock_con.execute.assert_not_called()


class TestUserUpdateTuple:
    """Test cases for user_update_tuple function"""
    
    @patch('updating_tuples.getUserPrimaryColumns')
    @patch('updating_tuples.searchForRecord')
    @patch('updating_tuples.getTableColumns')
    @patch('updating_tuples.getUserInput')
    @patch('updating_tuples.perform_update')
    @patch('builtins.print')
    def test_user_update_tuple(self, mock_print, mock_update, mock_input, 
                              mock_columns, mock_search, mock_primary):
        """Test updating a tuple"""
        mock_primary.return_value = ['1']
        mock_columns.return_value = ['employee_id', 'e_name', 'e_phone']
        mock_search.return_value = (1, 'John Doe', '12345678')
        mock_input.side_effect = ['', '87654321', '']  # Only update phone
        
        result = user_update_tuple('EMPLOYEE')
        mock_update.assert_called_once()
        assert result is not None
    
    @patch('updating_tuples.getUserPrimaryColumns')
    @patch('updating_tuples.searchForRecord')
    @patch('updating_tuples.getTableColumns')
    @patch('updating_tuples.getUserInput')
    @patch('updating_tuples.perform_update')
    def test_user_update_tuple_no_changes(self, mock_update, mock_input, 
                                         mock_columns, mock_search, mock_primary):
        """Test update with no changes (all blank)"""
        mock_primary.return_value = ['1']
        mock_columns.return_value = ['employee_id', 'e_name', 'e_phone']
        mock_search.return_value = (1, 'John Doe', '12345678')
        mock_input.side_effect = ['', '', '']  # All blank
        
        user_update_tuple('EMPLOYEE')
        # Should still call perform_update, but with empty values
        mock_update.assert_called_once()


class TestPerformUpdate:
    """Test cases for perform_update function"""
    
    @patch('updating_tuples.getTableColumns')
    @patch('updating_tuples.escapeString')
    @patch('updating_tuples.searchPkToWhereClause')
    @patch('updating_tuples.con')
    def test_perform_update_single_field(self, mock_con, mock_where, mock_escape, mock_columns):
        """Test updating a single field"""
        mock_columns.return_value = ['employee_id', 'e_name', 'e_phone']
        mock_escape.side_effect = lambda x: f"'{x}'" if isinstance(x, str) else x
        mock_where.return_value = 'employee_id = 1'
        
        perform_update('EMPLOYEE', ['1'], ['', 'Jane Doe', ''])
        mock_con.execute.assert_called_once()
        call_args = mock_con.execute.call_args[0][0]
        assert 'e_name' in call_args
        assert 'Jane Doe' in call_args
    
    @patch('updating_tuples.getTableColumns')
    @patch('updating_tuples.escapeString')
    @patch('updating_tuples.searchPkToWhereClause')
    @patch('updating_tuples.con')
    def test_perform_update_multiple_fields(self, mock_con, mock_where, mock_escape, mock_columns):
        """Test updating multiple fields"""
        mock_columns.return_value = ['employee_id', 'e_name', 'e_phone']
        mock_escape.side_effect = lambda x: f"'{x}'" if isinstance(x, str) else x
        mock_where.return_value = 'employee_id = 1'
        
        perform_update('EMPLOYEE', ['1'], ['', 'Jane Doe', '87654321'])
        mock_con.execute.assert_called_once()
        call_args = mock_con.execute.call_args[0][0]
        assert 'e_name' in call_args
        assert 'e_phone' in call_args
    
    @patch('updating_tuples.getTableColumns')
    @patch('updating_tuples.escapeString')
    @patch('updating_tuples.searchPkToWhereClause')
    @patch('updating_tuples.con')
    def test_perform_update_no_changes(self, mock_con, mock_where, mock_escape, mock_columns):
        """Test update with no changes - should raise IndexError when set_clause is empty"""
        mock_columns.return_value = ['employee_id', 'e_name', 'e_phone']
        mock_where.return_value = 'employee_id = 1'
        
        with pytest.raises(IndexError):
            perform_update('EMPLOYEE', ['1'], ['', '', ''])


class TestPerformDeletion:
    """Test cases for perform_deletion function"""
    
    @patch('updating_tuples.searchPkToWhereClause')
    @patch('updating_tuples.con')
    def test_perform_deletion(self, mock_con, mock_where):
        """Test performing a deletion"""
        mock_where.return_value = 'employee_id = 1'
        
        perform_deletion('EMPLOYEE', ['1'])
        mock_con.execute.assert_called_once()
        call_args = mock_con.execute.call_args[0][0]
        assert 'DELETE FROM EMPLOYEE' in call_args
        assert 'employee_id = 1' in call_args
    
    @patch('updating_tuples.searchPkToWhereClause')
    @patch('updating_tuples.con')
    def test_perform_deletion_multiple_keys(self, mock_con, mock_where):
        """Test deletion with multiple primary keys"""
        mock_where.return_value = 'location_id = 1 AND a_id = 2'
        
        perform_deletion('ACTIVITY_LOCATIONS', ['1', '2'])
        mock_con.execute.assert_called_once()
        call_args = mock_con.execute.call_args[0][0]
        assert 'DELETE FROM ACTIVITY_LOCATIONS' in call_args
        assert 'location_id = 1' in call_args
        assert 'a_id = 2' in call_args

