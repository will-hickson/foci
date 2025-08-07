# PitchBook Data Analysis

This project provides comprehensive analysis tools for PitchBook CSV data. The scripts are designed to load data into memory for fast analysis and evaluation purposes.

## Overview

The analysis includes:
- **Basic Analysis** (`pitchbook_analysis.py`): Comprehensive data loading and basic statistics
- **Advanced Analysis** (`advanced_analysis.py`): Data visualization, network analysis, and insights
- **In-Memory Processing**: All data is loaded into memory for fast analysis
- **Data Export**: Results are saved to CSV files and visualizations

## Data Structure

The PitchBook data contains the following key entities and relationships:

### Core Entities:
- **Company**: Central entity with CompanyID as primary key
- **Investor**: Investment entities with InvestorID as primary key
- **Person**: Individual people with PersonID as primary key
- **Fund**: Investment funds with FundID as primary key
- **Deal**: Investment deals with DealID as primary key
- **LimitedPartner**: LP entities
- **ServiceProvider**: Service companies

### Key Relationships:
- Company ↔ Investor (via CompanyInvestorRelation.csv)
- Company ↔ Deal (via Deal.csv with CompanyID)
- Deal ↔ Investor (via DealInvestorRelation.csv)
- Person ↔ Company (via Person.csv with PrimaryCompanyID)
- Fund ↔ Investor (via FundInvestorRelation.csv)

## Installation

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Ensure data is in the correct location:**
   ```
   /ValidEval/foci/
   ├── pitchbook_data/
   │   ├── Company.csv
   │   ├── Investor.csv
   │   ├── Deal.csv
   │   └── ... (other CSV files)
   ├── pitchbook_analysis.py
   ├── advanced_analysis.py
   └── requirements.txt
   ```

## Usage

### Basic Analysis

Run the comprehensive basic analysis:

```bash
python pitchbook_analysis.py
```

This will:
- Load all CSV files (skipping files larger than 50MB)
- Generate basic statistics for each dataset
- Analyze company-investor relationships
- Analyze deal data
- Analyze company and investor characteristics
- Find network relationships
- Export key dataframes to `analysis_output/`

### Advanced Analysis

Run the advanced analysis with visualizations:

```bash
python advanced_analysis.py
```

This will:
- Create company-investor network analysis
- Analyze investment patterns and trends
- Generate data visualizations (saved to `analysis_output/plots/`)
- Generate insights and recommendations
- Export analysis results to CSV files

## Output Files

### Basic Analysis Output:
- `analysis_output/companies.csv` - Company data
- `analysis_output/investors.csv` - Investor data
- `analysis_output/company_investor_relations.csv` - Relationship data

### Advanced Analysis Output:
- `analysis_output/top_investors.csv` - Top investors by company count
- `analysis_output/top_companies.csv` - Top companies by investor count
- `analysis_output/plots/` - Data visualizations (PNG files)

## Data Analysis Features

### Network Analysis
- Company-investor relationship mapping
- Network density calculations
- Most active investors and companies
- Investment pattern analysis

### Statistical Analysis
- Company financing status distribution
- Employee count statistics
- Investor location analysis
- Deal frequency analysis

### Visualization
- Top investors by number of companies
- Top companies by number of investors
- Company financing status pie chart
- Employee count distribution histogram
- Investor location bar chart

## Data Volume Assessment

The total dataset is approximately 250MB, making it perfect for in-memory analysis:

- **Core data**: ~73MB (excluding large files)
- **Most files**: Under 1MB each
- **Largest files**: 
  - Person.csv (35MB)
  - PersonAffiliatedDealRelation.csv (16MB)
  - PersonPositionRelation.csv (12MB)
  - PatentCPCCode.csv (177MB) - excluded by default

## Why In-Memory Processing?

1. **Speed**: 10-100x faster than database queries
2. **Flexibility**: Easy complex analyses and transformations
3. **No Setup**: No database installation or configuration
4. **Cost**: No database licensing or infrastructure costs
5. **Iterative**: Perfect for exploratory data analysis

## Customization

### Loading Different Files

To load specific files, modify the `core_files` and `relation_files` lists in the scripts:

```python
core_files = [
    'Company.csv',
    'Investor.csv',
    # Add or remove files as needed
]
```

### Adjusting File Size Limits

To change the file size limit for loading:

```python
if file_size < 50 * 1024 * 1024:  # 50MB limit
    # Load file
```

### Adding Custom Analysis

Add new analysis methods to the `PitchBookAnalyzer` class:

```python
def my_custom_analysis(self):
    """Custom analysis method."""
    # Your analysis code here
    pass
```

## Troubleshooting

### Common Issues:

1. **Memory Error**: Reduce the file size limit or load fewer files
2. **File Not Found**: Ensure CSV files are in the `pitchbook_data/` directory
3. **Import Error**: Install required packages with `pip install -r requirements.txt`

### Performance Tips:

1. **Large Files**: The scripts automatically skip files larger than 50MB
2. **Memory Usage**: Monitor memory usage during analysis
3. **Selective Loading**: Load only the files you need for your analysis

## Example Output

```
PITCHBOOK DATA ANALYSIS
============================================================

Loading PitchBook data...
✓ Loaded Company.csv (18 rows)
✓ Loaded Investor.csv (59 rows)
✓ Loaded Deal.csv (65 rows)
✓ Loaded CompanyInvestorRelation.csv (85 rows)

Total files loaded: 4

============================================================
BASIC DATA STATISTICS
============================================================

Company:
  Rows: 18
  Columns: 35
  Memory usage: 0.0 MB

CompanyInvestorRelation:
  Rows: 85
  Columns: 12
  Memory usage: 0.0 MB

============================================================
COMPANY-INVESTOR RELATIONSHIP ANALYSIS
============================================================

Total company-investor relationships: 85

Investor Status Distribution:
  Active: 75
  Former: 10

Top 10 Investors by Number of Companies:
  National Aeronautics and Space Administration (114726-97): 8 companies
  United States Department of Agriculture (52587-46): 6 companies
  U. S. National Science Foundation (51038-20): 5 companies
  ...
```

## License

This project is for evaluation purposes. Please ensure you have appropriate permissions to use the PitchBook data.
