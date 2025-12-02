from pathlib import Path
import pandas as pd
from nyc_sales.extract import DataExtractor as de

class DataCleaner:
    '''
    dogtag: DataCleaner-v1.0
    description: Cleans and prepares NYC sales data. Handles deduplication, header and neighborhood normalization, data type conversions, sale price validation, borough-code mapping, and statistics aggregation.
    '''
    _instance = None
    
    def __new__(cls):
        '''
        dogtag: DataCleaner.__new__-v1.0
        description: Singleton pattern implementation to ensure only one instance of DataCleaner exists.
        '''
        if cls._instance is None:
            cls._instance = super(DataCleaner, cls).__new__(cls)
        return cls._instance

    @classmethod
    def _get_instance(cls):
        '''
        dogtag: DataCleaner._get_instance-v1.0
        description: Returns the singleton instance of DataCleaner, creating it if it doesn't exist.
        '''
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    @classmethod
    def _norm_neighborhood(cls, val):
        '''
        dogtag: DataCleaner._norm_neighborhood-v1.0
        description: Normalizes neighborhood name by stripping, removing extra whitespace, and uppercasing.
        '''
        v = str(val).upper().replace('_', ' ').strip()
        v = ' '.join(v.split())
        return v

    @classmethod
    def _add_stats(cls, df):
        '''
        dogtag: DataCleaner._add_stats-v1.0
        description: Aggregates statistics (min, mean, median, max sale price, number of sales) by borough name, neighborhood, building class category, and year.
        '''
        group_cols = ['BOROUGH NAME', 'NEIGHBORHOOD', 'BUILDING CLASS CATEGORY', 'YEAR']
        df['SALE PRICE'] = pd.to_numeric(df['SALE PRICE'], errors='coerce')
        stats = df.groupby(group_cols)['SALE PRICE'].agg(**{'MIN SALE PRICE': 'min', 'AVG SALE PRICE': 'mean', 'MEDIAN SALE PRICE': 'median', 'MAX SALE PRICE': 'max', 'NUM SALES': 'count'}).reset_index()
        df = df.merge(stats, on=group_cols, how='left')
        return df

    @classmethod
    def _is_header_row(cls, row):
        '''
        dogtag: DataCleaner._is_header_row-v1.0
        description: Checks if a row is a header row by examining if BOROUGH or NEIGHBORHOOD columns contain header text.
        '''
        return (
            (str(row['BOROUGH']).strip().upper() == 'BOROUGH') or
            (str(row['NEIGHBORHOOD']).strip().upper() == 'NEIGHBORHOOD')
        )

    @classmethod
    def clean(cls, src_dir='', trgt_dir='', file_name=''):
        '''
        dogtag: DataCleaner.clean-v1.0
        description: Removes duplicate records, header rows, normalizes data types and neighborhood names, filters invalid sale prices, parses sale dates, maps borough codes to names, aggregates statistics, and calculates YoY changes.
        '''
        src_dir = Path(src_dir)
        trgt_dir = Path(trgt_dir)
        trgt_dir.mkdir(parents=True, exist_ok=True)
        df = de.load(src_dir=src_dir)

        # 1. Remove duplicate rows based on key columns
        df.drop_duplicates(['BOROUGH', 'NEIGHBORHOOD', 'BUILDING CLASS CATEGORY','BLOCK', 'LOT', 'ADDRESS', 'APARTMENT NUMBER', 'SALE DATE', 'ZIP CODE', 'SALE PRICE'], keep='first', inplace=True)

        # 2. Remove rows that are header repeats (e.g., from concatenated Excel files)
        if 'BOROUGH' in df.columns:
            header_mask = df.apply(cls._is_header_row, axis=1)
            df = df[~header_mask]

        # 3. Convert BOROUGH to integer dtype for easier handling and analysis
        df['BOROUGH'] = pd.to_numeric(df['BOROUGH'], errors='coerce').astype(pd.Int64Dtype())

        # 4. Normalize neighborhood names (remove extra spaces, upper case)
        df['NEIGHBORHOOD'] = df['NEIGHBORHOOD'].apply(cls._norm_neighborhood)

        # 5. Remove rows with invalid, zero, or negative sale price
        df = df[pd.to_numeric(df['SALE PRICE'], errors='coerce') > 0]

        # 6. Convert SALE DATE to datetime and extract year
        df = df.assign(**{'SALE DATE': pd.to_datetime(df['SALE DATE'], errors='coerce')}).dropna(subset=['SALE DATE'])
        df['YEAR'] = df['SALE DATE'].dt.year

        # 7. Map borough codes to names (1-5 to Manhattan, Bronx, Brooklyn, Queens, Staten Island)
        df['BOROUGH NAME'] = df['BOROUGH'].map({1: 'MANHATTAN', 2: 'BRONX', 3: 'BROOKLYN', 4: 'QUEENS', 5: 'STATEN ISLAND'})

        # 8. Aggregate statistics (min, mean, median, max sale price, number of sales) by borough name/neighborhood/building class category/year
        df = cls._add_stats(df)

        # 9. Calculate year-over-year (YoY) change in median sale price by borough
        median_by_year = df.groupby(['BOROUGH NAME', 'YEAR'])['SALE PRICE'].median().reset_index()
        median_by_year['MEDIAN PRICE YOY PCT'] = (median_by_year.groupby('BOROUGH NAME')['SALE PRICE'].pct_change() * 100).fillna(0)

        # 10. Merge YoY median price change back into the main DataFrame
        df = pd.merge(
            df, 
            median_by_year[['BOROUGH NAME', 'YEAR', 'MEDIAN PRICE YOY PCT']],
            how='left',
            on=['BOROUGH NAME', 'YEAR']
        )

        # 11. Strip all string columns
        str_cols = df.select_dtypes(include=['object', 'string']).columns
        for col in str_cols:
            df[col] = df[col].astype(str).str.strip()

        df.reset_index(drop=True, inplace=True)
        df.to_csv(trgt_dir / file_name, index=False, encoding='utf-8')
        return df