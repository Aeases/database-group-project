"""
Tests for utils.py
"""
import pytest
from unittest.mock import patch
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils import (
    getTableNames, getTableColumns, getTablePrimaryColumns,
    getUserPrimaryColumns, searchPkToWhereClause, searchForRecord,
    getUserInput, getUserBinaryInput, escapeString, getTableUserInput
)


class TestTableInfoFunctions:
    """Test cases for table information functions"""
    
    @patch('utils.cur')
    def test_getTableNames(self, mock_cur):
        """Test getting table names"""
        mock_cur.fetchall.return_value = [('EMPLOYEE',), ('CMM_ACTIVITY',), ('SUBCONTRACTOR',)]
        tables = getTableNames()
        assert 'EMPLOYEE' in tables
        assert 'CMM_ACTIVITY' in tables
        assert 'SUBCONTRACTOR' in tables
        mock_cur.execute.assert_called_once_with("SELECT name FROM sqlite_master WHERE type='table'")
    
    @patch('utils.cur')
    def test_getTableColumns(self, mock_cur):
        """Test getting table columns"""
        mock_cur.fetchall.return_value = [
            (0, 'employee_id', 'INTEGER', 0, None, 1),
            (1, 'e_name', 'VARCHAR(30)', 1, None, 0),
            (2, 'e_phone', 'VARCHAR(8)', 1, None, 0)
        ]
        columns = getTableColumns('EMPLOYEE')
        assert 'employee_id' in columns
        assert 'e_name' in columns
        assert 'e_phone' in columns
        mock_cur.execute.assert_called_once_with("PRAGMA table_info(EMPLOYEE)")
    
    @patch('utils.cur')
    def test_getTablePrimaryColumns_single(self, mock_cur):
        """Test getting single primary key column"""
        mock_cur.fetchall.return_value = [('employee_id',)]
        primary_keys = getTablePrimaryColumns('EMPLOYEE')
        assert primary_keys == ['employee_id']
    
    @patch('utils.cur')
    def test_getTablePrimaryColumns_multiple(self, mock_cur):
        """Test getting multiple primary key columns"""
        mock_cur.fetchall.return_value = [('location_id',), ('a_id',)]
        primary_keys = getTablePrimaryColumns('ACTIVITY_LOCATIONS')
        assert 'location_id' in primary_keys
        assert 'a_id' in primary_keys
        assert len(primary_keys) == 2


class TestSearchFunctions:
    """Test cases for search functions"""
    
    @patch('utils.getUserInput')
    @patch('utils.getTablePrimaryColumns')
    def test_getUserPrimaryColumns_single(self, mock_get_primary, mock_get_input):
        """Test getting user input for single primary key"""
        mock_get_primary.return_value = ['employee_id']
        mock_get_input.return_value = '1'
        result = getUserPrimaryColumns('EMPLOYEE')
        assert result == ['1']
    
    @patch('utils.getUserInput')
    @patch('utils.getTablePrimaryColumns')
    def test_getUserPrimaryColumns_multiple(self, mock_get_primary, mock_get_input):
        """Test getting user input for multiple primary keys"""
        mock_get_primary.return_value = ['location_id', 'a_id']
        mock_get_input.side_effect = ['1', '2']
        result = getUserPrimaryColumns('ACTIVITY_LOCATIONS')
        assert result == ['1', '2']
    
    def test_searchPkToWhereClause_single(self):
        """Test WHERE clause generation for single primary key"""
        where_clause = searchPkToWhereClause('EMPLOYEE', ['1'])
        assert where_clause == 'employee_id = 1'
    
    def test_searchPkToWhereClause_multiple(self):
        """Test WHERE clause generation for multiple primary keys"""
        where_clause = searchPkToWhereClause('ACTIVITY_LOCATIONS', ['1', '2'])
        assert 'location_id = 1' in where_clause
        assert 'a_id = 2' in where_clause
        assert ' AND ' in where_clause
    
    @patch('utils.cur')
    @patch('utils.searchPkToWhereClause')
    def test_searchForRecord(self, mock_where, mock_cur):
        """Test searching for a record"""
        mock_where.return_value = 'employee_id = 1'
        mock_cur.fetchall.return_value = [(1, 'John Doe', '12345678', 'john@test.com', None, 'executive officer')]
        
        result = searchForRecord('EMPLOYEE', ['1'])
        assert result[0] == 1
        assert result[1] == 'John Doe'
        mock_cur.execute.assert_called_once_with('SELECT * FROM EMPLOYEE WHERE employee_id = 1')


class TestUserInputFunctions:
    """Test cases for user input functions"""
    
    @patch('builtins.input')
    @patch('builtins.print')
    def test_getUserInput(self, mock_print, mock_input):
        """Test getting user input"""
        mock_input.return_value = 'test input'
        result = getUserInput('Enter value: ')
        assert result == 'test input'
        mock_input.assert_called_once()
    
    
    @patch('utils.getUserInput')
    def test_getUserBinaryInput_true(self, mock_get_input):
        """Test binary input returning True"""
        true_values = ['y', 'Y', 'yes', 'YES', 'true', 'TRUE', 't', 'T', '1']
        for value in true_values:
            mock_get_input.return_value = value
            result = getUserBinaryInput('Yes or No? ')
            assert result is True
    
    @patch('utils.getUserInput')
    @patch('builtins.print')
    def test_getUserBinaryInput_false(self, mock_print, mock_get_input):
        """Test binary input returning False"""
        false_values = ['n', 'N', 'no', 'NO', 'false', 'FALSE', 'f', 'F', '0']
        for value in false_values:
            mock_get_input.return_value = value
            result = getUserBinaryInput('Yes or No? ')
            assert result is False
    
    @patch('utils.getUserInput')
    @patch('builtins.print')
    def test_getUserBinaryInput_invalid(self, mock_print, mock_get_input):
        """Test binary input with invalid value"""
        mock_get_input.side_effect = ['maybe', 'y']  # First invalid, then valid
        result = getUserBinaryInput('Yes or No? ')
        assert result is True
        mock_print.assert_called_with("Invalid Input")


class TestUtilityFunctions:
    """Test cases for utility functions"""
    
    def test_escapeString_integer(self):
        """Test escaping integer values"""
        assert escapeString(123) == 123
        assert escapeString(0) == 0
    
    def test_escapeString_string(self):
        """Test escaping string values"""
        assert escapeString('test') == "'test'"
        assert escapeString("test's") == "'test's'"
        assert escapeString('') == "''"
    
    @patch('utils.getUserInput')
    @patch('utils.getTableNames')
    @patch('builtins.print')
    def test_getTableUserInput_valid(self, mock_print, mock_get_tables, mock_get_input):
        """Test getting valid table name from user"""
        mock_get_tables.return_value = ['EMPLOYEE', 'CMM_ACTIVITY', 'SUBCONTRACTOR']
        mock_get_input.return_value = 'EMPLOYEE'
        result = getTableUserInput('Select table: ')
        assert result == 'EMPLOYEE'
    
    @patch('utils.getUserInput')
    @patch('utils.getTableNames')
    @patch('builtins.print')
    def test_getTableUserInput_invalid_then_valid(self, mock_print, mock_get_tables, mock_get_input):
        """Test getting invalid then valid table name"""
        mock_get_tables.return_value = ['EMPLOYEE', 'CMM_ACTIVITY']
        mock_get_input.side_effect = ['INVALID', 'EMPLOYEE']  # First invalid, then valid
        result = getTableUserInput('Select table: ')
        assert result == 'EMPLOYEE'
        assert mock_print.call_count >= 1  # Should print "Invalid Table Name"

