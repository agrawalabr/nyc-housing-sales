from pathlib import Path
import pandas as pd
from nyc_sales.extract import DataExtractor as de

class DataCleaner:
    """
    dogtag: DataCleaner-v1.0
    description: Provides cleaning routines for NYC sales data, including duplicate removal, header normalization, data type conversion, validation steps, neighborhood normalization, and statistics aggregation.

    Functions:
        clean(df):
            - Removes duplicate records based on key identifying columns.
            - Removes spurious header rows (e.g., from concatenated Excel files).
            - Converts key columns to numeric or date type where appropriate.
            - Normalizes neighborhood names by trimming and standardizing.
            - Filters out rows with invalid, zero, or negative sale price.
            - Parses sale dates and adds a year column.
            - Maps borough codes (1-5) to borough names for easier interpretation.
        _add_stats(df):
            - Aggregates statistics (min, mean, median, max sale price, number of sales) by borough name, neighborhood, building class category, and year.
        _norm_neighborhood(val):
            - Normalizes neighborhood name by stripping, removing extra whitespace, and uppercasing.
    """
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DataCleaner, cls).__new__(cls)
        return cls._instance

    @classmethod
    def _get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    @classmethod
    def _norm_neighborhood(cls, val):
        v = str(val).upper().replace('_', ' ').strip()
        v = ' '.join(v.split())
        return v

    @classmethod
    def _add_stats(cls, df):
        group_cols = ['BOROUGH NAME', 'NEIGHBORHOOD', 'BUILDING CLASS CATEGORY', 'YEAR']
        df['SALE PRICE'] = pd.to_numeric(df['SALE PRICE'], errors='coerce')
        stats = df.groupby(group_cols)['SALE PRICE'].agg(**{'MIN SALE PRICE': 'min', 'AVG SALE PRICE': 'mean', 'MEDIAN SALE PRICE': 'median', 'MAX SALE PRICE': 'max', 'NUM SALES': 'count'}).reset_index()
        df = df.merge(stats, on=group_cols, how='left')
        return df

    @classmethod
    def _is_header_row(cls, row):
        return (
            (str(row['BOROUGH']).strip().upper() == 'BOROUGH') or
            (str(row['NEIGHBORHOOD']).strip().upper() == 'NEIGHBORHOOD')
        )

    @classmethod
    def clean(cls, src_dir='', trgt_dir='', file_name=''):
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