import pandas as pd
from pathlib import Path

class DataIngester:
    '''
    dogtag: DataIngester-v1.0
    description: Ingests and aggregates NYC sales data by borough, neighborhood, building class category, and year.
    '''
    _instance = None
    
    def __new__(cls):
        '''
        dogtag: DataIngester.__new__-v1.0
        description: Singleton pattern implementation to ensure only one instance of DataIngester exists.
        '''
        if cls._instance is None:
            cls._instance = super(DataIngester, cls).__new__(cls)
        return cls._instance
    
    @classmethod
    def _get_instance(cls):
        '''
        dogtag: DataIngester._get_instance-v1.0
        description: Returns the singleton instance of DataIngester, creating it if it doesn't exist.
        '''
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    @classmethod
    def ingest(cls, src_dir='', trgt_dir='', file_name=''):
        '''
        dogtag: DataIngester.ingest-v1.0
        description: Ingests sales data from source directory, aggregates by borough, neighborhood, building class category, and year, calculates metrics, and saves to target directory.
        '''
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
            year_file = f'{year}_{file_name}'
            df_year.to_csv(trgt_dir / year_file, index=False)

        return df