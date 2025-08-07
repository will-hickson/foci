#!/usr/bin/env python3
"""
Search for specific EntityIDs in all CSV files to check for relationships
"""

import pandas as pd
import os

def search_entity_ids():
    """Search for specific EntityIDs in all CSV files."""
    entity_ids = ['10011-79', '10019-98', '10115-20', '10047-34', '10069-75', '10143-10', '11079-46', '10072-27', '10014-49']
    
    csv_files = [f for f in os.listdir('pitchbook_data') if f.endswith('.csv')]
    
    print("Searching for EntityIDs in all CSV files:")
    print(f"EntityIDs to search: {entity_ids}")
    print(f"CSV files to search: {csv_files}")
    print("\nResults:")
    
    for entity_id in entity_ids:
        print(f"\nEntityID {entity_id}:")
        found = False
        
        for csv_file in csv_files:
            try:
                df = pd.read_csv(f'pitchbook_data/{csv_file}')
                
                # Check if entity_id appears in any column
                for col in df.columns:
                    if entity_id in df[col].astype(str).values:
                        print(f"  Found in {csv_file} column {col}")
                        found = True
                        
            except Exception as e:
                print(f"  Error reading {csv_file}: {e}")
        
        if not found:
            print("  Not found in any CSV file")

if __name__ == "__main__":
    search_entity_ids()
