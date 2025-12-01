import pandas as pd
from pathlib import Path
import re

class DataExtractor:
    """
    dogtag: DataExtractor-v1.0
    description: Provides ETL routines for NYC sales data, including Excel to CSV/Pandas conversion,
                 column normalization, schema validation, and easy batch import/load operations.

    Functions:
        normalize_column(col):
            - Normalizes a given column name: strips whitespace, corrects known variations (e.g., EASE-MENT to EASEMENT),
              replaces various text patterns, and returns the cleaned column name.

        clean(src_dir='', trgt_dir=''):
            - Extracts and cleans raw Excel sales files from a directory.
            - Normalizes column names, checks schema against REQUIRED_COLUMNS, and writes cleaned CSVs to the target location.
            - Prints progress and raises on errors or schema mismatches.

        load(src_dir=''):
            - Loads all cleaned CSV sales files from a directory, concatenates them into a single DataFrame, and returns it.
    """
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DataExtractor, cls).__new__(cls)
        return cls._instance
    
    @classmethod
    def _get_instance(cls):
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
    def extract(cls, src_dir='', trgt_dir=''):
        instance = cls._get_instance()
        errors = []
        src_dir = Path(src_dir)
        trgt_dir = Path(trgt_dir)
        trgt_dir.mkdir(parents=True, exist_ok=True)
        files = list(src_dir.glob('*.xls*'))

        for idx, file in enumerate(files):
            temp_df = pd.read_excel(file, engine='xlrd' if file.suffix == '.xls' else 'openpyxl', header=None)
            header_row_idx = next(
                (i for i, row in enumerate(temp_df.values)
                if [str(x).strip().upper() for x in row[:3]] == ['BOROUGH', 'NEIGHBORHOOD', 'BUILDING CLASS CATEGORY']),
                None)
            if header_row_idx is not None:
                df = pd.read_excel(file, engine='xlrd' if file.suffix == '.xls' else 'openpyxl', header=header_row_idx)
                columns = [instance.normalize_column(col) for col in df.columns]
                df.columns = columns
                if columns != cls.REQUIRED_COLUMNS:
                    errors.append(KeyError(f"Column mismatch in {file}\n{columns}"))
                    continue
                df.dropna(how='all').to_csv(trgt_dir / f"{file.stem}.csv", index=False)
                print(f"{idx + 1}) Saved {file.stem}.csv")
            else:
                errors.append(f"Header row 'BOROUGH' not found in file {file}")
        if errors:
            raise Exception(errors)
        return df

    @classmethod
    def load(cls, src_dir=''):
        src_dir = Path(src_dir)
        dataframes = [pd.read_csv(file) for file in src_dir.glob('*.csv')]
        if not dataframes:
            return pd.DataFrame()
        return pd.concat(dataframes, ignore_index=True)