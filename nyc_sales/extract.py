import requests
import pandas as pd
from pathlib import Path
import re

class DataExtractor:
    '''
    dogtag: DataExtractor-v1.0
    description: ETL routines for NYC sales data—Excel to CSV/Pandas conversion, column normalization, schema validation, and batch import/load.
    '''
    _instance = None
    
    def __new__(cls):
        '''
        dogtag: DataExtractor.__new__-v1.0
        description: Singleton pattern implementation to ensure only one instance of DataExtractor exists.
        '''
        if cls._instance is None:
            cls._instance = super(DataExtractor, cls).__new__(cls)
        return cls._instance
    
    @classmethod
    def _get_instance(cls):
        '''
        dogtag: DataExtractor._get_instance-v1.0
        description: Returns the singleton instance of DataExtractor, creating it if it doesn't exist.
        '''
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    REQUIRED_COLUMNS = [
        'BOROUGH', 'NEIGHBORHOOD', 'BUILDING CLASS CATEGORY', 'TAX CLASS AT PRESENT', 'BLOCK', 'LOT', 'EASEMENT',
        'BUILDING CLASS AT PRESENT', 'ADDRESS', 'APARTMENT NUMBER', 'ZIP CODE', 'RESIDENTIAL UNITS',
        'COMMERCIAL UNITS', 'TOTAL UNITS', 'LAND SQUARE FEET', 'GROSS SQUARE FEET', 'YEAR BUILT',
        'TAX CLASS AT TIME OF SALE', 'BUILDING CLASS AT TIME OF SALE', 'SALE PRICE', 'SALE DATE'
    ]

    @staticmethod
    def normalize_column(col):
        '''
        dogtag: DataExtractor.normalize_column-v1.0
        description: Normalizes a given column name by stripping whitespace, correcting known variations (e.g., EASE-MENT to EASEMENT), and replacing various text patterns.
        '''
        c = str(col).strip()
        if re.fullmatch(r'EASE-?MENT', c, flags=re.IGNORECASE):
            return 'EASEMENT'
        if re.fullmatch(r'TAX CLASS AS.*', c, flags=re.IGNORECASE):
            return 'TAX CLASS AT PRESENT'
        if re.fullmatch(r'BUILDING CLASS AS.*', c, flags=re.IGNORECASE):
            return 'BUILDING CLASS AT PRESENT'
        c = re.sub(r'\n+', ' ', c)
        c = re.sub(r' {2,}', ' ', c)
        c = re.sub(r'\s*UNITS\s*', ' UNITS', c)
        c = re.sub(r'\s*SQUARE FEET\s*', ' SQUARE FEET', c)
        c = re.sub(r'BUILDING CLASS\s*AT TIME OF SALE', 'BUILDING CLASS AT TIME OF SALE', c, flags=re.IGNORECASE)
        c = c.strip()
        return c

    @classmethod
    def download(cls, boroughs, years, suffixes, local_dir):
        '''
        dogtag: DataExtractor.download-v1.0
        description: Downloads NYC sales data files from the official website for specified boroughs, years, and file suffixes to a local directory.
        '''
        local_dir.mkdir(parents=True, exist_ok=True)
        success_downloads = 0
        combos = [(f'https://www.nyc.gov/assets/finance/downloads/pdf/rolling_sales/annualized-sales/{y}/{y}_{b}.{suf}', local_dir / f'{y}_{b}.{suf}')
                for y in years for b in boroughs for suf in suffixes]
        combos += [(f'https://www.nyc.gov/assets/finance/downloads/pdf/rolling_sales/rollingsales_{b}.{suf}', local_dir / f'rollingsales_{b}.{suf}')
                for b in boroughs for suf in suffixes]
        for url, path in combos:
            r = requests.get(url)
            if r.status_code == 200:
                with open(path, 'wb') as f:
                    f.write(r.content)
                    success_downloads += 1
        print(f'{success_downloads} files were downloaded successfully to {local_dir}')

    @classmethod
    def extract(cls, src_dir='', trgt_dir=''):
        '''
        dogtag: DataExtractor.extract-v1.0
        description: Extracts and cleans raw Excel sales files from a directory, normalizes column names, checks schema against REQUIRED_COLUMNS, and writes cleaned CSVs to the target location.
        '''
        instance = cls._get_instance()
        src_dir, trgt_dir = Path(src_dir), Path(trgt_dir)
        trgt_dir.mkdir(parents=True, exist_ok=True)
        errors, df = [], None

        for file in src_dir.glob('*.xls*'):
            engine = 'xlrd' if file.suffix == '.xls' else 'openpyxl'
            temp = pd.read_excel(file, engine=engine, header=None)
            hdr_idx = next((i for i, r in enumerate(temp.values)
                            if [str(x).strip().upper() for x in r[:3]] == ['BOROUGH', 'NEIGHBORHOOD', 'BUILDING CLASS CATEGORY']), None)
            if hdr_idx is not None:
                df = pd.read_excel(file, engine=engine, header=hdr_idx)
                df.columns = [instance.normalize_column(c) for c in df.columns]
                if list(df.columns) != cls.REQUIRED_COLUMNS:
                    errors.append(KeyError(f'Column mismatch in {file}\n{df.columns}'))
                    continue
                df.dropna(how='all').to_csv(trgt_dir / f'{file.stem}.csv', index=False)
            else:
                errors.append(f'Header row "BOROUGH" not found in file {file}')
        if errors:
            raise Exception(errors)
        print(f'{len(list(src_dir.glob('*.xls*')))} files were processed successfully to {trgt_dir}')
        return df

    @classmethod
    def load(cls, src_dir=''):
        '''
        dogtag: DataExtractor.load-v1.0
        description: Loads all cleaned CSV sales files from a directory, concatenates them into a single DataFrame, and returns it.
        '''
        src_dir = Path(src_dir)
        dataframes = [pd.read_csv(file) for file in src_dir.glob('*.csv')]
        if not dataframes:
            return pd.DataFrame()
        return pd.concat(dataframes, ignore_index=True)