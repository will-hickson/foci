#!/usr/bin/env python3
"""
Enhanced International Connections Analysis for PitchBook Data
Focuses on entities outside the USA and their connections to companies.
Includes null country handling and detailed breakdowns.
"""

import pandas as pd
import numpy as np
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

class EnhancedInternationalAnalyzer:
    def __init__(self, data_dir='pitchbook_data'):
        """Initialize the enhanced international analyzer."""
        self.data_dir = Path(data_dir)
        self.data = {}
        self.international_entities = {}
        self.null_country_entities = {}
        self.load_international_data()
    
    def load_international_data(self):
        """Load data files that contain country information."""
        print("Loading data for enhanced international analysis...")
        
        # Core files with country information
        files_with_countries = [
            'Company.csv',
            'Investor.csv', 
            'ServiceProvider.csv',
            'LimitedPartner.csv',
            'Person.csv',
            'CompanyInvestorRelation.csv',
            'DealInvestorRelation.csv',
            'FundLimitedPartnerRelation.csv'
        ]
        
        for file in files_with_countries:
            file_path = self.data_dir / file
            if file_path.exists():
                try:
                    self.data[file.replace('.csv', '')] = pd.read_csv(file_path)
                    print(f"✓ Loaded {file}")
                except Exception as e:
                    print(f"✗ Error loading {file}: {e}")
        
        print(f"\nTotal files loaded: {len(self.data)}")
    
    def analyze_international_entities(self):
        """Analyze entities outside the USA and handle null countries."""
        print("\n" + "="*60)
        print("ENHANCED INTERNATIONAL ENTITIES ANALYSIS")
        print("="*60)
        
        international_data = {}
        null_country_data = {}
        
        # 1. Analyze Investors outside USA and null countries
        if 'Investor' in self.data:
            investors_df = self.data['Investor']
            if 'HQCountry' in investors_df.columns:
                # Handle null countries
                null_country_investors = investors_df[investors_df['HQCountry'].isna() | (investors_df['HQCountry'] == '')]
                null_country_data['investors'] = null_country_investors
                
                # Non-US investors
                non_us_investors = investors_df[investors_df['HQCountry'] != 'United States']
                international_data['investors'] = non_us_investors
                
                print(f"\nInternational Investors:")
                print(f"  Total investors: {len(investors_df)}")
                print(f"  Non-US investors: {len(non_us_investors)}")
                print(f"  Investors with null/empty country: {len(null_country_investors)}")
                
                if len(non_us_investors) > 0:
                    country_counts = non_us_investors['HQCountry'].value_counts()
                    print(f"  Countries represented:")
                    for country, count in country_counts.items():
                        print(f"    {country}: {count} investors")
        
        # 2. Analyze Service Providers outside USA and null countries
        if 'ServiceProvider' in self.data:
            service_providers_df = self.data['ServiceProvider']
            if 'HQCountry' in service_providers_df.columns:
                # Handle null countries
                null_country_service_providers = service_providers_df[service_providers_df['HQCountry'].isna() | (service_providers_df['HQCountry'] == '')]
                null_country_data['service_providers'] = null_country_service_providers
                
                # Non-US service providers
                non_us_service_providers = service_providers_df[service_providers_df['HQCountry'] != 'United States']
                international_data['service_providers'] = non_us_service_providers
                
                print(f"\nInternational Service Providers:")
                print(f"  Total service providers: {len(service_providers_df)}")
                print(f"  Non-US service providers: {len(non_us_service_providers)}")
                print(f"  Service providers with null/empty country: {len(null_country_service_providers)}")
                
                if len(non_us_service_providers) > 0:
                    country_counts = non_us_service_providers['HQCountry'].value_counts()
                    print(f"  Countries represented:")
                    for country, count in country_counts.items():
                        print(f"    {country}: {count} service providers")
        
        # 3. Analyze Limited Partners outside USA and null countries
        if 'LimitedPartner' in self.data:
            limited_partners_df = self.data['LimitedPartner']
            if 'HQCountry' in limited_partners_df.columns:
                # Handle null countries
                null_country_limited_partners = limited_partners_df[limited_partners_df['HQCountry'].isna() | (limited_partners_df['HQCountry'] == '')]
                null_country_data['limited_partners'] = null_country_limited_partners
                
                # Non-US limited partners
                non_us_limited_partners = limited_partners_df[limited_partners_df['HQCountry'] != 'United States']
                international_data['limited_partners'] = non_us_limited_partners
                
                print(f"\nInternational Limited Partners:")
                print(f"  Total limited partners: {len(limited_partners_df)}")
                print(f"  Non-US limited partners: {len(non_us_limited_partners)}")
                print(f"  Limited partners with null/empty country: {len(null_country_limited_partners)}")
                
                if len(non_us_limited_partners) > 0:
                    country_counts = non_us_limited_partners['HQCountry'].value_counts()
                    print(f"  Countries represented:")
                    for country, count in country_counts.items():
                        print(f"    {country}: {count} limited partners")
        
        # 4. Analyze Persons outside USA and null countries
        if 'Person' in self.data:
            persons_df = self.data['Person']
            if 'Country' in persons_df.columns:
                # Handle null countries
                null_country_persons = persons_df[persons_df['Country'].isna() | (persons_df['Country'] == '')]
                null_country_data['persons'] = null_country_persons
                
                # Non-US persons
                non_us_persons = persons_df[persons_df['Country'] != 'United States']
                international_data['persons'] = non_us_persons
                
                print(f"\nInternational Persons:")
                print(f"  Total persons: {len(persons_df)}")
                print(f"  Non-US persons: {len(non_us_persons)}")
                print(f"  Persons with null/empty country: {len(null_country_persons)}")
                
                if len(non_us_persons) > 0:
                    country_counts = non_us_persons['Country'].value_counts()
                    print(f"  Countries represented:")
                    for country, count in country_counts.head(10).items():
                        print(f"    {country}: {count} persons")
        
        self.international_entities = international_data
        self.null_country_entities = null_country_data
        return international_data, null_country_data
    
    def find_company_connections(self):
        """Find connections between international entities and companies with detailed breakdown."""
        print("\n" + "="*60)
        print("DETAILED INTERNATIONAL ENTITY - COMPANY CONNECTIONS")
        print("="*60)
        
        connections = []
        connection_breakdown = {
            'Investor': 0,
            'ServiceProvider': 0,
            'LimitedPartner': 0,
            'Person': 0
        }
        
        # 1. International Investors connected to companies
        if 'CompanyInvestorRelation' in self.data and 'investors' in self.international_entities:
            rel_df = self.data['CompanyInvestorRelation']
            int_investors = self.international_entities['investors']
            
            # Get international investor IDs
            int_investor_ids = set(int_investors['InvestorID'])
            
            # Find relationships with international investors
            int_investor_relations = rel_df[rel_df['InvestorID'].isin(int_investor_ids)]
            connection_breakdown['Investor'] = len(int_investor_relations)
            
            if len(int_investor_relations) > 0:
                print(f"\nInternational Investor - Company Connections:")
                print(f"  Total connections: {len(int_investor_relations)}")
                
                for _, relation in int_investor_relations.iterrows():
                    investor_info = int_investors[int_investors['InvestorID'] == relation['InvestorID']].iloc[0]
                    connections.append({
                        'EntityType': 'Investor',
                        'EntityID': relation['InvestorID'],
                        'EntityName': relation['InvestorName'],
                        'EntityCountry': investor_info['HQCountry'],
                        'CompanyID': relation['CompanyID'],
                        'CompanyName': relation['CompanyName'],
                        'ConnectionType': 'Investment',
                        'Status': relation.get('InvestorStatus', 'Unknown')
                    })
        
        # 2. International Service Providers connected to deals
        if 'DealServiceProviderRelation' in self.data and 'service_providers' in self.international_entities:
            rel_df = self.data['DealServiceProviderRelation']
            int_service_providers = self.international_entities['service_providers']
            
            # Get international service provider IDs
            int_sp_ids = set(int_service_providers['ServiceProviderID'])
            
            # Find relationships with international service providers
            int_sp_relations = rel_df[rel_df['ServiceProviderID'].isin(int_sp_ids)]
            connection_breakdown['ServiceProvider'] = len(int_sp_relations)
            
            if len(int_sp_relations) > 0:
                print(f"\nInternational Service Provider - Deal Connections:")
                print(f"  Total connections: {len(int_sp_relations)}")
                
                for _, relation in int_sp_relations.iterrows():
                    sp_info = int_service_providers[int_service_providers['ServiceProviderID'] == relation['ServiceProviderID']].iloc[0]
                    connections.append({
                        'EntityType': 'ServiceProvider',
                        'EntityID': relation['ServiceProviderID'],
                        'EntityName': relation['ServiceProviderName'],
                        'EntityCountry': sp_info['HQCountry'],
                        'CompanyID': 'N/A',  # Connected via deal, not direct company
                        'CompanyName': 'N/A',
                        'ConnectionType': 'Service',
                        'Status': 'Active'
                    })
        
        # 3. International Limited Partners connected to funds
        if 'FundLimitedPartnerRelation' in self.data and 'limited_partners' in self.international_entities:
            rel_df = self.data['FundLimitedPartnerRelation']
            int_limited_partners = self.international_entities['limited_partners']
            
            # Get international limited partner IDs
            int_lp_ids = set(int_limited_partners['LimitedPartnerID'])
            
            # Find relationships with international limited partners
            int_lp_relations = rel_df[rel_df['LimitedPartnerID'].isin(int_lp_ids)]
            connection_breakdown['LimitedPartner'] = len(int_lp_relations)
            
            if len(int_lp_relations) > 0:
                print(f"\nInternational Limited Partner - Fund Connections:")
                print(f"  Total connections: {len(int_lp_relations)}")
                
                for _, relation in int_lp_relations.iterrows():
                    lp_info = int_limited_partners[int_limited_partners['LimitedPartnerID'] == relation['LimitedPartnerID']].iloc[0]
                    connections.append({
                        'EntityType': 'LimitedPartner',
                        'EntityID': relation['LimitedPartnerID'],
                        'EntityName': relation['LimitedPartnerName'],
                        'EntityCountry': lp_info['HQCountry'],
                        'CompanyID': 'N/A',  # Connected via fund, not direct company
                        'CompanyName': 'N/A',
                        'ConnectionType': 'Fund Investment',
                        'Status': 'Active'
                    })
        
        # 4. International Persons connected to companies
        if 'Person' in self.data and 'persons' in self.international_entities:
            persons_df = self.data['Person']
            int_persons = self.international_entities['persons']
            
            # Find persons with primary company connections
            int_persons_with_company = int_persons[int_persons['PrimaryCompanyID'].notna()]
            connection_breakdown['Person'] = len(int_persons_with_company)
            
            if len(int_persons_with_company) > 0:
                print(f"\nInternational Person - Company Connections:")
                print(f"  Total connections: {len(int_persons_with_company)}")
                
                for _, person in int_persons_with_company.iterrows():
                    connections.append({
                        'EntityType': 'Person',
                        'EntityID': person['PersonID'],
                        'EntityName': person['FullName'],
                        'EntityCountry': person['Country'],
                        'CompanyID': person['PrimaryCompanyID'],
                        'CompanyName': person['PrimaryCompany'],
                        'ConnectionType': 'Employment',
                        'Status': 'Active'
                    })
        
        # Print detailed breakdown
        print(f"\n" + "="*60)
        print("CONNECTION BREAKDOWN")
        print("="*60)
        total_connections = sum(connection_breakdown.values())
        print(f"Total International Connections: {total_connections}")
        print(f"  - Investor connections: {connection_breakdown['Investor']}")
        print(f"  - Service Provider connections: {connection_breakdown['ServiceProvider']}")
        print(f"  - Limited Partner connections: {connection_breakdown['LimitedPartner']}")
        print(f"  - Person connections: {connection_breakdown['Person']}")
        
        self.connections = connections
        self.connection_breakdown = connection_breakdown
        return connections
    
    def export_international_entities_for_compliance(self):
        """Export international entities with requested fields for compliance analysis."""
        print("\n" + "="*60)
        print("EXPORTING INTERNATIONAL ENTITIES FOR COMPLIANCE")
        print("="*60)
        
        import os
        os.makedirs('analysis_output', exist_ok=True)
        
        compliance_entities = []
        
        # Export international persons with requested fields
        if 'persons' in self.international_entities:
            persons_df = self.international_entities['persons']
            for _, person in persons_df.iterrows():
                compliance_entities.append({
                    'EntityType': 'Person',
                    'EntityID': person['PersonID'],
                    'EntityName': person['FullName'],
                    'Country': person['Country'],
                    'LinkedInProfileURL': person.get('LinkedInProfileURL', ''),
                    'PrimaryCompanyID': person.get('PrimaryCompanyID', ''),
                    'PrimaryCompany': person.get('PrimaryCompany', ''),
                    'PrimaryCompanyWebsite': person.get('PrimaryCompanyWebsite', ''),
                    'Biography': person.get('Biography', ''),
                    'PrimaryPosition': person.get('PrimaryPosition', ''),
                    'PrimaryPositionLevel': person.get('PrimaryPositionLevel', '')
                })
        
        # Export international investors with all fields
        if 'investors' in self.international_entities:
            investors_df = self.international_entities['investors']
            for _, investor in investors_df.iterrows():
                compliance_entities.append({
                    'EntityType': 'Investor',
                    'EntityID': investor['InvestorID'],
                    'EntityName': investor['InvestorName'],
                    'Country': investor['HQCountry'],
                    'Website': investor.get('Website', ''),
                    'HQLocation': investor.get('HQLocation', ''),
                    'HQAddressLine1': investor.get('HQAddressLine1', ''),
                    'HQCity': investor.get('HQCity', ''),
                    'HQState_Province': investor.get('HQState_Province', ''),
                    'HQPostCode': investor.get('HQPostCode', ''),
                    'HQEmail': investor.get('HQEmail', ''),
                    'PrimaryContact': investor.get('PrimaryContact', ''),
                    'PrimaryContactEmail': investor.get('PrimaryContactEmail', '')
                })
        
        # Export international service providers with all fields
        if 'service_providers' in self.international_entities:
            service_providers_df = self.international_entities['service_providers']
            for _, sp in service_providers_df.iterrows():
                compliance_entities.append({
                    'EntityType': 'ServiceProvider',
                    'EntityID': sp['ServiceProviderID'],
                    'EntityName': sp['ServiceProviderName'],
                    'Country': sp['HQCountry'],
                    'Website': sp.get('Website', ''),
                    'HQLocation': sp.get('HQLocation', ''),
                    'HQCity': sp.get('HQCity', ''),
                    'HQState_Province': sp.get('HQState_Province', '')
                })
        
        # Export international limited partners with all fields
        if 'limited_partners' in self.international_entities:
            limited_partners_df = self.international_entities['limited_partners']
            for _, lp in limited_partners_df.iterrows():
                compliance_entities.append({
                    'EntityType': 'LimitedPartner',
                    'EntityID': lp['LimitedPartnerID'],
                    'EntityName': lp['LimitedPartnerName'],
                    'Country': lp['HQCountry'],
                    'Website': lp.get('Website', ''),
                    'HQLocation': lp.get('HQLocation', ''),
                    'HQAddressLine1': lp.get('HQAddressLine1', ''),
                    'HQCity': lp.get('HQCity', ''),
                    'HQState_Province': lp.get('HQState_Province', ''),
                    'HQPostCode': lp.get('HQPostCode', ''),
                    'LimitedPartnerType': lp.get('LimitedPartnerType', ''),
                    'AUM': lp.get('AUM', ''),
                    'Description': lp.get('Description', '')
                })
        
        # Create DataFrame and export
        if compliance_entities:
            compliance_df = pd.DataFrame(compliance_entities)
            compliance_df.to_csv('analysis_output/international_entities_compliance.csv', index=False)
            print(f"✓ Exported {len(compliance_entities)} international entities for compliance analysis")
        
        # Export null country entities summary
        null_summary = []
        for entity_type, entities in self.null_country_entities.items():
            null_summary.append({
                'EntityType': entity_type.title(),
                'Count': len(entities),
                'Description': f'Entities with null or empty country field'
            })
        
        if null_summary:
            null_df = pd.DataFrame(null_summary)
            null_df.to_csv('analysis_output/null_country_entities_summary.csv', index=False)
            print(f"✓ Exported null country entities summary")
        
        return compliance_entities
    
    def run_enhanced_analysis(self):
        """Run the complete enhanced international analysis."""
        print("ENHANCED INTERNATIONAL CONNECTIONS ANALYSIS")
        print("="*60)
        
        self.analyze_international_entities()
        self.find_company_connections()
        self.export_international_entities_for_compliance()
        
        print("\n" + "="*60)
        print("ENHANCED INTERNATIONAL ANALYSIS COMPLETE")
        print("="*60)

def main():
    """Main function to run the enhanced international analysis."""
    try:
        analyzer = EnhancedInternationalAnalyzer()
        analyzer.run_enhanced_analysis()
        
    except Exception as e:
        print(f"Error during enhanced international analysis: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 