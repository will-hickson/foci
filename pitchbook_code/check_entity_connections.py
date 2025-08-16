#!/usr/bin/env python3
"""
Check if specific EntityIDs connect to our 34 companies through any relationship
"""

import pandas as pd

def check_entity_connections():
    """Check if EntityIDs connect to our companies."""
    entity_ids = ['10011-79', '10019-98', '10115-20', '10047-34', '10069-75', '10143-10', '11079-46', '10072-27', '10014-49']
    
    comp_df = pd.read_csv('pitchbook_data/Company.csv')
    our_company_ids = set(comp_df['CompanyID'])
    
    print("Our 34 companies:")
    print(our_company_ids)
    print(f"\nChecking if EntityIDs connect to our companies:")
    
    for entity_id in entity_ids:
        print(f"\nEntityID {entity_id}:")
        
        # Check PersonAffiliatedDealRelation
        try:
            deal_rel_df = pd.read_csv('pitchbook_data/PersonAffiliatedDealRelation.csv')
            deals_with_entity = deal_rel_df[deal_rel_df['RepresentingID'] == entity_id]
            if len(deals_with_entity) > 0:
                print(f"  Found in PersonAffiliatedDealRelation: {len(deals_with_entity)} records")
                deal_ids = set(deals_with_entity['DealID'])
                print(f"  DealIDs: {list(deal_ids)[:5]}")
                
                # Check if these deals connect to our companies
                deal_df = pd.read_csv('pitchbook_data/Deal.csv')
                our_deals = deal_df[deal_df['DealID'].isin(deal_ids)]
                our_deals = our_deals[our_deals['CompanyID'].isin(our_company_ids)]
                if len(our_deals) > 0:
                    print(f"  CONNECTED TO OUR COMPANIES: {len(our_deals)} deals")
                    print(f"  Our companies involved: {list(our_deals['CompanyID'])}")
                else:
                    print("  Not connected to our companies")
        except Exception as e:
            print(f"  Error checking PersonAffiliatedDealRelation: {e}")
        
        # Check PersonAffiliatedFundRelation
        try:
            fund_rel_df = pd.read_csv('pitchbook_data/PersonAffiliatedFundRelation.csv')
            funds_with_entity = fund_rel_df[fund_rel_df['InvestorID'] == entity_id]
            if len(funds_with_entity) > 0:
                print(f"  Found in PersonAffiliatedFundRelation: {len(funds_with_entity)} records")
        except Exception as e:
            print(f"  Error checking PersonAffiliatedFundRelation: {e}")
        
        # Check PersonBoardSeatRelation
        try:
            board_rel_df = pd.read_csv('pitchbook_data/PersonBoardSeatRelation.csv')
            board_with_entity = board_rel_df[board_rel_df['RepresentingID'] == entity_id]
            our_board = board_with_entity[board_with_entity['CompanyID'].isin(our_company_ids)]
            if len(our_board) > 0:
                print(f"  CONNECTED TO OUR COMPANIES: {len(our_board)} board seats")
                print(f"  Our companies: {list(our_board['CompanyID'])}")
            else:
                print("  Not connected to our companies")
        except Exception as e:
            print(f"  Error checking PersonBoardSeatRelation: {e}")

if __name__ == "__main__":
    check_entity_connections()
