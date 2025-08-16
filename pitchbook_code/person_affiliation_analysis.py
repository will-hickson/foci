#!/usr/bin/env python3
"""
Person Affiliation Analysis
Analyzes the additional affiliations of the 101 people beyond their primary company positions.
"""

import pandas as pd

def analyze_person_affiliations():
    """Analyze additional affiliations of the 101 people."""
    print("PERSON AFFILIATION ANALYSIS")
    print("="*60)
    
    # Load data
    pos_df = pd.read_csv('pitchbook_data/PersonPositionRelation.csv')
    comp_df = pd.read_csv('pitchbook_data/Company.csv')
    
    # Get our 101 people (those with positions at our companies)
    merged = pos_df.merge(comp_df, left_on='EntityID', right_on='CompanyID', how='inner')
    our_people = set(merged['PersonID'])
    
    print(f"Our 101 people have positions at our companies")
    print(f"Total positions for our people: {len(pos_df[pos_df['PersonID'].isin(our_people)])}")
    
    # Get all positions for our people
    all_positions = pos_df[pos_df['PersonID'].isin(our_people)]
    
    # Analyze by entity type
    print(f"\nEntity Types for Our 101 People:")
    entity_types = all_positions['EntityType'].value_counts()
    for entity_type, count in entity_types.items():
        print(f"  {entity_type}: {count} positions")
    
    # Analyze people with additional affiliations
    company_positions = all_positions[all_positions['EntityType'] == 'Company']
    other_positions = all_positions[all_positions['EntityType'] != 'Company']
    
    people_with_only_companies = set(company_positions['PersonID']) - set(other_positions['PersonID'])
    people_with_other_positions = set(other_positions['PersonID'])
    
    print(f"\nAffiliation Breakdown:")
    print(f"  People with only company positions: {len(people_with_only_companies)}")
    print(f"  People with other entity positions: {len(people_with_other_positions)}")
    print(f"  Total unique people: {len(people_with_only_companies) + len(people_with_other_positions)}")
    
    # Show examples of people with multiple affiliations
    print(f"\nPeople with Most Positions:")
    person_counts = all_positions['PersonID'].value_counts()
    for person_id, count in person_counts.head(10).items():
        person_positions = all_positions[all_positions['PersonID'] == person_id]
        print(f"  Person {person_id}: {count} positions")
        for _, pos in person_positions.iterrows():
            print(f"    - {pos['EntityType']}: {pos['EntityName']} ({pos['FullTitle']})")
    
    # Analyze by specific entity types
    print(f"\nDetailed Analysis by Entity Type:")
    for entity_type in ['University (Non-Endowment)', 'Venture Capital', 'Foundation']:
        entity_positions = all_positions[all_positions['EntityType'] == entity_type]
        print(f"  {entity_type}: {len(entity_positions)} positions by {entity_positions['PersonID'].nunique()} people")
    
    return all_positions, our_people

if __name__ == "__main__":
    analyze_person_affiliations()
