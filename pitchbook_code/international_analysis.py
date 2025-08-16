#!/usr/bin/env python3
"""
International Connections Analysis for PitchBook Data
Focuses on entities outside the USA and their connections to companies.
"""

import pandas as pd
import numpy as np
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

class InternationalAnalyzer:
    def __init__(self, data_dir='pitchbook_data'):
        """Initialize the international analyzer."""
        self.data_dir = Path(data_dir)
        self.data = {}
        self.international_entities = {}
        self.load_international_data()
    
    def load_international_data(self):
        """Load data files that contain country information."""
        print("Loading data for international analysis...")
        
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
        """Analyze entities outside the USA."""
        print("\n" + "="*60)
        print("INTERNATIONAL ENTITIES ANALYSIS")
        print("="*60)
        
        international_data = {}
        
        # 1. Analyze Investors outside USA
        if 'Investor' in self.data:
            investors_df = self.data['Investor']
            if 'HQCountry' in investors_df.columns:
                non_us_investors = investors_df[investors_df['HQCountry'] != 'United States']
                international_data['investors'] = non_us_investors
                
                print(f"\nInternational Investors:")
                print(f"  Total investors: {len(investors_df)}")
                print(f"  Non-US investors: {len(non_us_investors)}")
                
                if len(non_us_investors) > 0:
                    country_counts = non_us_investors['HQCountry'].value_counts()
                    print(f"  Countries represented:")
                    for country, count in country_counts.items():
                        print(f"    {country}: {count} investors")
        
        # 2. Analyze Service Providers outside USA
        if 'ServiceProvider' in self.data:
            service_providers_df = self.data['ServiceProvider']
            if 'HQCountry' in service_providers_df.columns:
                non_us_service_providers = service_providers_df[service_providers_df['HQCountry'] != 'United States']
                international_data['service_providers'] = non_us_service_providers
                
                print(f"\nInternational Service Providers:")
                print(f"  Total service providers: {len(service_providers_df)}")
                print(f"  Non-US service providers: {len(non_us_service_providers)}")
                
                if len(non_us_service_providers) > 0:
                    country_counts = non_us_service_providers['HQCountry'].value_counts()
                    print(f"  Countries represented:")
                    for country, count in country_counts.items():
                        print(f"    {country}: {count} service providers")
        
        # 3. Analyze Limited Partners outside USA
        if 'LimitedPartner' in self.data:
            limited_partners_df = self.data['LimitedPartner']
            if 'HQCountry' in limited_partners_df.columns:
                non_us_limited_partners = limited_partners_df[limited_partners_df['HQCountry'] != 'United States']
                international_data['limited_partners'] = non_us_limited_partners
                
                print(f"\nInternational Limited Partners:")
                print(f"  Total limited partners: {len(limited_partners_df)}")
                print(f"  Non-US limited partners: {len(non_us_limited_partners)}")
                
                if len(non_us_limited_partners) > 0:
                    country_counts = non_us_limited_partners['HQCountry'].value_counts()
                    print(f"  Countries represented:")
                    for country, count in country_counts.items():
                        print(f"    {country}: {count} limited partners")
        
        # 4. Analyze Persons outside USA
        if 'Person' in self.data:
            persons_df = self.data['Person']
            if 'Country' in persons_df.columns:
                non_us_persons = persons_df[persons_df['Country'] != 'United States']
                international_data['persons'] = non_us_persons
                
                print(f"\nInternational Persons:")
                print(f"  Total persons: {len(persons_df)}")
                print(f"  Non-US persons: {len(non_us_persons)}")
                
                if len(non_us_persons) > 0:
                    country_counts = non_us_persons['Country'].value_counts()
                    print(f"  Countries represented:")
                    for country, count in country_counts.head(10).items():
                        print(f"    {country}: {count} persons")
        
        self.international_entities = international_data
        return international_data
    
    def find_company_connections(self):
        """Find connections between international entities and companies."""
        print("\n" + "="*60)
        print("INTERNATIONAL ENTITY - COMPANY CONNECTIONS")
        print("="*60)
        
        connections = []
        
        # 1. International Investors connected to companies
        if 'CompanyInvestorRelation' in self.data and 'investors' in self.international_entities:
            rel_df = self.data['CompanyInvestorRelation']
            int_investors = self.international_entities['investors']
            
            # Get international investor IDs
            int_investor_ids = set(int_investors['InvestorID'])
            
            # Find relationships with international investors
            int_investor_relations = rel_df[rel_df['InvestorID'].isin(int_investor_ids)]
            
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
        
        self.connections = connections
        return connections
    
    def generate_country_statistics(self):
        """Generate comprehensive country statistics."""
        print("\n" + "="*60)
        print("COUNTRY STATISTICS")
        print("="*60)
        
        country_stats = {}
        
        # Collect all country data
        if 'investors' in self.international_entities:
            investor_countries = self.international_entities['investors']['HQCountry'].value_counts()
            country_stats['Investors'] = investor_countries
        
        if 'service_providers' in self.international_entities:
            sp_countries = self.international_entities['service_providers']['HQCountry'].value_counts()
            country_stats['ServiceProviders'] = sp_countries
        
        if 'limited_partners' in self.international_entities:
            lp_countries = self.international_entities['limited_partners']['HQCountry'].value_counts()
            country_stats['LimitedPartners'] = lp_countries
        
        if 'persons' in self.international_entities:
            person_countries = self.international_entities['persons']['Country'].value_counts()
            country_stats['Persons'] = person_countries
        
        # Combine all countries
        all_countries = {}
        for entity_type, countries in country_stats.items():
            for country, count in countries.items():
                if country not in all_countries:
                    all_countries[country] = {'Investors': 0, 'ServiceProviders': 0, 'LimitedPartners': 0, 'Persons': 0}
                all_countries[country][entity_type] = count
        
        # Display combined statistics
        print(f"\nCombined Country Statistics:")
        print(f"{'Country':<25} {'Investors':<10} {'Service Providers':<15} {'Limited Partners':<15} {'Persons':<10} {'Total':<10}")
        print("-" * 85)
        
        for country, counts in sorted(all_countries.items()):
            total = sum(counts.values())
            print(f"{country:<25} {counts.get('Investors', 0):<10} {counts.get('ServiceProviders', 0):<15} {counts.get('LimitedPartners', 0):<15} {counts.get('Persons', 0):<10} {total:<10}")
        
        return all_countries
    
    def export_international_data(self):
        """Export international entity data to CSV files."""
        print("\n" + "="*60)
        print("EXPORTING INTERNATIONAL DATA")
        print("="*60)
        
        import os
        os.makedirs('analysis_output', exist_ok=True)
        
        # Export connections
        if hasattr(self, 'connections') and self.connections:
            connections_df = pd.DataFrame(self.connections)
            connections_df.to_csv('analysis_output/international_connections.csv', index=False)
            print(f"✓ Exported {len(self.connections)} international connections to international_connections.csv")
        
        # Export international entities by type
        if 'investors' in self.international_entities:
            self.international_entities['investors'].to_csv('analysis_output/international_investors.csv', index=False)
            print(f"✓ Exported {len(self.international_entities['investors'])} international investors")
        
        if 'service_providers' in self.international_entities:
            self.international_entities['service_providers'].to_csv('analysis_output/international_service_providers.csv', index=False)
            print(f"✓ Exported {len(self.international_entities['service_providers'])} international service providers")
        
        if 'limited_partners' in self.international_entities:
            self.international_entities['limited_partners'].to_csv('analysis_output/international_limited_partners.csv', index=False)
            print(f"✓ Exported {len(self.international_entities['limited_partners'])} international limited partners")
        
        if 'persons' in self.international_entities:
            self.international_entities['persons'].to_csv('analysis_output/international_persons.csv', index=False)
            print(f"✓ Exported {len(self.international_entities['persons'])} international persons")
        
        # Export country statistics
        country_stats = self.generate_country_statistics()
        country_stats_df = pd.DataFrame([
            {
                'Country': country,
                'Investors': counts.get('Investors', 0),
                'ServiceProviders': counts.get('ServiceProviders', 0),
                'LimitedPartners': counts.get('LimitedPartners', 0),
                'Persons': counts.get('Persons', 0),
                'Total': sum(counts.values())
            }
            for country, counts in country_stats.items()
        ])
        country_stats_df = country_stats_df.sort_values('Total', ascending=False)
        country_stats_df.to_csv('analysis_output/country_statistics.csv', index=False)
        print(f"✓ Exported country statistics for {len(country_stats_df)} countries")
    
    def run_international_analysis(self):
        """Run the complete international analysis."""
        print("INTERNATIONAL CONNECTIONS ANALYSIS")
        print("="*60)
        
        self.analyze_international_entities()
        self.find_company_connections()
        self.generate_country_statistics()
        self.export_international_data()
        
        print("\n" + "="*60)
        print("INTERNATIONAL ANALYSIS COMPLETE")
        print("="*60)

def main():
    """Main function to run the international analysis."""
    try:
        analyzer = InternationalAnalyzer()
        analyzer.run_international_analysis()
        
    except Exception as e:
        print(f"Error during international analysis: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 