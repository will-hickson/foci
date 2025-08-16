#!/usr/bin/env python3
"""
Second Level Relationship Analysis
Analyzes people connected to our companies through second-level relationships (investors, service providers, etc.)
"""

import pandas as pd

def analyze_second_level_relationships():
    """Analyze second-level relationships and people."""
    print("SECOND LEVEL RELATIONSHIP ANALYSIS")
    print("="*60)
    
    # Load data
    pos_df = pd.read_csv('pitchbook_data/PersonPositionRelation.csv')
    comp_df = pd.read_csv('pitchbook_data/Company.csv')
    inv_rel_df = pd.read_csv('pitchbook_data/CompanyInvestorRelation.csv')
    sp_rel_df = pd.read_csv('pitchbook_data/CompanyServiceProviderRelation.csv')
    lp_rel_df = pd.read_csv('pitchbook_data/CompanyInvLeadPartnerRelation.csv')
    aff_rel_df = pd.read_csv('pitchbook_data/CompanyAffiliateRelation.csv')
    
    # Get connected entities
    our_investors = set(inv_rel_df['InvestorID'])
    our_service_providers = set(sp_rel_df['ServiceProviderID'])
    our_lead_partners = set(lp_rel_df['LeadPartnerID'])
    our_affiliates = set(aff_rel_df['AffiliateID'])
    
    connected_entities = our_investors.union(our_service_providers).union(our_lead_partners).union(our_affiliates)
    
    print(f"Connected entities to our companies:")
    print(f"  Investors: {len(our_investors)}")
    print(f"  Service Providers: {len(our_service_providers)}")
    print(f"  Lead Partners: {len(our_lead_partners)}")
    print(f"  Affiliates: {len(our_affiliates)}")
    print(f"  Total connected entities: {len(connected_entities)}")
    
    # Get people at connected entities
    connected_people = pos_df[pos_df['EntityID'].isin(connected_entities)]
    
    print(f"\nSecond-level people analysis:")
    print(f"  Total positions at connected entities: {len(connected_people)}")
    print(f"  Unique people at connected entities: {connected_people['PersonID'].nunique()}")
    
    # Analyze by entity type
    print(f"\nPeople by connected entity type:")
    entity_types = connected_people['EntityType'].value_counts()
    for entity_type, count in entity_types.head(10).items():
        print(f"  {entity_type}: {count} positions")
    
    # Analyze by relationship type
    investor_people = pos_df[pos_df['EntityID'].isin(our_investors)]
    sp_people = pos_df[pos_df['EntityID'].isin(our_service_providers)]
    lp_people = pos_df[pos_df['EntityID'].isin(our_lead_partners)]
    aff_people = pos_df[pos_df['EntityID'].isin(our_affiliates)]
    
    print(f"\nPeople by relationship type:")
    print(f"  People at investor entities: {len(investor_people)} ({investor_people['PersonID'].nunique()} unique)")
    print(f"  People at service provider entities: {len(sp_people)} ({sp_people['PersonID'].nunique()} unique)")
    print(f"  People at lead partner entities: {len(lp_people)} ({lp_people['PersonID'].nunique()} unique)")
    print(f"  People at affiliate entities: {len(aff_people)} ({aff_people['PersonID'].nunique()} unique)")
    
    # Check for international connections
    print(f"\nInternational analysis:")
    international_entities = connected_people[connected_people['EntityType'].isin(['University (Non-Endowment)', 'Venture Capital', 'Foundation'])]
    print(f"  International entity positions: {len(international_entities)}")
    print(f"  Unique people at international entities: {international_entities['PersonID'].nunique()}")
    
    return connected_people, our_investors, our_service_providers, our_lead_partners, our_affiliates

if __name__ == "__main__":
    analyze_second_level_relationships()
