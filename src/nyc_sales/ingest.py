import pandas as pd
from pathlib import Path

class DataIngester:
    """
    dogtag: DataIngester-v1.0
    description: Provides ingestion routines for NYC sales data, including aggregation, normalization, and validation steps.

    Functions:
        ingest(df):
            - Ingests sales data from source directory into target directory.
            - Aggregates sales data by borough, neighborhood, building class category, and year.
            - Calculates the number of sales, average sale price, and median sale price.
            - Saves the aggregated data to the target directory.
    """
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DataIngester, cls).__new__(cls)
        return cls._instance
    
    @classmethod
    def _get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    @classmethod
    def ingest(cls, src_dir='', trgt_dir='', file_name=''):
        src_dir = Path(src_dir)
        trgt_dir = Path(trgt_dir)
        trgt_dir.mkdir(parents=True, exist_ok=True)

        all_files = list(src_dir.glob('*.csv'))
        if not all_files:
            return pd.DataFrame()

        df = pd.concat((pd.read_csv(file, usecols=['BOROUGH NAME', 'NEIGHBORHOOD', 'BUILDING CLASS CATEGORY', 'YEAR', 'SALE PRICE']) for file in all_files), ignore_index=True)
        df['SALE PRICE'] = pd.to_numeric(df['SALE PRICE'], errors='coerce')

        df = (df.groupby(['BOROUGH NAME', 'NEIGHBORHOOD', 'BUILDING CLASS CATEGORY', 'YEAR'], as_index=False)
                    .agg(**{
                        'NUM SALES': ('SALE PRICE', 'count'),
                        'AVG SALE PRICE': ('SALE PRICE', 'mean'),
                        'MEDIAN SALE PRICE': ('SALE PRICE', 'median')
                    })
                    )

        for year, df_year in df.groupby('YEAR'):
            year_file = f"{year}_{file_name}"
            df_year.to_csv(trgt_dir / year_file, index=False)

        return df