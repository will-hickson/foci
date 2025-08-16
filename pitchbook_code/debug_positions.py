#!/usr/bin/env python3
"""
Debug script to test position counting logic.
"""

import pandas as pd

def debug_positions():
    """Debug the position counting logic."""
    print("DEBUGGING POSITION COUNTS")
    print("="*60)
    
    # Load data
    pos_df = pd.read_csv('pitchbook_data/PersonPositionRelation.csv')
    board_df = pd.read_csv('pitchbook_data/PersonBoardSeatRelation.csv')
    comp_df = pd.read_csv('pitchbook_data/Company.csv')
    
    # Get positions at our companies
    merged = pos_df.merge(comp_df, left_on='EntityID', right_on='CompanyID', how='inner')
    print(f"Positions at our companies: {len(merged)}")
    
    # Get board members at our companies
    board_at_our_companies = board_df[board_df['CompanyID'].isin(comp_df['CompanyID'])]
    print(f"Board seats at our companies: {len(board_at_our_companies)}")
    
    # Get sets of persons
    position_persons = set(merged['PersonID'])
    board_persons = set(board_at_our_companies['PersonID'])
    
    print(f"Unique persons with positions: {len(position_persons)}")
    print(f"Unique persons with board seats: {len(board_persons)}")
    
    # Calculate overlaps
    employee_board_persons = position_persons.intersection(board_persons)
    only_employees = position_persons - board_persons
    only_board_members = board_persons - position_persons
    
    print(f"Persons who are both employees AND board members: {len(employee_board_persons)}")
    print(f"Persons who are only employees (not board members): {len(only_employees)}")
    print(f"Persons who are only board members (not employees): {len(only_board_members)}")
    
    # Test for one specific company
    test_company = '234500-68'  # Alphacore
    print(f"\nTesting for company {test_company}:")
    
    company_employees = merged[merged['CompanyID'] == test_company]
    company_board = board_at_our_companies[board_at_our_companies['CompanyID'] == test_company]
    
    print(f"  Company employees: {len(company_employees)}")
    print(f"  Company board seats: {len(company_board)}")
    
    company_employee_ids = set(company_employees['PersonID'])
    company_board_ids = set(company_board['PersonID'])
    
    only_employee_count = len(company_employee_ids.intersection(only_employees))
    employee_board_count = len(company_board_ids.intersection(employee_board_persons))
    other_board_count = len(company_board_ids.intersection(only_board_members))
    
    print(f"  Only employees: {only_employee_count}")
    print(f"  Employee board members: {employee_board_count}")
    print(f"  Other board members: {other_board_count}")
    
    return merged, board_at_our_companies

if __name__ == "__main__":
    debug_positions()
