#!/usr/bin/env python3
"""
Company Analysis with Specific Plots
Generates plots for international entities, people, patents, and board members by company.
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

class CompanyAnalysisPlots:
    def __init__(self, data_dir='pitchbook_data'):
        """Initialize the company analysis."""
        self.data_dir = Path(data_dir)
        self.data = {}
        self.load_analysis_data()
    
    def load_analysis_data(self):
        """Load data files needed for analysis."""
        print("Loading data for company analysis...")
        
        files_to_load = [
            'Company.csv',
            'Person.csv',
            'CompanyInvestorRelation.csv',
            'CompanyPatentRelation.csv',
            'PersonBoardSeatRelation.csv',
            'Investor.csv',
            'ServiceProvider.csv',
            'LimitedPartner.csv'
        ]
        
        for file in files_to_load:
            file_path = self.data_dir / file
            if file_path.exists():
                try:
                    self.data[file.replace('.csv', '')] = pd.read_csv(file_path)
                    print(f"✓ Loaded {file}")
                except Exception as e:
                    print(f"✗ Error loading {file}: {e}")
        
        print(f"\nTotal files loaded: {len(self.data)}")
    
    def analyze_international_entities_by_company(self):
        """Analyze international entities (investors, service providers, limited partners) by company."""
        print("\n" + "="*60)
        print("INTERNATIONAL ENTITIES BY COMPANY ANALYSIS")
        print("="*60)
        
        company_international_counts = {}
        
        # Get all companies
        if 'Company' in self.data:
            companies_df = self.data['Company']
            for _, company in companies_df.iterrows():
                company_id = company['CompanyID']
                company_name = company['CompanyName']
                company_international_counts[company_id] = {
                    'CompanyName': company_name,
                    'InternationalInvestors': 0,
                    'InternationalServiceProviders': 0,
                    'InternationalLimitedPartners': 0,
                    'TotalInternationalEntities': 0
                }
        
        # Count international investors by company
        if 'CompanyInvestorRelation' in self.data and 'Investor' in self.data:
            rel_df = self.data['CompanyInvestorRelation']
            investors_df = self.data['Investor']
            
            # Get international investors
            int_investors = investors_df[investors_df['HQCountry'] != 'United States']
            int_investor_ids = set(int_investors['InvestorID'])
            
            # Count international investor connections by company
            for _, relation in rel_df.iterrows():
                if relation['InvestorID'] in int_investor_ids:
                    company_id = relation['CompanyID']
                    if company_id in company_international_counts:
                        company_international_counts[company_id]['InternationalInvestors'] += 1
                        company_international_counts[company_id]['TotalInternationalEntities'] += 1
        
        # Count international service providers (connected via deals)
        if 'ServiceProvider' in self.data:
            service_providers_df = self.data['ServiceProvider']
            int_service_providers = service_providers_df[service_providers_df['HQCountry'] != 'United States']
            
            # Note: Service providers are connected via deals, not directly to companies
            # This would require DealServiceProviderRelation data for accurate counting
        
        # Count international limited partners (connected via funds)
        if 'LimitedPartner' in self.data:
            limited_partners_df = self.data['LimitedPartner']
            int_limited_partners = limited_partners_df[limited_partners_df['HQCountry'] != 'United States']
            
            # Note: Limited partners are connected via funds, not directly to companies
            # This would require FundLimitedPartnerRelation data for accurate counting
        
        return company_international_counts
    
    def analyze_international_people_by_company(self):
        """Analyze international people by company."""
        print("\n" + "="*60)
        print("INTERNATIONAL PEOPLE BY COMPANY ANALYSIS")
        print("="*60)
        
        company_international_people = {}
        
        # Get all companies
        if 'Company' in self.data:
            companies_df = self.data['Company']
            for _, company in companies_df.iterrows():
                company_id = company['CompanyID']
                company_name = company['CompanyName']
                company_international_people[company_id] = {
                    'CompanyName': company_name,
                    'InternationalPeople': 0
                }
        
        # Count international people by company
        if 'Person' in self.data:
            persons_df = self.data['Person']
            int_persons = persons_df[persons_df['Country'] != 'United States']
            
            # Count international people with primary company connections
            for _, person in int_persons.iterrows():
                if pd.notna(person.get('PrimaryCompanyID')):
                    company_id = person['PrimaryCompanyID']
                    if company_id in company_international_people:
                        company_international_people[company_id]['InternationalPeople'] += 1
        
        return company_international_people
    
    def analyze_patents_by_company(self):
        """Analyze patents by company."""
        print("\n" + "="*60)
        print("PATENTS BY COMPANY ANALYSIS")
        print("="*60)
        
        company_patents = {}
        
        # Get all companies
        if 'Company' in self.data:
            companies_df = self.data['Company']
            for _, company in companies_df.iterrows():
                company_id = company['CompanyID']
                company_name = company['CompanyName']
                company_patents[company_id] = {
                    'CompanyName': company_name,
                    'PatentCount': 0
                }
        
        # Count patents by company
        if 'CompanyPatentRelation' in self.data:
            patents_df = self.data['CompanyPatentRelation']
            
            for _, patent in patents_df.iterrows():
                company_id = patent['CompanyID']
                if company_id in company_patents:
                    company_patents[company_id]['PatentCount'] += 1
        
        return company_patents
    
    def analyze_board_members_with_multiple_positions(self):
        """Analyze board members with high numbers of other positions held."""
        print("\n" + "="*60)
        print("BOARD MEMBERS WITH MULTIPLE POSITIONS ANALYSIS")
        print("="*60)
        
        # Count board positions per person
        if 'PersonBoardSeatRelation' in self.data:
            board_seats_df = self.data['PersonBoardSeatRelation']
            
            # Count board positions per person
            person_board_counts = board_seats_df['PersonID'].value_counts()
            
            # Get people with multiple board positions
            people_with_multiple_boards = person_board_counts[person_board_counts > 1]
            
            print(f"Total unique board members: {len(person_board_counts)}")
            print(f"Board members with multiple positions: {len(people_with_multiple_boards)}")
            
            # Get top board members by number of positions
            top_board_members = people_with_multiple_boards.head(20)
            
            print(f"\nTop 20 Board Members by Number of Positions:")
            for person_id, count in top_board_members.items():
                # Get person name if available
                person_name = "Unknown"
                if 'Person' in self.data:
                    person_info = self.data['Person'][self.data['Person']['PersonID'] == person_id]
                    if not person_info.empty:
                        person_name = person_info.iloc[0]['FullName']
                
                print(f"  {person_name} ({person_id}): {count} board positions")
            
            return person_board_counts, people_with_multiple_boards
        
        return None, None
    
    def create_plots(self):
        """Create the specific plots requested."""
        print("\n" + "="*60)
        print("CREATING COMPANY ANALYSIS PLOTS")
        print("="*60)
        
        # Create output directory
        os.makedirs('analysis_output/plots', exist_ok=True)
        
        # 1. International entities by company
        company_int_entities = self.analyze_international_entities_by_company()
        if company_int_entities:
            # Convert to DataFrame for plotting
            int_entities_data = []
            for company_id, data in company_int_entities.items():
                int_entities_data.append({
                    'CompanyID': company_id,
                    'CompanyName': data['CompanyName'],
                    'InternationalEntities': data['TotalInternationalEntities']
                })
            
            int_entities_df = pd.DataFrame(int_entities_data)
            int_entities_df = int_entities_df.sort_values('InternationalEntities', ascending=False)
            
            # Plot international entities by company
            plt.figure(figsize=(12, 8))
            companies_with_int_entities = int_entities_df[int_entities_df['InternationalEntities'] > 0]
            if len(companies_with_int_entities) > 0:
                plt.bar(range(len(companies_with_int_entities)), companies_with_int_entities['InternationalEntities'])
                plt.title('International Entities by Company')
                plt.xlabel('Companies')
                plt.ylabel('Number of International Entities')
                plt.xticks(range(len(companies_with_int_entities)), companies_with_int_entities['CompanyName'], rotation=45, ha='right')
                plt.tight_layout()
                plt.savefig('analysis_output/plots/international_entities_by_company.png', dpi=300, bbox_inches='tight')
                plt.close()
                print("✓ Created international entities by company plot")
            
            # Add null count information to the plot
            if 'Investor' in self.data:
                investors_df = self.data['Investor']
                null_investors = investors_df['HQCountry'].isna().sum()
                print(f"  Note: {null_investors} investors have null country values")
        
        # 2. International people by company
        company_int_people = self.analyze_international_people_by_company()
        if company_int_people:
            # Convert to DataFrame for plotting
            int_people_data = []
            for company_id, data in company_int_people.items():
                int_people_data.append({
                    'CompanyID': company_id,
                    'CompanyName': data['CompanyName'],
                    'InternationalPeople': data['InternationalPeople']
                })
            
            int_people_df = pd.DataFrame(int_people_data)
            int_people_df = int_people_df.sort_values('InternationalPeople', ascending=False)
            
            # Plot international people by company
            plt.figure(figsize=(12, 8))
            companies_with_int_people = int_people_df[int_people_df['InternationalPeople'] > 0]
            if len(companies_with_int_people) > 0:
                plt.bar(range(len(companies_with_int_people)), companies_with_int_people['InternationalPeople'])
                plt.title('International People by Company')
                plt.xlabel('Companies')
                plt.ylabel('Number of International People')
                plt.xticks(range(len(companies_with_int_people)), companies_with_int_people['CompanyName'], rotation=45, ha='right')
                plt.tight_layout()
                plt.savefig('analysis_output/plots/international_people_by_company.png', dpi=300, bbox_inches='tight')
                plt.close()
                print("✓ Created international people by company plot")
            
            # Add null count information to the plot
            if 'Person' in self.data:
                persons_df = self.data['Person']
                null_persons = persons_df['Country'].isna().sum()
                print(f"  Note: {null_persons} persons have null country values")
        
        # 3. Patents by company
        company_patents = self.analyze_patents_by_company()
        if company_patents:
            # Convert to DataFrame for plotting
            patents_data = []
            for company_id, data in company_patents.items():
                patents_data.append({
                    'CompanyID': company_id,
                    'CompanyName': data['CompanyName'],
                    'PatentCount': data['PatentCount']
                })
            
            patents_df = pd.DataFrame(patents_data)
            patents_df = patents_df.sort_values('PatentCount', ascending=False)
            
            # Plot patents by company
            plt.figure(figsize=(12, 8))
            companies_with_patents = patents_df[patents_df['PatentCount'] > 0]
            if len(companies_with_patents) > 0:
                plt.bar(range(len(companies_with_patents)), companies_with_patents['PatentCount'])
                plt.title('Patents by Company')
                plt.xlabel('Companies')
                plt.ylabel('Number of Patents')
                plt.xticks(range(len(companies_with_patents)), companies_with_patents['CompanyName'], rotation=45, ha='right')
                plt.tight_layout()
                plt.savefig('analysis_output/plots/patents_by_company.png', dpi=300, bbox_inches='tight')
                plt.close()
                print("✓ Created patents by company plot")
        
        # 4. Board members with multiple positions
        person_board_counts, people_with_multiple_boards = self.analyze_board_members_with_multiple_positions()
        if person_board_counts is not None:
            # Plot board members by number of positions
            plt.figure(figsize=(15, 8))
            top_board_members = person_board_counts.head(20)
            
            # Get actual names for the top board members
            board_member_names = []
            for person_id in top_board_members.index:
                person_name = "Unknown"
                if 'Person' in self.data:
                    person_info = self.data['Person'][self.data['Person']['PersonID'] == person_id]
                    if not person_info.empty:
                        person_name = person_info.iloc[0]['FullName']
                board_member_names.append(person_name)
            
            plt.bar(range(len(top_board_members)), top_board_members.values)
            plt.title('Top 20 Board Members by Number of Board Positions')
            plt.xlabel('Board Members')
            plt.ylabel('Number of Board Positions')
            plt.xticks(range(len(top_board_members)), board_member_names, rotation=45, ha='right')
            plt.tight_layout()
            plt.savefig('analysis_output/plots/board_members_multiple_positions.png', dpi=300, bbox_inches='tight')
            plt.close()
            print("✓ Created board members multiple positions plot")
    
    def generate_summary_statistics(self):
        """Generate summary statistics for the analysis."""
        print("\n" + "="*60)
        print("SUMMARY STATISTICS")
        print("="*60)
        
        summary_stats = {}
        
        # International entities by company
        company_int_entities = self.analyze_international_entities_by_company()
        if company_int_entities:
            int_entities_counts = [data['TotalInternationalEntities'] for data in company_int_entities.values()]
            summary_stats['InternationalEntities'] = {
                'TotalCompanies': len(company_int_entities),
                'CompaniesWithInternationalEntities': len([c for c in int_entities_counts if c > 0]),
                'TotalInternationalEntities': sum(int_entities_counts),
                'AverageInternationalEntities': np.mean(int_entities_counts),
                'MaxInternationalEntities': max(int_entities_counts) if int_entities_counts else 0
            }
        
        # International people by company
        company_int_people = self.analyze_international_people_by_company()
        if company_int_people:
            int_people_counts = [data['InternationalPeople'] for data in company_int_people.values()]
            summary_stats['InternationalPeople'] = {
                'TotalCompanies': len(company_int_people),
                'CompaniesWithInternationalPeople': len([c for c in int_people_counts if c > 0]),
                'TotalInternationalPeople': sum(int_people_counts),
                'AverageInternationalPeople': np.mean(int_people_counts),
                'MaxInternationalPeople': max(int_people_counts) if int_people_counts else 0
            }
        
        # Patents by company
        company_patents = self.analyze_patents_by_company()
        if company_patents:
            patent_counts = [data['PatentCount'] for data in company_patents.values()]
            summary_stats['Patents'] = {
                'TotalCompanies': len(company_patents),
                'CompaniesWithPatents': len([c for c in patent_counts if c > 0]),
                'TotalPatents': sum(patent_counts),
                'AveragePatents': np.mean(patent_counts),
                'MaxPatents': max(patent_counts) if patent_counts else 0
            }
        
        # Board members with multiple positions
        person_board_counts, people_with_multiple_boards = self.analyze_board_members_with_multiple_positions()
        if person_board_counts is not None:
            summary_stats['BoardMembers'] = {
                'TotalBoardMembers': len(person_board_counts),
                'BoardMembersWithMultiplePositions': len(people_with_multiple_boards),
                'AveragePositionsPerBoardMember': person_board_counts.mean(),
                'MaxPositionsPerBoardMember': person_board_counts.max(),
                'MedianPositionsPerBoardMember': person_board_counts.median()
            }
        
        # Print summary statistics
        for category, stats in summary_stats.items():
            print(f"\n{category} Statistics:")
            for stat_name, value in stats.items():
                if isinstance(value, float):
                    print(f"  {stat_name}: {value:.2f}")
                else:
                    print(f"  {stat_name}: {value}")
        
        return summary_stats
    
    def export_analysis_data(self):
        """Export analysis data to CSV files."""
        print("\n" + "="*60)
        print("EXPORTING ANALYSIS DATA")
        print("="*60)
        
        import os
        os.makedirs('analysis_output', exist_ok=True)
        
        # Export international entities by company
        company_int_entities = self.analyze_international_entities_by_company()
        if company_int_entities:
            int_entities_data = []
            for company_id, data in company_int_entities.items():
                int_entities_data.append({
                    'CompanyID': company_id,
                    'CompanyName': data['CompanyName'],
                    'InternationalInvestors': data['InternationalInvestors'],
                    'InternationalServiceProviders': data['InternationalServiceProviders'],
                    'InternationalLimitedPartners': data['InternationalLimitedPartners'],
                    'TotalInternationalEntities': data['TotalInternationalEntities']
                })
            
            int_entities_df = pd.DataFrame(int_entities_data)
            int_entities_df.to_csv('analysis_output/international_entities_by_company.csv', index=False)
            print("✓ Exported international entities by company data")
        
        # Export international people by company
        company_int_people = self.analyze_international_people_by_company()
        if company_int_people:
            int_people_data = []
            for company_id, data in company_int_people.items():
                int_people_data.append({
                    'CompanyID': company_id,
                    'CompanyName': data['CompanyName'],
                    'InternationalPeople': data['InternationalPeople']
                })
            
            int_people_df = pd.DataFrame(int_people_data)
            int_people_df.to_csv('analysis_output/international_people_by_company.csv', index=False)
            print("✓ Exported international people by company data")
        
        # Export patents by company
        company_patents = self.analyze_patents_by_company()
        if company_patents:
            patents_data = []
            for company_id, data in company_patents.items():
                patents_data.append({
                    'CompanyID': company_id,
                    'CompanyName': data['CompanyName'],
                    'PatentCount': data['PatentCount']
                })
            
            patents_df = pd.DataFrame(patents_data)
            patents_df.to_csv('analysis_output/patents_by_company.csv', index=False)
            print("✓ Exported patents by company data")
        
        # Export board members with multiple positions
        person_board_counts, people_with_multiple_boards = self.analyze_board_members_with_multiple_positions()
        if person_board_counts is not None:
            board_data = []
            for person_id, count in person_board_counts.items():
                person_name = "Unknown"
                if 'Person' in self.data:
                    person_info = self.data['Person'][self.data['Person']['PersonID'] == person_id]
                    if not person_info.empty:
                        person_name = person_info.iloc[0]['FullName']
                
                board_data.append({
                    'PersonID': person_id,
                    'PersonName': person_name,
                    'BoardPositionCount': count
                })
            
            board_df = pd.DataFrame(board_data)
            board_df = board_df.sort_values('BoardPositionCount', ascending=False)
            board_df.to_csv('analysis_output/board_members_multiple_positions.csv', index=False)
            print("✓ Exported board members multiple positions data")
    
    def run_analysis(self):
        """Run the complete company analysis."""
        print("COMPANY ANALYSIS WITH SPECIFIC PLOTS")
        print("="*60)
        
        self.create_plots()
        self.generate_summary_statistics()
        self.export_analysis_data()
        
        print("\n" + "="*60)
        print("COMPANY ANALYSIS COMPLETE")
        print("="*60)

def main():
    """Main function to run the company analysis."""
    try:
        analyzer = CompanyAnalysisPlots()
        analyzer.run_analysis()
        
    except Exception as e:
        print(f"Error during company analysis: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 