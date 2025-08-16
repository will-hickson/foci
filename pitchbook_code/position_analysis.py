#!/usr/bin/env python3
"""
Position Analysis Script
Analyzes the different types of positions and shows where people are categorized.
"""

import pandas as pd
import numpy as np

def analyze_positions():
    """Analyze different position types and their counts."""
    print("POSITION ANALYSIS")
    print("="*60)
    
    # Load the data
    pos_df = pd.read_csv('pitchbook_data/PersonPositionRelation.csv')
    comp_df = pd.read_csv('pitchbook_data/Company.csv')
    board_df = pd.read_csv('pitchbook_data/PersonBoardSeatRelation.csv')
    summary_df = pd.read_csv('analysis_output/company_summary_table.csv')
    
    print(f"Total positions in PersonPositionRelation: {len(pos_df)}")
    print(f"Total board seats in PersonBoardSeatRelation: {len(board_df)}")
    print(f"Companies in our dataset: {len(comp_df)}")
    
    # Merge positions with companies
    merged = pos_df.merge(comp_df, left_on='EntityID', right_on='CompanyID', how='inner')
    
    print(f"\nPositions at companies in our dataset: {len(merged)}")
    print(f"Unique persons at companies: {merged['PersonID'].nunique()}")
    print(f"Unique companies with positions: {merged['CompanyID'].nunique()}")
    
    # Check board members for our companies
    board_at_our_companies = board_df[board_df['CompanyID'].isin(comp_df['CompanyID'])]
    
    print(f"\nBoard seats at our companies: {len(board_at_our_companies)}")
    print(f"Unique board members at our companies: {board_at_our_companies['PersonID'].nunique()}")
    print(f"Companies with board members: {board_at_our_companies['CompanyID'].nunique()}")
    
    # Show position types at our companies
    print(f"\nPosition types at our companies:")
    position_types = merged['EntityType'].value_counts()
    for pos_type, count in position_types.items():
        print(f"  {pos_type}: {count}")
    
    # Show summary table counts
    print(f"\nSummary Table Board Members: {summary_df['BoardMembers'].sum()}")
    print(f"Companies with board members in summary: {len(summary_df[summary_df['BoardMembers'] > 0])}")
    
    # Check for overlap between positions and board members
    position_persons = set(merged['PersonID'])
    board_persons = set(board_at_our_companies['PersonID'])
    
    overlap = position_persons.intersection(board_persons)
    print(f"\nPersons who are both employees AND board members: {len(overlap)}")
    print(f"Persons who are only employees (not board members): {len(position_persons - board_persons)}")
    print(f"Persons who are only board members (not employees): {len(board_persons - position_persons)}")
    
    return merged, board_at_our_companies

if __name__ == "__main__":
    analyze_positions()
