"""
Tests for scheduled_activities.py
"""
import pytest
from unittest.mock import patch
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scheduled_activities import getScheduledActivities


class TestGetScheduledActivities:
    """Test cases for getScheduledActivities function"""
    
    @patch('scheduled_activities.getUserInput')
    @patch('scheduled_activities.cur')
    @patch('builtins.print')
    def test_getScheduledActivities_no_results(self, mock_print, mock_cur, mock_input):
        """Test when no activities are found"""
        # Set up mocks
        mock_input.side_effect = ['2025-01-01', '2025-12-31', 'NonExistent']
        mock_cur.fetchall.return_value = []  # No results
        
        # Call the function
        getScheduledActivities()
        
        # Check that "No matching activities" message was printed
        found_message = False
        for call in mock_print.call_args_list:
            call_str = str(call)
            if "No matching activities" in call_str:
                found_message = True
                break
        assert found_message == True
    
    @patch('scheduled_activities.getUserInput')
    @patch('scheduled_activities.cur')
    @patch('builtins.print')
    def test_getScheduledActivities_with_results(self, mock_print, mock_cur, mock_input):
        """Test when activities are found"""
        # Set up mocks
        mock_input.side_effect = ['2025-01-01', '2025-12-31', '']
        
        # Mock activity results - first call returns activities, second returns no chemicals, third returns assignments
        mock_cur.fetchall.side_effect = [
            [(1, 'window cleaning', '2025-11-25', '2025-11-26', 1, 'cleaning', 1, 'Test Building', 'building')],
            [],  # No chemicals
            [(1, 'No one assigned yet')]  # Assignments
        ]
        
        # Call the function
        getScheduledActivities()
        
        # Check that "found" message was printed
        found_message = False
        for call in mock_print.call_args_list:
            call_str = str(call).lower()
            if "found" in call_str:
                found_message = True
                break
        assert found_message == True
    
    @patch('scheduled_activities.getUserInput')
    @patch('scheduled_activities.cur')
    @patch('builtins.print')
    def test_getScheduledActivities_with_chemicals(self, mock_print, mock_cur, mock_input):
        """Test activities with chemical usage"""
        # Set up mocks
        mock_input.side_effect = ['2025-01-01', '2025-12-31', '']
        
        mock_cur.fetchall.side_effect = [
            [(1, 'cleaning', '2025-11-25', '2025-11-26', 0, 'cleaning', 1, 'Test Building', 'building')],
            [(1, 'windex', 1)],  # Harmful chemical
            [(1, 'John Doe')]
        ]
        
        # Call the function
        getScheduledActivities()
        
        # Check that "chemical" was mentioned in the output
        found_chemical = False
        for call in mock_print.call_args_list:
            call_str = str(call).lower()
            if "chemical" in call_str:
                found_chemical = True
                break
        assert found_chemical == True
    
    @patch('scheduled_activities.getUserInput')
    @patch('scheduled_activities.cur')
    @patch('builtins.print')
    def test_getScheduledActivities_makes_unusable(self, mock_print, mock_cur, mock_input):
        """Test activity that makes area unusable"""
        mock_input.side_effect = ['2025-01-01', '2025-12-31', '']
        
        mock_cur.fetchall.side_effect = [
            [(1, 'repair', '2025-11-25', '2025-11-26', 1, 'repair', 1, 'Test Building', 'building')],
            [],
            [(1, 'John Doe')]
        ]
        
        getScheduledActivities()
        assert any("unavailable" in str(call).lower() or "unusable" in str(call).lower() 
                  for call in mock_print.call_args_list)
    
    @patch('scheduled_activities.getUserInput')
    @patch('scheduled_activities.cur')
    @patch('builtins.print')
    def test_getScheduledActivities_all_filters(self, mock_print, mock_cur, mock_input):
        """Test with all filters applied"""
        mock_input.side_effect = ['2025-11-01', '2025-11-30', 'Building']
        mock_cur.fetchall.return_value = []
        
        getScheduledActivities()
        # Verify query was constructed with all conditions
        assert mock_cur.execute.called
        call_args = mock_cur.execute.call_args[0][0]
        assert 'start_date' in call_args.lower()
        assert 'end_date' in call_args.lower()
        assert 'area_name' in call_args.lower()
    
    @patch('scheduled_activities.getUserInput')
    @patch('scheduled_activities.cur')
    @patch('builtins.print')
    def test_getScheduledActivities_exception_handling(self, mock_print, mock_cur, mock_input):
        """Test exception handling"""
        mock_input.side_effect = ['2025-01-01', '2025-12-31', '']
        mock_cur.execute.side_effect = Exception("Database error")
        
        getScheduledActivities()
        assert any("went wrong" in str(call).lower() or "error" in str(call).lower() 
                  for call in mock_print.call_args_list)
    
    @patch('scheduled_activities.getUserInput')
    @patch('scheduled_activities.cur')
    @patch('builtins.print')
    def test_getScheduledActivities_multiple_activities(self, mock_print, mock_cur, mock_input):
        """Test with multiple activities"""
        mock_input.side_effect = ['2025-01-01', '2025-12-31', '']
        
        mock_cur.fetchall.side_effect = [
            [
                (1, 'activity1', '2025-11-25', '2025-11-26', 0, 'cleaning', 1, 'Building1', 'building'),
                (2, 'activity2', '2025-11-27', '2025-11-28', 1, 'repair', 2, 'Building2', 'building')
            ],
            [],  # No chemicals
            [(1, 'John'), (2, 'Jane')]  # Assignments
        ]
        
        getScheduledActivities()
        # Should process multiple activities
        assert mock_cur.execute.call_count >= 3  # Main query + chemical query + assignment query

