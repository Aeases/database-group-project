"""
Tests for report_generation.py
"""
import pytest
from unittest.mock import patch
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from report_generation import (
    generate_reports, show_worker_assignments, show_chemical_safety,
    show_area_status, show_employee_workload, show_upcoming_maintenance
)


class TestGenerateReports:
    """Test cases for generate_reports function"""
    
    @patch('report_generation.getUserInput')
    @patch('report_generation.show_worker_assignments')
    @patch('builtins.print')
    def test_generate_reports_worker_assignments(self, mock_print, mock_show, mock_input):
        """Test selecting worker assignments report"""
        mock_input.return_value = '1'
        generate_reports()
        mock_show.assert_called_once()
    
    @patch('report_generation.getUserInput')
    @patch('report_generation.show_chemical_safety')
    @patch('builtins.print')
    def test_generate_reports_chemical_safety(self, mock_print, mock_show, mock_input):
        """Test selecting chemical safety report"""
        mock_input.return_value = '2'
        generate_reports()
        mock_show.assert_called_once()
    
    @patch('report_generation.getUserInput')
    @patch('report_generation.show_area_status')
    @patch('builtins.print')
    def test_generate_reports_area_status(self, mock_print, mock_show, mock_input):
        """Test selecting area status report"""
        mock_input.return_value = '3'
        generate_reports()
        mock_show.assert_called_once()
    
    @patch('report_generation.getUserInput')
    @patch('report_generation.show_employee_workload')
    @patch('builtins.print')
    def test_generate_reports_employee_workload(self, mock_print, mock_show, mock_input):
        """Test selecting employee workload report"""
        mock_input.return_value = '4'
        generate_reports()
        mock_show.assert_called_once()
    
    @patch('report_generation.getUserInput')
    @patch('report_generation.show_upcoming_maintenance')
    @patch('builtins.print')
    def test_generate_reports_upcoming_maintenance(self, mock_print, mock_show, mock_input):
        """Test selecting upcoming maintenance report"""
        mock_input.return_value = '5'
        generate_reports()
        mock_show.assert_called_once()
    
    @patch('report_generation.getUserInput')
    @patch('builtins.print')
    def test_generate_reports_invalid_choice(self, mock_print, mock_input):
        """Test invalid choice"""
        mock_input.return_value = '99'
        generate_reports()
        
        # Check that print was called (to show error message)
        assert mock_print.called == True
        # Check that one of the print calls contains "Invalid choice"
        found_invalid_message = False
        for call in mock_print.call_args_list:
            call_str = str(call)
            if "Invalid choice" in call_str:
                found_invalid_message = True
                break
        assert found_invalid_message == True


class TestShowWorkerAssignments:
    """Test cases for show_worker_assignments function"""
    
    @patch('report_generation.cur')
    @patch('report_generation.print_cursor')
    @patch('builtins.print')
    def test_show_worker_assignments(self, mock_print, mock_print_cursor, mock_cur):
        """Test worker assignments report"""
        # Set up mock data
        mock_cur.fetchall.return_value = [
            ('cleaning', 5, 10),
            ('repair', 3, 8)
        ]
        
        # Call the function
        show_worker_assignments()
        
        # Check that execute was called
        assert mock_cur.execute.called == True
        # Check that print_cursor was called
        assert mock_print_cursor.called == True


class TestShowChemicalSafety:
    """Test cases for show_chemical_safety function"""
    
    @patch('report_generation.cur')
    @patch('report_generation.print_cursor')
    @patch('builtins.print')
    def test_show_chemical_safety(self, mock_print, mock_print_cursor, mock_cur):
        """Test chemical safety report"""
        # Set up mock data
        mock_cur.fetchall.return_value = [
            ('Building A', 'windex', 'Harmful'),
            ('Building B', 'soap mix', 'Safe')
        ]
        
        # Call the function
        show_chemical_safety()
        
        # Check that execute was called
        assert mock_cur.execute.called == True
        # Check that print_cursor was called
        assert mock_print_cursor.called == True


