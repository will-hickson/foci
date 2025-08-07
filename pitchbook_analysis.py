#!/usr/bin/env python3
"""
PitchBook Data Analysis Script
Loads and analyzes PitchBook CSV data for evaluation purposes.
"""

import pandas as pd
import numpy as np
import os
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

class PitchBookAnalyzer:
    def __init__(self, data_dir='pitchbook_data'):
        """Initialize the analyzer with data directory."""
        self.data_dir = Path(data_dir)
        self.data = {}
        self.load_all_data()
    
    def load_all_data(self):
        """Load all CSV files from the data directory."""
        print("Loading PitchBook data...")
        
        # Core entity files
        core_files = [
            'Company.csv',
            'Investor.csv', 
            'Deal.csv',
            'Fund.csv',
            'LimitedPartner.csv',
            'ServiceProvider.csv'
        ]
        
        # Relationship files
        relation_files = [
            'CompanyInvestorRelation.csv',
            'CompanyBoardTeamRelation.csv',
            'CompanyLocationRelation.csv',
            'CompanyPatentRelation.csv',
            'CompanyAffiliateRelation.csv',
            'DealInvestorRelation.csv',
            'DealSellerRelation.csv',
            'DealServiceProviderRelation.csv',
            'InvestorBoardTeamRelation.csv',
            'InvestorCoInvestorRelation.csv',
            'InvestorLeadPartnerRelation.csv',
            'FundInvestorRelation.csv',
            'FundLimitedPartnerRelation.csv',
            'FundTeamRelation.csv',
            'PersonPositionRelation.csv',
            'PersonBoardSeatRelation.csv',
            'PersonAffiliatedDealRelation.csv',
            'PersonAffiliatedFundRelation.csv'
        ]
        
        # Load core entities
        for file in core_files:
            file_path = self.data_dir / file
            if file_path.exists():
                try:
                    self.data[file.replace('.csv', '')] = pd.read_csv(file_path)
                    print(f"✓ Loaded {file} ({len(self.data[file.replace('.csv', '')])} rows)")
                except Exception as e:
                    print(f"✗ Error loading {file}: {e}")
        
        # Load relationship files (skip large files for now)
        large_files = ['Person.csv', 'PatentCPCCode.csv', 'PersonEducationRelation.csv']
        for file in relation_files:
            file_path = self.data_dir / file
            if file_path.exists():
                try:
                    file_size = file_path.stat().st_size
                    if file_size < 50 * 1024 * 1024:  # Skip files larger than 50MB
                        self.data[file.replace('.csv', '')] = pd.read_csv(file_path)
                        print(f"✓ Loaded {file} ({len(self.data[file.replace('.csv', '')])} rows)")
                    else:
                        print(f"⚠ Skipped {file} (too large: {file_size / 1024 / 1024:.1f}MB)")
                except Exception as e:
                    print(f"✗ Error loading {file}: {e}")
        
        print(f"\nTotal files loaded: {len(self.data)}")
    
    def get_basic_stats(self):
        """Get basic statistics about the loaded data."""
        print("\n" + "="*60)
        print("BASIC DATA STATISTICS")
        print("="*60)
        
        for name, df in self.data.items():
            print(f"\n{name}:")
            print(f"  Rows: {len(df):,}")
            print(f"  Columns: {len(df.columns)}")
            print(f"  Memory usage: {df.memory_usage(deep=True).sum() / 1024 / 1024:.1f} MB")
            
            # Show sample columns
            if len(df.columns) <= 10:
                print(f"  Columns: {list(df.columns)}")
            else:
                print(f"  Sample columns: {list(df.columns[:5])}...")
    
    def analyze_company_investor_relationships(self):
        """Analyze relationships between companies and investors."""
        print("\n" + "="*60)
        print("COMPANY-INVESTOR RELATIONSHIP ANALYSIS")
        print("="*60)
        
        if 'CompanyInvestorRelation' not in self.data:
            print("CompanyInvestorRelation data not available")
            return
        
        rel_df = self.data['CompanyInvestorRelation']
        companies_df = self.data.get('Company', pd.DataFrame())
        
        print(f"\nTotal company-investor relationships: {len(rel_df):,}")
        
        # Analyze by investor status
        if 'InvestorStatus' in rel_df.columns:
            status_counts = rel_df['InvestorStatus'].value_counts()
            print(f"\nInvestor Status Distribution:")
            for status, count in status_counts.items():
                print(f"  {status}: {count:,}")
        
        # Analyze by holding type
        if 'Holding' in rel_df.columns:
            holding_counts = rel_df['Holding'].value_counts()
            print(f"\nHolding Type Distribution:")
            for holding, count in holding_counts.items():
                print(f"  {holding}: {count:,}")
        
        # Top investors by number of companies
        investor_counts = rel_df['InvestorID'].value_counts()
        print(f"\nTop 10 Investors by Number of Companies:")
        for investor_id, count in investor_counts.head(10).items():
            investor_name = rel_df[rel_df['InvestorID'] == investor_id]['InvestorName'].iloc[0]
            print(f"  {investor_name} ({investor_id}): {count} companies")
        
        # Companies with most investors
        company_counts = rel_df['CompanyID'].value_counts()
        print(f"\nCompanies with Most Investors:")
        for company_id, count in company_counts.head(10).items():
            company_name = rel_df[rel_df['CompanyID'] == company_id]['CompanyName'].iloc[0]
            print(f"  {company_name} ({company_id}): {count} investors")
    
    def analyze_deal_data(self):
        """Analyze deal information."""
        print("\n" + "="*60)
        print("DEAL ANALYSIS")
        print("="*60)
        
        if 'Deal' not in self.data:
            print("Deal data not available")
            return
        
        deals_df = self.data['Deal']
        print(f"\nTotal deals: {len(deals_df):,}")
        
        # Companies with most deals
        company_deal_counts = deals_df['CompanyID'].value_counts()
        print(f"\nCompanies with Most Deals:")
        for company_id, count in company_deal_counts.head(10).items():
            company_name = deals_df[deals_df['CompanyID'] == company_id]['CompanyName'].iloc[0]
            print(f"  {company_name} ({company_id}): {count} deals")
        
        # Analyze deal investors if available
        if 'DealInvestorRelation' in self.data:
            deal_inv_df = self.data['DealInvestorRelation']
            print(f"\nTotal deal-investor relationships: {len(deal_inv_df):,}")
            
            # Top investors by number of deals
            investor_deal_counts = deal_inv_df['InvestorID'].value_counts()
            print(f"\nTop 10 Investors by Number of Deals:")
            for investor_id, count in investor_deal_counts.head(10).items():
                investor_name = deal_inv_df[deal_inv_df['InvestorID'] == investor_id]['InvestorName'].iloc[0]
                print(f"  {investor_name} ({investor_id}): {count} deals")
    
    def analyze_company_characteristics(self):
        """Analyze company characteristics."""
        print("\n" + "="*60)
        print("COMPANY CHARACTERISTICS ANALYSIS")
        print("="*60)
        
        if 'Company' not in self.data:
            print("Company data not available")
            return
        
        companies_df = self.data['Company']
        print(f"\nTotal companies: {len(companies_df):,}")
        
        # Analyze by financing status
        if 'CompanyFinancingStatus' in companies_df.columns:
            status_counts = companies_df['CompanyFinancingStatus'].value_counts()
            print(f"\nFinancing Status Distribution:")
            for status, count in status_counts.items():
                print(f"  {status}: {count:,}")
        
        # Analyze by ownership status
        if 'OwnershipStatus' in companies_df.columns:
            ownership_counts = companies_df['OwnershipStatus'].value_counts()
            print(f"\nOwnership Status Distribution:")
            for ownership, count in ownership_counts.items():
                print(f"  {ownership}: {count:,}")
        
        # Analyze by universe
        if 'Universe' in companies_df.columns:
            universe_counts = companies_df['Universe'].value_counts()
            print(f"\nUniverse Distribution:")
            for universe, count in universe_counts.items():
                print(f"  {universe}: {count:,}")
        
        # Companies by employee count
        if 'Employees' in companies_df.columns:
            # Convert to numeric, handling non-numeric values
            employees_numeric = pd.to_numeric(companies_df['Employees'], errors='coerce')
            valid_employees = employees_numeric.dropna()
            
            if len(valid_employees) > 0:
                print(f"\nEmployee Count Statistics:")
                print(f"  Mean: {valid_employees.mean():.1f}")
                print(f"  Median: {valid_employees.median():.1f}")
                print(f"  Min: {valid_employees.min():.0f}")
                print(f"  Max: {valid_employees.max():.0f}")
                
                # Companies with most employees
                top_companies = companies_df.loc[employees_numeric.nlargest(10).index]
                print(f"\nCompanies with Most Employees:")
                for _, company in top_companies.iterrows():
                    print(f"  {company['CompanyName']}: {company['Employees']} employees")
    
    def analyze_investor_characteristics(self):
        """Analyze investor characteristics."""
        print("\n" + "="*60)
        print("INVESTOR CHARACTERISTICS ANALYSIS")
        print("="*60)
        
        if 'Investor' not in self.data:
            print("Investor data not available")
            return
        
        investors_df = self.data['Investor']
        print(f"\nTotal investors: {len(investors_df):,}")
        
        # Analyze by location
        if 'HQLocation' in investors_df.columns:
            location_counts = investors_df['HQLocation'].value_counts()
            print(f"\nTop 10 Investor Locations:")
            for location, count in location_counts.head(10).items():
                print(f"  {location}: {count:,}")
        
        # Analyze by country
        if 'HQCountry' in investors_df.columns:
            country_counts = investors_df['HQCountry'].value_counts()
            print(f"\nInvestor Countries:")
            for country, count in country_counts.items():
                print(f"  {country}: {count:,}")
    
    def find_network_relationships(self):
        """Find interesting network relationships."""
        print("\n" + "="*60)
        print("NETWORK RELATIONSHIP ANALYSIS")
        print("="*60)
        
        # Find companies that are both companies and investors
        if 'Company' in self.data and 'Investor' in self.data:
            companies_df = self.data['Company']
            investors_df = self.data['Investor']
            
            # Check for companies that are also investors
            company_names = set(companies_df['CompanyName'].str.lower())
            investor_names = set(investors_df['InvestorName'].str.lower())
            
            common_names = company_names.intersection(investor_names)
            if common_names:
                print(f"\nCompanies that are also Investors ({len(common_names)}):")
                for name in sorted(list(common_names))[:10]:  # Show first 10
                    print(f"  {name.title()}")
        
        # Analyze co-investment patterns
        if 'InvestorCoInvestorRelation' in self.data:
            co_inv_df = self.data['InvestorCoInvestorRelation']
            print(f"\nTotal co-investor relationships: {len(co_inv_df):,}")
            
            # Most active co-investors
            co_inv_counts = co_inv_df['InvestorID'].value_counts()
            print(f"\nMost Active Co-Investors:")
            for investor_id, count in co_inv_counts.head(10).items():
                # Get the co-investor name from the first occurrence
                co_investor_name = co_inv_df[co_inv_df['InvestorID'] == investor_id]['Co_InvestorName'].iloc[0]
                print(f"  {co_investor_name} ({investor_id}): {count} co-investments")
    
    def generate_summary_report(self):
        """Generate a comprehensive summary report."""
        print("\n" + "="*60)
        print("COMPREHENSIVE SUMMARY REPORT")
        print("="*60)
        
        # Data overview
        total_rows = sum(len(df) for df in self.data.values())
        total_memory = sum(df.memory_usage(deep=True).sum() for df in self.data.values()) / 1024 / 1024
        
        print(f"\nData Overview:")
        print(f"  Total files loaded: {len(self.data)}")
        print(f"  Total rows across all files: {total_rows:,}")
        print(f"  Total memory usage: {total_memory:.1f} MB")
        
        # Key metrics
        if 'Company' in self.data:
            print(f"  Companies: {len(self.data['Company']):,}")
        if 'Investor' in self.data:
            print(f"  Investors: {len(self.data['Investor']):,}")
        if 'Deal' in self.data:
            print(f"  Deals: {len(self.data['Deal']):,}")
        if 'Fund' in self.data:
            print(f"  Funds: {len(self.data['Fund']):,}")
        
        # Relationship counts
        relationship_files = [k for k in self.data.keys() if 'Relation' in k]
        print(f"\nRelationship Files ({len(relationship_files)}):")
        for rel_file in relationship_files:
            print(f"  {rel_file}: {len(self.data[rel_file]):,} relationships")
    
    def run_full_analysis(self):
        """Run the complete analysis."""
        print("PITCHBOOK DATA ANALYSIS")
        print("="*60)
        
        self.get_basic_stats()
        self.analyze_company_investor_relationships()
        self.analyze_deal_data()
        self.analyze_company_characteristics()
        self.analyze_investor_characteristics()
        self.find_network_relationships()
        self.generate_summary_report()
        
        print("\n" + "="*60)
        print("ANALYSIS COMPLETE")
        print("="*60)

def main():
    """Main function to run the analysis."""
    try:
        analyzer = PitchBookAnalyzer()
        analyzer.run_full_analysis()
        
        # Save some key dataframes for further analysis
        print("\nSaving key dataframes for further analysis...")
        if 'Company' in analyzer.data:
            analyzer.data['Company'].to_csv('analysis_output/companies.csv', index=False)
        if 'Investor' in analyzer.data:
            analyzer.data['Investor'].to_csv('analysis_output/investors.csv', index=False)
        if 'CompanyInvestorRelation' in analyzer.data:
            analyzer.data['CompanyInvestorRelation'].to_csv('analysis_output/company_investor_relations.csv', index=False)
        
        print("Analysis complete! Check the analysis_output/ directory for exported files.")
        
    except Exception as e:
        print(f"Error during analysis: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    # Create output directory
    os.makedirs('analysis_output', exist_ok=True)
    main() 