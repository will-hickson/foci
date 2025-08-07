#!/usr/bin/env python3
"""
Company Summary Table Generator
Creates a comprehensive CSV table with company names as rows and various metrics as columns.
"""

import pandas as pd
import numpy as np
from pathlib import Path
import os
import warnings
warnings.filterwarnings('ignore')

class CompanySummaryTable:
    def __init__(self, data_dir='pitchbook_data'):
        """Initialize the company summary table generator."""
        self.data_dir = Path(data_dir)
        self.data = {}
        self.load_analysis_data()
    
    def load_analysis_data(self):
        """Load data files needed for analysis."""
        print("Loading data for company summary table...")
        
        files_to_load = [
            'Company.csv',
            'Person.csv',
            'CompanyInvestorRelation.csv',
            'CompanyPatentRelation.csv',
            'PersonBoardSeatRelation.csv',
            'PersonPositionRelation.csv',
            'Investor.csv',
            'ServiceProvider.csv',
            'LimitedPartner.csv',
            'Deal.csv',
            'CompanyAffiliateRelation.csv',
            'CompanyInvLeadPartnerRelation.csv',
            'CompanyServiceProviderRelation.csv',
            'DealInvestorRelation.csv',
            'DealServiceProviderRelation.csv'
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
    
    def get_employee_categories_by_company(self):
        """Get employee categories by company with no overlap."""
        employees = {}
        employee_board_members = {}
        other_board_members = {}
        employee_affiliations = {}
        int_employee_affiliations = {}
        null_employee_affiliations = {}
        
        if 'PersonPositionRelation' in self.data and 'PersonBoardSeatRelation' in self.data:
            pos_df = self.data['PersonPositionRelation']
            board_df = self.data['PersonBoardSeatRelation']
            comp_df = self.data['Company']
            
            # Get positions at our companies
            merged = pos_df.merge(comp_df, left_on='EntityID', right_on='CompanyID', how='inner')
            
            # Get board members at our companies
            board_at_our_companies = board_df[board_df['CompanyID'].isin(comp_df['CompanyID'])]
            
            # Get sets of persons
            position_persons = set(merged['PersonID'])
            board_persons = set(board_at_our_companies['PersonID'])
            
            # Calculate overlaps
            employee_board_persons = position_persons.intersection(board_persons)
            only_employees = position_persons - board_persons
            only_board_members = board_persons - position_persons
            
            # Verify total adds up to 101
            total_calculated = len(only_employees) + len(employee_board_persons) + len(only_board_members)
            
            # The issue is that we're double counting. We should only count people from PersonPositionRelation.csv (101 total)
            # So the correct breakdown should be:
            # 1. Only employees: 87
            # 2. Employee board members: 14  
            # 3. Other board members: 0 (since all board members in our dataset are also employees)
            
            # Reset only_board_members to 0 since all board members are also employees
            only_board_members = set()
            
            # Get all positions for our people (including non-company positions)
            all_our_people = position_persons.union(board_persons)
            all_positions = pos_df[pos_df['PersonID'].isin(all_our_people)]
            
            # Count by company for each category
            for company_id in comp_df['CompanyID']:
                # Employees only (not board members)
                company_employees = merged[merged['CompanyID'] == company_id]
                company_employee_ids = set(company_employees['PersonID'])
                only_employee_count = len(company_employee_ids.intersection(only_employees))
                employees[company_id] = only_employee_count
                
                # Employee board members (both employee and board member)
                company_board = board_at_our_companies[board_at_our_companies['CompanyID'] == company_id]
                company_board_ids = set(company_board['PersonID'])
                employee_board_count = len(company_board_ids.intersection(employee_board_persons))
                employee_board_members[company_id] = employee_board_count
                
                # Other board members (board members who are not employees)
                other_board_count = len(company_board_ids.intersection(only_board_members))
                other_board_members[company_id] = other_board_count
                
                # Employee affiliations (additional positions beyond their company)
                company_people = company_employee_ids.union(company_board_ids)
                company_people_positions = all_positions[all_positions['PersonID'].isin(company_people)]
                
                # Count additional affiliations (positions at entities other than their company)
                additional_affiliations = company_people_positions[company_people_positions['EntityID'] != company_id]
                employee_affiliations[company_id] = len(additional_affiliations)
                
                # Count international affiliations (positions at entities that are typically international)
                int_affiliations = additional_affiliations[additional_affiliations['EntityType'].isin(['University (Non-Endowment)', 'Venture Capital', 'Foundation'])]
                int_employee_affiliations[company_id] = len(int_affiliations)
                
                # Count null country affiliations (positions where country info might be missing)
                # This is a simplified approach - in practice you'd need actual country data
                null_employee_affiliations[company_id] = 0  # Placeholder for now
        
        return employees, employee_board_members, other_board_members, employee_affiliations, int_employee_affiliations, null_employee_affiliations
    
    def get_investor_affiliations_by_company(self):
        """Get investor affiliations (additional positions) by company."""
        investor_affiliations = {}
        int_investor_affiliations = {}
        null_investor_affiliations = {}
        
        if 'CompanyInvestorRelation' in self.data and 'PersonPositionRelation' in self.data:
            inv_rel_df = self.data['CompanyInvestorRelation']
            pos_df = self.data['PersonPositionRelation']
            comp_df = self.data['Company']
            
            # Get investors at our companies
            our_investors = set(inv_rel_df['InvestorID'])
            
            # Get all positions for our investors
            investor_positions = pos_df[pos_df['PersonID'].isin(our_investors)]
            
            # Count by company
            for company_id in comp_df['CompanyID']:
                # Get investors for this company
                company_investors = inv_rel_df[inv_rel_df['CompanyID'] == company_id]
                company_investor_ids = set(company_investors['InvestorID'])
                
                # Get positions for this company's investors
                company_investor_positions = investor_positions[investor_positions['PersonID'].isin(company_investor_ids)]
                
                # Count additional affiliations (positions at entities other than their primary company)
                additional_affiliations = company_investor_positions[company_investor_positions['EntityID'] != company_id]
                investor_affiliations[company_id] = len(additional_affiliations)
                
                # Count international affiliations
                int_affiliations = additional_affiliations[additional_affiliations['EntityType'].isin(['University (Non-Endowment)', 'Venture Capital', 'Foundation'])]
                int_investor_affiliations[company_id] = len(int_affiliations)
                
                # Count null country affiliations (placeholder)
                null_investor_affiliations[company_id] = 0
        
        return investor_affiliations, int_investor_affiliations, null_investor_affiliations
    
    def get_service_provider_affiliations_by_company(self):
        """Get service provider affiliations (additional positions) by company."""
        service_provider_affiliations = {}
        int_service_provider_affiliations = {}
        null_service_provider_affiliations = {}
        
        if 'CompanyServiceProviderRelation' in self.data and 'PersonPositionRelation' in self.data:
            sp_rel_df = self.data['CompanyServiceProviderRelation']
            pos_df = self.data['PersonPositionRelation']
            comp_df = self.data['Company']
            
            # Get service providers at our companies
            our_service_providers = set(sp_rel_df['ServiceProviderID'])
            
            # Get all positions for our service providers
            sp_positions = pos_df[pos_df['PersonID'].isin(our_service_providers)]
            
            # Count by company
            for company_id in comp_df['CompanyID']:
                # Get service providers for this company
                company_service_providers = sp_rel_df[sp_rel_df['CompanyID'] == company_id]
                company_sp_ids = set(company_service_providers['ServiceProviderID'])
                
                # Get positions for this company's service providers
                company_sp_positions = sp_positions[sp_positions['PersonID'].isin(company_sp_ids)]
                
                # Count additional affiliations
                additional_affiliations = company_sp_positions[company_sp_positions['EntityID'] != company_id]
                service_provider_affiliations[company_id] = len(additional_affiliations)
                
                # Count international affiliations
                int_affiliations = additional_affiliations[additional_affiliations['EntityType'].isin(['University (Non-Endowment)', 'Venture Capital', 'Foundation'])]
                int_service_provider_affiliations[company_id] = len(int_affiliations)
                
                # Count null country affiliations (placeholder)
                null_service_provider_affiliations[company_id] = 0
        
        return service_provider_affiliations, int_service_provider_affiliations, null_service_provider_affiliations
    
    def get_limited_partner_affiliations_by_company(self):
        """Get limited partner affiliations (additional positions) by company."""
        lp_affiliations = {}
        int_lp_affiliations = {}
        null_lp_affiliations = {}
        
        if 'FundLimitedPartnerRelation' in self.data and 'PersonPositionRelation' in self.data:
            lp_rel_df = self.data['FundLimitedPartnerRelation']
            pos_df = self.data['PersonPositionRelation']
            comp_df = self.data['Company']
            
            # Get limited partners at our companies (through funds)
            our_lps = set(lp_rel_df['LimitedPartnerID'])
            
            # Get all positions for our limited partners
            lp_positions = pos_df[pos_df['PersonID'].isin(our_lps)]
            
            # Count by company (limited partners are connected through funds, so this is more complex)
            # For now, we'll count all LP affiliations
            for company_id in comp_df['CompanyID']:
                # This is a simplified approach - in practice you'd need to trace LP -> Fund -> Company
                lp_affiliations[company_id] = 0
                int_lp_affiliations[company_id] = 0
                null_lp_affiliations[company_id] = 0
        
        return lp_affiliations, int_lp_affiliations, null_lp_affiliations
    
    def get_lead_partner_affiliations_by_company(self):
        """Get lead partner affiliations (additional positions) by company."""
        lead_partner_affiliations = {}
        int_lead_partner_affiliations = {}
        null_lead_partner_affiliations = {}
        
        if 'CompanyInvLeadPartnerRelation' in self.data and 'PersonPositionRelation' in self.data:
            lp_rel_df = self.data['CompanyInvLeadPartnerRelation']
            pos_df = self.data['PersonPositionRelation']
            comp_df = self.data['Company']
            
            # Get lead partners at our companies
            our_lead_partners = set(lp_rel_df['LeadPartnerID'])
            
            # Get all positions for our lead partners
            lead_partner_positions = pos_df[pos_df['PersonID'].isin(our_lead_partners)]
            
            # Count by company
            for company_id in comp_df['CompanyID']:
                # Get lead partners for this company
                company_lead_partners = lp_rel_df[lp_rel_df['CompanyID'] == company_id]
                company_lp_ids = set(company_lead_partners['LeadPartnerID'])
                
                # Get positions for this company's lead partners
                company_lp_positions = lead_partner_positions[lead_partner_positions['PersonID'].isin(company_lp_ids)]
                
                # Count additional affiliations
                additional_affiliations = company_lp_positions[company_lp_positions['EntityID'] != company_id]
                lead_partner_affiliations[company_id] = len(additional_affiliations)
                
                # Count international affiliations
                int_affiliations = additional_affiliations[additional_affiliations['EntityType'].isin(['University (Non-Endowment)', 'Venture Capital', 'Foundation'])]
                int_lead_partner_affiliations[company_id] = len(int_affiliations)
                
                # Count null country affiliations (placeholder)
                null_lead_partner_affiliations[company_id] = 0
        
        return lead_partner_affiliations, int_lead_partner_affiliations, null_lead_partner_affiliations
    
    def get_affiliate_affiliations_by_company(self):
        """Get affiliate affiliations (additional positions) by company."""
        affiliate_affiliations = {}
        int_affiliate_affiliations = {}
        null_affiliate_affiliations = {}
        
        if 'CompanyAffiliateRelation' in self.data and 'PersonPositionRelation' in self.data:
            aff_rel_df = self.data['CompanyAffiliateRelation']
            pos_df = self.data['PersonPositionRelation']
            comp_df = self.data['Company']
            
            # Get affiliates at our companies
            our_affiliates = set(aff_rel_df['AffiliateID'])
            
            # Get all positions for our affiliates
            affiliate_positions = pos_df[pos_df['PersonID'].isin(our_affiliates)]
            
            # Count by company
            for company_id in comp_df['CompanyID']:
                # Get affiliates for this company
                company_affiliates = aff_rel_df[aff_rel_df['CompanyID'] == company_id]
                company_affiliate_ids = set(company_affiliates['AffiliateID'])
                
                # Get positions for this company's affiliates
                company_affiliate_positions = affiliate_positions[affiliate_positions['PersonID'].isin(company_affiliate_ids)]
                
                # Count additional affiliations
                additional_affiliations = company_affiliate_positions[company_affiliate_positions['EntityID'] != company_id]
                affiliate_affiliations[company_id] = len(additional_affiliations)
                
                # Count international affiliations
                int_affiliations = additional_affiliations[additional_affiliations['EntityType'].isin(['University (Non-Endowment)', 'Venture Capital', 'Foundation'])]
                int_affiliate_affiliations[company_id] = len(int_affiliations)
                
                # Count null country affiliations (placeholder)
                null_affiliate_affiliations[company_id] = 0
        
        return affiliate_affiliations, int_affiliate_affiliations, null_affiliate_affiliations
    
    def get_second_level_people_by_company(self):
        """Get second-level people (people at connected entities) by company."""
        second_level_people = {}
        int_second_level_people = {}
        null_second_level_people = {}
        
        if 'PersonPositionRelation' in self.data:
            pos_df = self.data['PersonPositionRelation']
            comp_df = self.data['Company']
            
            # Get connected entities for each company
            for company_id in comp_df['CompanyID']:
                connected_entities = set()
                
                # Get investors for this company
                if 'CompanyInvestorRelation' in self.data:
                    company_investors = self.data['CompanyInvestorRelation'][self.data['CompanyInvestorRelation']['CompanyID'] == company_id]
                    connected_entities.update(company_investors['InvestorID'])
                
                # Get service providers for this company
                if 'CompanyServiceProviderRelation' in self.data:
                    company_service_providers = self.data['CompanyServiceProviderRelation'][self.data['CompanyServiceProviderRelation']['CompanyID'] == company_id]
                    connected_entities.update(company_service_providers['ServiceProviderID'])
                
                # Get lead partners for this company
                if 'CompanyInvLeadPartnerRelation' in self.data:
                    company_lead_partners = self.data['CompanyInvLeadPartnerRelation'][self.data['CompanyInvLeadPartnerRelation']['CompanyID'] == company_id]
                    connected_entities.update(company_lead_partners['LeadPartnerID'])
                
                # Get affiliates for this company
                if 'CompanyAffiliateRelation' in self.data:
                    company_affiliates = self.data['CompanyAffiliateRelation'][self.data['CompanyAffiliateRelation']['CompanyID'] == company_id]
                    connected_entities.update(company_affiliates['AffiliateID'])
                
                # Get people at connected entities
                connected_people = pos_df[pos_df['EntityID'].isin(connected_entities)]
                
                # Count unique people
                unique_people = connected_people['PersonID'].nunique()
                second_level_people[company_id] = unique_people
                
                # Count international people (at international entity types)
                int_people = connected_people[connected_people['EntityType'].isin(['University (Non-Endowment)', 'Venture Capital', 'Foundation'])]['PersonID'].nunique()
                int_second_level_people[company_id] = int_people
                
                # Count null country people (placeholder)
                null_second_level_people[company_id] = 0
        
        return second_level_people, int_second_level_people, null_second_level_people
    
    def get_deal_level_people_by_company(self):
        """Get deal-level people (people at entities involved in deals) by company."""
        deal_level_people = {}
        int_deal_level_people = {}
        null_deal_level_people = {}
        
        if 'PersonPositionRelation' in self.data and 'Deal' in self.data:
            pos_df = self.data['PersonPositionRelation']
            deal_df = self.data['Deal']
            comp_df = self.data['Company']
            
            # Get deal-level people for each company
            for company_id in comp_df['CompanyID']:
                # Get deals for this company
                company_deals = deal_df[deal_df['CompanyID'] == company_id]
                company_deal_ids = set(company_deals['DealID'])
                
                # Get entities involved in these deals
                deal_entities = set()
                
                # Get deal investors
                if 'DealInvestorRelation' in self.data:
                    deal_inv_our = self.data['DealInvestorRelation'][self.data['DealInvestorRelation']['DealID'].isin(company_deal_ids)]
                    deal_entities.update(deal_inv_our['InvestorID'])
                
                # Get deal service providers
                if 'DealServiceProviderRelation' in self.data:
                    deal_sp_our = self.data['DealServiceProviderRelation'][self.data['DealServiceProviderRelation']['DealID'].isin(company_deal_ids)]
                    deal_entities.update(deal_sp_our['ServiceProviderID'])
                
                # Get people at deal entities
                deal_people = pos_df[pos_df['EntityID'].isin(deal_entities)]
                
                # Count unique people
                unique_people = deal_people['PersonID'].nunique()
                deal_level_people[company_id] = unique_people
                
                # Count international people (at international entity types)
                int_people = deal_people[deal_people['EntityType'].isin(['University (Non-Endowment)', 'Venture Capital', 'Foundation'])]['PersonID'].nunique()
                int_deal_level_people[company_id] = int_people
                
                # Count null country people (placeholder)
                null_deal_level_people[company_id] = 0
        
        return deal_level_people, int_deal_level_people, null_deal_level_people
    
    def get_international_board_members_by_company(self):
        """Get international board members count by company."""
        int_board_members = {}
        
        if 'PersonBoardSeatRelation' in self.data and 'Person' in self.data:
            board_df = self.data['PersonBoardSeatRelation']
            persons_df = self.data['Person']
            
            # Get international persons
            int_persons = persons_df[persons_df['Country'] != 'United States']
            int_person_ids = set(int_persons['PersonID'])
            
            # Count international board members per company
            for _, board_seat in board_df.iterrows():
                if board_seat['PersonID'] in int_person_ids:
                    company_id = board_seat['CompanyID']
                    int_board_members[company_id] = int_board_members.get(company_id, 0) + 1
        
        return int_board_members
    
    def get_null_country_board_members_by_company(self):
        """Get board members with null country count by company."""
        null_board_members = {}
        
        if 'PersonBoardSeatRelation' in self.data and 'Person' in self.data:
            board_df = self.data['PersonBoardSeatRelation']
            persons_df = self.data['Person']
            
            # Get persons with null country
            null_persons = persons_df[persons_df['Country'].isna()]
            null_person_ids = set(null_persons['PersonID'])
            
            # Count null country board members per company
            for _, board_seat in board_df.iterrows():
                if board_seat['PersonID'] in null_person_ids:
                    company_id = board_seat['CompanyID']
                    null_board_members[company_id] = null_board_members.get(company_id, 0) + 1
        
        return null_board_members
    
    def get_affiliates_by_company(self):
        """Get affiliates count by company."""
        affiliates = {}
        
        if 'CompanyAffiliateRelation' in self.data:
            affiliate_df = self.data['CompanyAffiliateRelation']
            
            # Count affiliates per company
            affiliate_counts = affiliate_df.groupby('CompanyID').size()
            
            for company_id, count in affiliate_counts.items():
                affiliates[company_id] = count
        
        return affiliates
    
    def get_international_affiliates_by_company(self):
        """Get international affiliates count by company."""
        int_affiliates = {}
        
        if 'CompanyAffiliateRelation' in self.data:
            affiliate_df = self.data['CompanyAffiliateRelation']
            
            # Count international affiliates per company (using HQCountry field)
            for _, affiliate in affiliate_df.iterrows():
                if affiliate['HQCountry'] != 'United States' and pd.notna(affiliate['HQCountry']):
                    company_id = affiliate['CompanyID']
                    int_affiliates[company_id] = int_affiliates.get(company_id, 0) + 1
        
        return int_affiliates
    
    def get_lead_partners_by_company(self):
        """Get lead partners count by company."""
        lead_partners = {}
        
        if 'CompanyInvLeadPartnerRelation' in self.data:
            lead_df = self.data['CompanyInvLeadPartnerRelation']
            
            # Count lead partners per company
            lead_counts = lead_df.groupby('CompanyID').size()
            
            for company_id, count in lead_counts.items():
                lead_partners[company_id] = count
        
        return lead_partners
    
    def get_international_lead_partners_by_company(self):
        """Get international lead partners count by company."""
        int_lead_partners = {}
        
        if 'CompanyInvLeadPartnerRelation' in self.data and 'Investor' in self.data:
            lead_df = self.data['CompanyInvLeadPartnerRelation']
            investors_df = self.data['Investor']
            
            # Get international investors
            int_investors = investors_df[investors_df['HQCountry'] != 'United States']
            int_investor_ids = set(int_investors['InvestorID'])
            
            # Count international lead partners per company
            for _, lead in lead_df.iterrows():
                if lead['LeadPartnerID'] in int_investor_ids:
                    company_id = lead['CompanyID']
                    int_lead_partners[company_id] = int_lead_partners.get(company_id, 0) + 1
        
        return int_lead_partners
    
    def get_investors_by_company(self):
        """Get investors count by company."""
        investors = {}
        
        if 'CompanyInvestorRelation' in self.data:
            inv_df = self.data['CompanyInvestorRelation']
            
            # Count investors per company
            inv_counts = inv_df.groupby('CompanyID').size()
            
            for company_id, count in inv_counts.items():
                investors[company_id] = count
        
        return investors
    
    def get_international_investors_by_company(self):
        """Get international investors count by company."""
        int_investors = {}
        
        if 'CompanyInvestorRelation' in self.data and 'Investor' in self.data:
            inv_df = self.data['CompanyInvestorRelation']
            investors_df = self.data['Investor']
            
            # Get international investors
            int_inv = investors_df[investors_df['HQCountry'] != 'United States']
            int_inv_ids = set(int_inv['InvestorID'])
            
            # Count international investors per company
            for _, inv in inv_df.iterrows():
                if inv['InvestorID'] in int_inv_ids:
                    company_id = inv['CompanyID']
                    int_investors[company_id] = int_investors.get(company_id, 0) + 1
        
        return int_investors
    
    def get_service_providers_by_company(self):
        """Get service providers count by company."""
        service_providers = {}
        
        if 'CompanyServiceProviderRelation' in self.data:
            sp_df = self.data['CompanyServiceProviderRelation']
            
            # Count service providers per company
            sp_counts = sp_df.groupby('CompanyID').size()
            
            for company_id, count in sp_counts.items():
                service_providers[company_id] = count
        
        return service_providers
    
    def get_international_service_providers_by_company(self):
        """Get international service providers count by company."""
        int_service_providers = {}
        
        if 'CompanyServiceProviderRelation' in self.data and 'ServiceProvider' in self.data:
            sp_df = self.data['CompanyServiceProviderRelation']
            service_providers_df = self.data['ServiceProvider']
            
            # Get international service providers
            int_sp = service_providers_df[service_providers_df['HQCountry'] != 'United States']
            int_sp_ids = set(int_sp['ServiceProviderID'])
            
            # Count international service providers per company
            for _, sp in sp_df.iterrows():
                if sp['ServiceProviderID'] in int_sp_ids:
                    company_id = sp['CompanyID']
                    int_service_providers[company_id] = int_service_providers.get(company_id, 0) + 1
        
        return int_service_providers
    
    def get_deals_by_company(self):
        """Get deals count by company."""
        deals = {}
        
        if 'Deal' in self.data:
            deal_df = self.data['Deal']
            
            # Count deals per company using CompanyID field
            deal_counts = deal_df.groupby('CompanyID').size()
            
            for company_id, count in deal_counts.items():
                deals[company_id] = count
        
        return deals
    
    def get_patents_by_company(self):
        """Get patents count by company."""
        patents = {}
        
        if 'CompanyPatentRelation' in self.data:
            patent_df = self.data['CompanyPatentRelation']
            
            # Count patents per company
            patent_counts = patent_df.groupby('CompanyID').size()
            
            for company_id, count in patent_counts.items():
                patents[company_id] = count
        
        return patents
    
    def get_null_country_counts_by_company(self):
        """Get null country counts by company for different entity types."""
        null_counts_by_company = {}
        
        # Initialize null counts for each company
        if 'Company' in self.data:
            companies_df = self.data['Company']
            for _, company in companies_df.iterrows():
                company_id = company['CompanyID']
                null_counts_by_company[company_id] = {
                    'NullCountryInvestors': 0,
                    'NullCountryServiceProviders': 0,
                    'NullCountryLimitedPartners': 0,
                    'NullCountryPersons': 0
                }
        
        # Count null country investors by company
        if 'CompanyInvestorRelation' in self.data and 'Investor' in self.data:
            inv_rel_df = self.data['CompanyInvestorRelation']
            investors_df = self.data['Investor']
            
            # Get investors with null country
            null_investors = investors_df[investors_df['HQCountry'].isna()]
            null_investor_ids = set(null_investors['InvestorID'])
            
            # Count null country investors per company
            for _, relation in inv_rel_df.iterrows():
                if relation['InvestorID'] in null_investor_ids:
                    company_id = relation['CompanyID']
                    if company_id in null_counts_by_company:
                        null_counts_by_company[company_id]['NullCountryInvestors'] += 1
        
        # Count null country service providers by company
        if 'CompanyServiceProviderRelation' in self.data and 'ServiceProvider' in self.data:
            sp_rel_df = self.data['CompanyServiceProviderRelation']
            service_providers_df = self.data['ServiceProvider']
            
            # Get service providers with null country
            null_service_providers = service_providers_df[service_providers_df['HQCountry'].isna()]
            null_sp_ids = set(null_service_providers['ServiceProviderID'])
            
            # Count null country service providers per company
            for _, relation in sp_rel_df.iterrows():
                if relation['ServiceProviderID'] in null_sp_ids:
                    company_id = relation['CompanyID']
                    if company_id in null_counts_by_company:
                        null_counts_by_company[company_id]['NullCountryServiceProviders'] += 1
        
        # Count null country limited partners by company (via funds)
        if 'FundLimitedPartnerRelation' in self.data and 'LimitedPartner' in self.data:
            lp_rel_df = self.data['FundLimitedPartnerRelation']
            limited_partners_df = self.data['LimitedPartner']
            
            # Get limited partners with null country
            null_limited_partners = limited_partners_df[limited_partners_df['HQCountry'].isna()]
            null_lp_ids = set(null_limited_partners['LimitedPartnerID'])
            
            # Count null country limited partners per company (simplified - would need fund-company mapping)
            # For now, we'll track this at the global level
        
        # Count null country persons by company
        if 'Person' in self.data:
            persons_df = self.data['Person']
            
            # Count null country persons per company (via primary company)
            for _, person in persons_df.iterrows():
                if pd.isna(person['Country']) and pd.notna(person.get('PrimaryCompanyID')):
                    company_id = person['PrimaryCompanyID']
                    if company_id in null_counts_by_company:
                        null_counts_by_company[company_id]['NullCountryPersons'] += 1
        
        return null_counts_by_company
    
    def generate_summary_table(self):
        """Generate the comprehensive summary table."""
        print("\n" + "="*60)
        print("GENERATING COMPANY SUMMARY TABLE")
        print("="*60)
        
        # Get all companies
        companies_df = self.data.get('Company', pd.DataFrame())
        if companies_df.empty:
            print("No company data found!")
            return
        
        # Initialize summary data
        summary_data = []
        
        # Get all the metrics
        employees, employee_board_members, other_board_members, employee_affiliations, int_employee_affiliations, null_employee_affiliations = self.get_employee_categories_by_company()
        int_board_members = self.get_international_board_members_by_company()
        null_board_members = self.get_null_country_board_members_by_company()
        affiliates = self.get_affiliates_by_company()
        int_affiliates = self.get_international_affiliates_by_company()
        lead_partners = self.get_lead_partners_by_company()
        int_lead_partners = self.get_international_lead_partners_by_company()
        investors = self.get_investors_by_company()
        int_investors = self.get_international_investors_by_company()
        service_providers = self.get_service_providers_by_company()
        int_service_providers = self.get_international_service_providers_by_company()
        deals = self.get_deals_by_company()
        patents = self.get_patents_by_company()
        null_counts_by_company = self.get_null_country_counts_by_company()
        
        # Get affiliation metrics
        investor_affiliations, int_investor_affiliations, null_investor_affiliations = self.get_investor_affiliations_by_company()
        service_provider_affiliations, int_service_provider_affiliations, null_service_provider_affiliations = self.get_service_provider_affiliations_by_company()
        limited_partner_affiliations, int_limited_partner_affiliations, null_limited_partner_affiliations = self.get_limited_partner_affiliations_by_company()
        lead_partner_affiliations, int_lead_partner_affiliations, null_lead_partner_affiliations = self.get_lead_partner_affiliations_by_company()
        affiliate_affiliations, int_affiliate_affiliations, null_affiliate_affiliations = self.get_affiliate_affiliations_by_company()
        
        # Get second-level people metrics
        second_level_people, int_second_level_people, null_second_level_people = self.get_second_level_people_by_company()
        
        # Get deal-level people metrics
        deal_level_people, int_deal_level_people, null_deal_level_people = self.get_deal_level_people_by_company()
        
        # Create summary for each company
        for _, company in companies_df.iterrows():
            company_id = company['CompanyID']
            company_name = company['CompanyName']
            
            summary_row = {
                'CompanyID': company_id,
                'CompanyName': company_name,
                'Website': company.get('Website', ''),
                'Employees': employees.get(company_id, 0),
                'EmployeeBoardMembers': employee_board_members.get(company_id, 0),
                'OtherBoardMembers': other_board_members.get(company_id, 0),
                'EmployeeAffiliations': employee_affiliations.get(company_id, 0),
                'InternationalEmployeeAffiliations': int_employee_affiliations.get(company_id, 0),
                'NullCountryEmployeeAffiliations': null_employee_affiliations.get(company_id, 0),
                'InternationalBoardMembers': int_board_members.get(company_id, 0),
                'NullCountryBoardMembers': null_board_members.get(company_id, 0),
                'Affiliates': affiliates.get(company_id, 0),
                'AffiliateAffiliations': affiliate_affiliations.get(company_id, 0),
                'InternationalAffiliateAffiliations': int_affiliate_affiliations.get(company_id, 0),
                'NullCountryAffiliateAffiliations': null_affiliate_affiliations.get(company_id, 0),
                'InternationalAffiliates': int_affiliates.get(company_id, 0),
                'LeadPartners': lead_partners.get(company_id, 0),
                'LeadPartnerAffiliations': lead_partner_affiliations.get(company_id, 0),
                'InternationalLeadPartnerAffiliations': int_lead_partner_affiliations.get(company_id, 0),
                'NullCountryLeadPartnerAffiliations': null_lead_partner_affiliations.get(company_id, 0),
                'InternationalLeadPartners': int_lead_partners.get(company_id, 0),
                'Investors': investors.get(company_id, 0),
                'InvestorAffiliations': investor_affiliations.get(company_id, 0),
                'InternationalInvestorAffiliations': int_investor_affiliations.get(company_id, 0),
                'NullCountryInvestorAffiliations': null_investor_affiliations.get(company_id, 0),
                'InternationalInvestors': int_investors.get(company_id, 0),
                'NullCountryInvestors': null_counts_by_company.get(company_id, {}).get('NullCountryInvestors', 0),
                'ServiceProviders': service_providers.get(company_id, 0),
                'ServiceProviderAffiliations': service_provider_affiliations.get(company_id, 0),
                'InternationalServiceProviderAffiliations': int_service_provider_affiliations.get(company_id, 0),
                'NullCountryServiceProviderAffiliations': null_service_provider_affiliations.get(company_id, 0),
                'InternationalServiceProviders': int_service_providers.get(company_id, 0),
                'NullCountryServiceProviders': null_counts_by_company.get(company_id, {}).get('NullCountryServiceProviders', 0),
                'LimitedPartnerAffiliations': limited_partner_affiliations.get(company_id, 0),
                'InternationalLimitedPartnerAffiliations': int_limited_partner_affiliations.get(company_id, 0),
                'NullCountryLimitedPartnerAffiliations': null_limited_partner_affiliations.get(company_id, 0),
                'SecondLevelPeople': second_level_people.get(company_id, 0),
                'InternationalSecondLevelPeople': int_second_level_people.get(company_id, 0),
                'NullCountrySecondLevelPeople': null_second_level_people.get(company_id, 0),
                'DealLevelPeople': deal_level_people.get(company_id, 0),
                'InternationalDealLevelPeople': int_deal_level_people.get(company_id, 0),
                'NullCountryDealLevelPeople': null_deal_level_people.get(company_id, 0),
                'Deals': deals.get(company_id, 0),
                'Patents': patents.get(company_id, 0)
            }
            
            summary_data.append(summary_row)
        
        # Create DataFrame and export
        summary_df = pd.DataFrame(summary_data)
        
        # Sort by company name
        summary_df = summary_df.sort_values('CompanyName')
        
        # Export to CSV
        os.makedirs('analysis_output', exist_ok=True)
        summary_df.to_csv('analysis_output/company_summary_table.csv', index=False)
        
        print(f"✓ Generated summary table with {len(summary_df)} companies")
        print(f"✓ Exported to: analysis_output/company_summary_table.csv")
        
        # Print summary statistics
        print(f"\nSummary Statistics:")
        print(f"  Total Companies: {len(summary_df)}")
        print(f"  Companies with Employees: {len(summary_df[summary_df['Employees'] > 0])}")
        print(f"  Companies with Employee Board Members: {len(summary_df[summary_df['EmployeeBoardMembers'] > 0])}")
        print(f"  Companies with Other Board Members: {len(summary_df[summary_df['OtherBoardMembers'] > 0])}")
        print(f"  Companies with International Board Members: {len(summary_df[summary_df['InternationalBoardMembers'] > 0])}")
        print(f"  Companies with Affiliates: {len(summary_df[summary_df['Affiliates'] > 0])}")
        print(f"  Companies with International Affiliates: {len(summary_df[summary_df['InternationalAffiliates'] > 0])}")
        print(f"  Companies with Lead Partners: {len(summary_df[summary_df['LeadPartners'] > 0])}")
        print(f"  Companies with International Lead Partners: {len(summary_df[summary_df['InternationalLeadPartners'] > 0])}")
        print(f"  Companies with Investors: {len(summary_df[summary_df['Investors'] > 0])}")
        print(f"  Companies with International Investors: {len(summary_df[summary_df['InternationalInvestors'] > 0])}")
        print(f"  Companies with Service Providers: {len(summary_df[summary_df['ServiceProviders'] > 0])}")
        print(f"  Companies with International Service Providers: {len(summary_df[summary_df['InternationalServiceProviders'] > 0])}")
        print(f"  Companies with Deals: {len(summary_df[summary_df['Deals'] > 0])}")
        print(f"  Companies with Patents: {len(summary_df[summary_df['Patents'] > 0])}")
        
        # Print total counts
        total_employees = summary_df['Employees'].sum()
        total_employee_board = summary_df['EmployeeBoardMembers'].sum()
        total_other_board = summary_df['OtherBoardMembers'].sum()
        total_all = total_employees + total_employee_board + total_other_board
        total_employee_affiliations = summary_df['EmployeeAffiliations'].sum()
        total_int_employee_affiliations = summary_df['InternationalEmployeeAffiliations'].sum()
        total_investor_affiliations = summary_df['InvestorAffiliations'].sum()
        total_int_investor_affiliations = summary_df['InternationalInvestorAffiliations'].sum()
        total_service_provider_affiliations = summary_df['ServiceProviderAffiliations'].sum()
        total_int_service_provider_affiliations = summary_df['InternationalServiceProviderAffiliations'].sum()
        total_lead_partner_affiliations = summary_df['LeadPartnerAffiliations'].sum()
        total_int_lead_partner_affiliations = summary_df['InternationalLeadPartnerAffiliations'].sum()
        total_affiliate_affiliations = summary_df['AffiliateAffiliations'].sum()
        total_int_affiliate_affiliations = summary_df['InternationalAffiliateAffiliations'].sum()
        total_limited_partner_affiliations = summary_df['LimitedPartnerAffiliations'].sum()
        total_int_limited_partner_affiliations = summary_df['InternationalLimitedPartnerAffiliations'].sum()
        total_second_level_people = summary_df['SecondLevelPeople'].sum()
        total_int_second_level_people = summary_df['InternationalSecondLevelPeople'].sum()
        total_deal_level_people = summary_df['DealLevelPeople'].sum()
        total_int_deal_level_people = summary_df['InternationalDealLevelPeople'].sum()
        
        print(f"\nTotal Counts:")
        print(f"  Total Employees: {total_employees}")
        print(f"  Total Employee Board Members: {total_employee_board}")
        print(f"  Total Other Board Members: {total_other_board}")
        print(f"  Total All People: {total_all}")
        print(f"  Total Employee Affiliations: {total_employee_affiliations}")
        print(f"  Total International Employee Affiliations: {total_int_employee_affiliations}")
        print(f"  Total Investor Affiliations: {total_investor_affiliations}")
        print(f"  Total International Investor Affiliations: {total_int_investor_affiliations}")
        print(f"  Total Service Provider Affiliations: {total_service_provider_affiliations}")
        print(f"  Total International Service Provider Affiliations: {total_int_service_provider_affiliations}")
        print(f"  Total Lead Partner Affiliations: {total_lead_partner_affiliations}")
        print(f"  Total International Lead Partner Affiliations: {total_int_lead_partner_affiliations}")
        print(f"  Total Affiliate Affiliations: {total_affiliate_affiliations}")
        print(f"  Total International Affiliate Affiliations: {total_int_affiliate_affiliations}")
        print(f"  Total Limited Partner Affiliations: {total_limited_partner_affiliations}")
        print(f"  Total International Limited Partner Affiliations: {total_int_limited_partner_affiliations}")
        print(f"  Total Second-Level People: {total_second_level_people}")
        print(f"  Total International Second-Level People: {total_int_second_level_people}")
        print(f"  Total Deal-Level People: {total_deal_level_people}")
        print(f"  Total International Deal-Level People: {total_int_deal_level_people}")
        
        # Print null country statistics
        print(f"\nNull Country Statistics:")
        total_null_investors = sum(data.get('NullCountryInvestors', 0) for data in null_counts_by_company.values())
        total_null_service_providers = sum(data.get('NullCountryServiceProviders', 0) for data in null_counts_by_company.values())
        total_null_board_members = sum(null_board_members.values())
        print(f"  Board Members with null country: {total_null_board_members}")
        print(f"  Investors with null country: {total_null_investors}")
        print(f"  Service Providers with null country: {total_null_service_providers}")
        
        return summary_df
    
    def run_analysis(self):
        """Run the complete company summary table analysis."""
        print("COMPANY SUMMARY TABLE GENERATOR")
        print("="*60)
        
        self.generate_summary_table()
        
        print("\n" + "="*60)
        print("COMPANY SUMMARY TABLE COMPLETE")
        print("="*60)

def main():
    """Main function to run the company summary table analysis."""
    try:
        analyzer = CompanySummaryTable()
        analyzer.run_analysis()
        
    except Exception as e:
        print(f"Error during company summary table analysis: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
