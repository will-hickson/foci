#!/usr/bin/env python3
"""
Advanced PitchBook Data Analysis
Includes data visualization, network analysis, and deeper insights.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import os
import warnings
warnings.filterwarnings('ignore')

# Set up plotting style
plt.style.use('default')
sns.set_palette("husl")

class AdvancedPitchBookAnalyzer:
    def __init__(self, data_dir='pitchbook_data'):
        """Initialize the advanced analyzer."""
        self.data_dir = Path(data_dir)
        self.data = {}
        self.load_core_data()
    
    def load_core_data(self):
        """Load core data files for analysis."""
        print("Loading core PitchBook data for advanced analysis...")
        
        core_files = [
            'Company.csv',
            'Investor.csv',
            'Deal.csv',
            'CompanyInvestorRelation.csv',
            'DealInvestorRelation.csv'
        ]
        
        for file in core_files:
            file_path = self.data_dir / file
            if file_path.exists():
                try:
                    self.data[file.replace('.csv', '')] = pd.read_csv(file_path)
                    print(f"✓ Loaded {file}")
                except Exception as e:
                    print(f"✗ Error loading {file}: {e}")
    
    def create_company_investor_network(self):
        """Create and analyze the company-investor network."""
        print("\n" + "="*60)
        print("COMPANY-INVESTOR NETWORK ANALYSIS")
        print("="*60)
        
        if 'CompanyInvestorRelation' not in self.data:
            print("CompanyInvestorRelation data not available")
            return
        
        rel_df = self.data['CompanyInvestorRelation']
        
        # Create network metrics
        unique_companies = rel_df['CompanyID'].nunique()
        unique_investors = rel_df['InvestorID'].nunique()
        total_relationships = len(rel_df)
        
        print(f"\nNetwork Statistics:")
        print(f"  Unique Companies: {unique_companies:,}")
        print(f"  Unique Investors: {unique_investors:,}")
        print(f"  Total Relationships: {total_relationships:,}")
        print(f"  Average relationships per company: {total_relationships/unique_companies:.1f}")
        print(f"  Average relationships per investor: {total_relationships/unique_investors:.1f}")
        
        # Analyze network density
        max_possible_relationships = unique_companies * unique_investors
        network_density = total_relationships / max_possible_relationships
        print(f"  Network Density: {network_density:.4f}")
        
        return rel_df
    
    def analyze_investment_patterns(self):
        """Analyze investment patterns and trends."""
        print("\n" + "="*60)
        print("INVESTMENT PATTERN ANALYSIS")
        print("="*60)
        
        if 'CompanyInvestorRelation' not in self.data:
            print("CompanyInvestorRelation data not available")
            return
        
        rel_df = self.data['CompanyInvestorRelation']
        
        # Analyze by investor status
        if 'InvestorStatus' in rel_df.columns:
            status_analysis = rel_df['InvestorStatus'].value_counts()
            print(f"\nInvestment Status Distribution:")
            for status, count in status_analysis.items():
                percentage = (count / len(rel_df)) * 100
                print(f"  {status}: {count:,} ({percentage:.1f}%)")
        
        # Analyze by holding type
        if 'Holding' in rel_df.columns:
            holding_analysis = rel_df['Holding'].value_counts()
            print(f"\nHolding Type Distribution:")
            for holding, count in holding_analysis.items():
                percentage = (count / len(rel_df)) * 100
                print(f"  {holding}: {count:,} ({percentage:.1f}%)")
        
        # Investment timing analysis
        if 'InvestorSince' in rel_df.columns:
            # Convert to datetime and analyze by year
            rel_df['InvestorSince'] = pd.to_datetime(rel_df['InvestorSince'], errors='coerce')
            yearly_investments = rel_df['InvestorSince'].dt.year.value_counts().sort_index()
            
            print(f"\nInvestments by Year:")
            for year, count in yearly_investments.items():
                if pd.notna(year):
                    print(f"  {year}: {count:,} investments")
    
    def create_visualizations(self):
        """Create data visualizations."""
        print("\n" + "="*60)
        print("CREATING DATA VISUALIZATIONS")
        print("="*60)
        
        # Create output directory for plots
        os.makedirs('analysis_output/plots', exist_ok=True)
        
        # 1. Company-Investor Relationship Distribution
        if 'CompanyInvestorRelation' in self.data:
            rel_df = self.data['CompanyInvestorRelation']
            
            # Top investors by number of companies
            investor_counts = rel_df['InvestorID'].value_counts().head(15)
            
            plt.figure(figsize=(12, 8))
            investor_counts.plot(kind='bar')
            plt.title('Top 15 Investors by Number of Companies')
            plt.xlabel('Investor')
            plt.ylabel('Number of Companies')
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            plt.savefig('analysis_output/plots/top_investors.png', dpi=300, bbox_inches='tight')
            plt.close()
            
            # Top companies by number of investors
            company_counts = rel_df['CompanyID'].value_counts().head(15)
            
            plt.figure(figsize=(12, 8))
            company_counts.plot(kind='bar')
            plt.title('Top 15 Companies by Number of Investors')
            plt.xlabel('Company')
            plt.ylabel('Number of Investors')
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            plt.savefig('analysis_output/plots/top_companies.png', dpi=300, bbox_inches='tight')
            plt.close()
        
        # 2. Company characteristics analysis
        if 'Company' in self.data:
            companies_df = self.data['Company']
            
            # Financing status distribution
            if 'CompanyFinancingStatus' in companies_df.columns:
                status_counts = companies_df['CompanyFinancingStatus'].value_counts()
                
                plt.figure(figsize=(10, 8))
                plt.pie(status_counts.values, labels=status_counts.index, autopct='%1.1f%%')
                plt.title('Company Financing Status Distribution')
                plt.tight_layout()
                plt.savefig('analysis_output/plots/financing_status.png', dpi=300, bbox_inches='tight')
                plt.close()
            
            # Employee count distribution
            if 'Employees' in companies_df.columns:
                employees_numeric = pd.to_numeric(companies_df['Employees'], errors='coerce')
                valid_employees = employees_numeric.dropna()
                
                if len(valid_employees) > 0:
                    plt.figure(figsize=(10, 6))
                    plt.hist(valid_employees, bins=20, edgecolor='black')
                    plt.title('Company Employee Count Distribution')
                    plt.xlabel('Number of Employees')
                    plt.ylabel('Number of Companies')
                    plt.tight_layout()
                    plt.savefig('analysis_output/plots/employee_distribution.png', dpi=300, bbox_inches='tight')
                    plt.close()
        
        # 3. Investor location analysis
        if 'Investor' in self.data:
            investors_df = self.data['Investor']
            
            if 'HQLocation' in investors_df.columns:
                location_counts = investors_df['HQLocation'].value_counts().head(15)
                
                plt.figure(figsize=(12, 8))
                location_counts.plot(kind='bar')
                plt.title('Top 15 Investor Locations')
                plt.xlabel('Location')
                plt.ylabel('Number of Investors')
                plt.xticks(rotation=45, ha='right')
                plt.tight_layout()
                plt.savefig('analysis_output/plots/investor_locations.png', dpi=300, bbox_inches='tight')
                plt.close()
        
        print("✓ Visualizations saved to analysis_output/plots/")
    
    def generate_insights_report(self):
        """Generate insights and recommendations."""
        print("\n" + "="*60)
        print("INSIGHTS AND RECOMMENDATIONS")
        print("="*60)
        
        insights = []
        
        if 'CompanyInvestorRelation' in self.data:
            rel_df = self.data['CompanyInvestorRelation']
            
            # Insight 1: Most active investors
            top_investors = rel_df['InvestorID'].value_counts().head(5)
            insights.append("Top 5 Most Active Investors:")
            for investor_id, count in top_investors.items():
                investor_name = rel_df[rel_df['InvestorID'] == investor_id]['InvestorName'].iloc[0]
                insights.append(f"  - {investor_name}: {count} companies")
            
            # Insight 2: Companies with most diverse investor base
            top_companies = rel_df['CompanyID'].value_counts().head(5)
            insights.append("\nCompanies with Most Diverse Investor Base:")
            for company_id, count in top_companies.items():
                company_name = rel_df[rel_df['CompanyID'] == company_id]['CompanyName'].iloc[0]
                insights.append(f"  - {company_name}: {count} investors")
        
        if 'Company' in self.data:
            companies_df = self.data['Company']
            
            # Insight 3: Financing status insights
            if 'CompanyFinancingStatus' in companies_df.columns:
                status_dist = companies_df['CompanyFinancingStatus'].value_counts()
                insights.append(f"\nFinancing Status Insights:")
                insights.append(f"  - Most common status: {status_dist.index[0]} ({status_dist.iloc[0]} companies)")
                insights.append(f"  - {len(status_dist)} different financing statuses identified")
            
            # Insight 4: Employee insights
            if 'Employees' in companies_df.columns:
                employees_numeric = pd.to_numeric(companies_df['Employees'], errors='coerce')
                valid_employees = employees_numeric.dropna()
                
                if len(valid_employees) > 0:
                    insights.append(f"\nEmployee Size Insights:")
                    insights.append(f"  - Average company size: {valid_employees.mean():.1f} employees")
                    insights.append(f"  - Median company size: {valid_employees.median():.1f} employees")
                    insights.append(f"  - Largest company: {valid_employees.max():.0f} employees")
                    insights.append(f"  - Smallest company: {valid_employees.min():.0f} employees")
        
        # Print insights
        for insight in insights:
            print(insight)
    
    def export_analysis_results(self):
        """Export analysis results to CSV files."""
        print("\n" + "="*60)
        print("EXPORTING ANALYSIS RESULTS")
        print("="*60)
        
        # Create analysis output directory
        os.makedirs('analysis_output', exist_ok=True)
        
        if 'CompanyInvestorRelation' in self.data:
            rel_df = self.data['CompanyInvestorRelation']
            
            # Export top investors
            top_investors = rel_df['InvestorID'].value_counts().head(20)
            top_investors_df = pd.DataFrame({
                'InvestorID': top_investors.index,
                'CompanyCount': top_investors.values
            })
            
            # Add investor names
            investor_names = {}
            for investor_id in top_investors.index:
                name = rel_df[rel_df['InvestorID'] == investor_id]['InvestorName'].iloc[0]
                investor_names[investor_id] = name
            
            top_investors_df['InvestorName'] = top_investors_df['InvestorID'].map(investor_names)
            top_investors_df.to_csv('analysis_output/top_investors.csv', index=False)
            
            # Export top companies
            top_companies = rel_df['CompanyID'].value_counts().head(20)
            top_companies_df = pd.DataFrame({
                'CompanyID': top_companies.index,
                'InvestorCount': top_companies.values
            })
            
            # Add company names
            company_names = {}
            for company_id in top_companies.index:
                name = rel_df[rel_df['CompanyID'] == company_id]['CompanyName'].iloc[0]
                company_names[company_id] = name
            
            top_companies_df['CompanyName'] = top_companies_df['CompanyID'].map(company_names)
            top_companies_df.to_csv('analysis_output/top_companies.csv', index=False)
        
        print("✓ Analysis results exported to analysis_output/")
    
    def run_advanced_analysis(self):
        """Run the complete advanced analysis."""
        print("ADVANCED PITCHBOOK DATA ANALYSIS")
        print("="*60)
        
        self.create_company_investor_network()
        self.analyze_investment_patterns()
        self.create_visualizations()
        self.generate_insights_report()
        self.export_analysis_results()
        
        print("\n" + "="*60)
        print("ADVANCED ANALYSIS COMPLETE")
        print("="*60)

def main():
    """Main function to run the advanced analysis."""
    try:
        import os
        analyzer = AdvancedPitchBookAnalyzer()
        analyzer.run_advanced_analysis()
        
    except Exception as e:
        print(f"Error during advanced analysis: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 