class TestShowAreaStatus:
    """Test cases for show_area_status function"""
    
    @patch('report_generation.cur')
    @patch('report_generation.print_cursor')
    @patch('builtins.print')
    def test_show_area_status(self, mock_print, mock_print_cursor, mock_cur):
        """Test area status report"""
        # Set up mock data
        mock_cur.fetchall.return_value = [
            ('Building A', 'building', 'Open', 5),
            ('Room 101', 'room', 'Closed for work', 2)
        ]
        
        # Call the function
        show_area_status()
        
        # Check that execute was called
        assert mock_cur.execute.called == True
        # Check that print_cursor was called
        assert mock_print_cursor.called == True


class TestShowEmployeeWorkload:
    """Test cases for show_employee_workload function"""
    
    @patch('report_generation.cur')
    @patch('report_generation.print_cursor')
    @patch('builtins.print')
    def test_show_employee_workload(self, mock_print, mock_print_cursor, mock_cur):
        """Test employee workload report"""
        # Set up mock data
        mock_cur.fetchall.return_value = [
            ('John Doe', 'mid-level manager', 5, 2),
            ('Jane Smith', 'base-level worker', 3, 0)
        ]
        
        # Call the function
        show_employee_workload()
        
        # Check that execute was called
        assert mock_cur.execute.called == True
        # Check that print_cursor was called
        assert mock_print_cursor.called == True


class TestShowUpcomingMaintenance:
    """Test cases for show_upcoming_maintenance function"""
    
    @patch('report_generation.getUserInput')
    @patch('report_generation.cur')
    @patch('report_generation.print_cursor')
    @patch('builtins.print')
    def test_show_upcoming_maintenance_default_limit(self, mock_print, mock_print_cursor, mock_cur, mock_input):
        """Test upcoming maintenance with default limit"""
        mock_input.return_value = ''  # Empty input = default 10
        mock_cur.fetchall.return_value = [
            ('window cleaning', '2025-11-25', '2025-11-26', 'Building A')
        ]
        
        show_upcoming_maintenance()
        mock_cur.execute.assert_called_once()
        # Check that LIMIT 10 is in the query
        call_args = mock_cur.execute.call_args[0][0]
        assert 'LIMIT 10' in call_args
        mock_print_cursor.assert_called_once()
    
    @patch('report_generation.getUserInput')
    @patch('report_generation.cur')
    @patch('report_generation.print_cursor')
    @patch('builtins.print')
    def test_show_upcoming_maintenance_custom_limit(self, mock_print, mock_print_cursor, mock_cur, mock_input):
        """Test upcoming maintenance with custom limit"""
        mock_input.return_value = '5'
        mock_cur.fetchall.return_value = [
            ('window cleaning', '2025-11-25', '2025-11-26', 'Building A')
        ]
        
        show_upcoming_maintenance()
        call_args = mock_cur.execute.call_args[0][0]
        assert 'LIMIT 5' in call_args
    
    @patch('report_generation.getUserInput')
    @patch('report_generation.cur')
    @patch('report_generation.print_cursor')
    @patch('builtins.print')
    def test_show_upcoming_maintenance_invalid_limit(self, mock_print, mock_print_cursor, mock_cur, mock_input):
        """Test upcoming maintenance with invalid limit"""
        mock_input.return_value = 'invalid'
        mock_cur.fetchall.return_value = []
        
        show_upcoming_maintenance()
        
        # Check that it defaulted to LIMIT 10
        call_args = mock_cur.execute.call_args[0][0]
        assert 'LIMIT 10' in call_args
        
        # Check that an error message was printed
        found_error_message = False
        for call in mock_print.call_args_list:
            call_str = str(call)
            if "Invalid input" in call_str or "10" in call_str:
                found_error_message = True
                break
        assert found_error_message == True

