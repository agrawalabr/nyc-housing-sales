import pandas as pd
from pathlib import Path

class MetricsCalculator:
    '''
    dogtag: MetricsCalculator-v1.0
    description: Computes NYC property sales metrics for borough-by-year affordability, citywide market breadth, and number of tracked neighborhoods.
    '''

    _instance = None
    
    def __new__(cls):
        '''
        dogtag: MetricsCalculator.__new__-v1.0
        description: Singleton pattern implementation to ensure only one instance of MetricsCalculator exists.
        '''
        if cls._instance is None:
            cls._instance = super(MetricsCalculator, cls).__new__(cls)
        return cls._instance
    
    @classmethod
    def _get_instance(cls):
        '''
        dogtag: MetricsCalculator._get_instance-v1.0
        description: Returns the singleton instance of MetricsCalculator, creating it if it doesn't exist.
        '''
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    @classmethod
    def _compute_market_breadth(cls, df):
        '''
        dogtag: MetricsCalculator._compute_market_breadth-v1.0
        description: Calculates market breadth (share of neighborhoods with rising YoY median sale price) and neighborhood counts by year.
        '''
        df = pd.concat((pd.read_csv(f) for f in Path('data/p').glob('*.csv')), ignore_index=True)
        df = df.sort_values(['NEIGHBORHOOD', 'YEAR'])
        df['MEDIAN PRICE YOY PCT'] = df.groupby('NEIGHBORHOOD')['MEDIAN SALE PRICE'].diff()
        valid_df = df.dropna(subset=['MEDIAN PRICE YOY PCT'])
        market_breadth = valid_df.groupby('YEAR')['MEDIAN PRICE YOY PCT'].apply(lambda x: (x > 0).mean())
        num_neighborhoods = valid_df.groupby('YEAR')['NEIGHBORHOOD'].count()
        result = (
            pd.DataFrame({'YEAR': df['YEAR'].unique()})
            .sort_values('YEAR')
            .assign(**{'MARKET BREADTH': lambda r: r['YEAR'].map(market_breadth).astype(float),
                'NUM NEIGHBORHOODS': lambda r: r['YEAR'].map(num_neighborhoods).fillna(0).astype(int)}
            )
        )
        return result

    @classmethod
    def compute(cls, src_dir='', trgt_dir='', file_name=''):
        '''
        dogtag: MetricsCalculator.compute-v1.0
        description: Aggregates affordability and market breadth metrics, outputs a summary matrix as CSV.
        '''
        src_dir = Path(src_dir)
        trgt_dir = Path(trgt_dir)
        trgt_dir.mkdir(parents=True, exist_ok=True)

        all_files = list(src_dir.glob('*.csv'))
        if not all_files:
            return pd.DataFrame()

        df = pd.concat((pd.read_csv(file) for file in all_files), ignore_index=True)

        # Compute the affordability index (25th percentile of median sale price), and aggregate median YoY % change by borough and year
        affordability_df = (
            df.groupby(['BOROUGH NAME', 'YEAR'])
              .agg(
                  **{'AFFORDABILITY INDEX': ('MEDIAN SALE PRICE', lambda x: x.quantile(0.25))}
              )
              .reset_index()
        )
        market_breadth_df = cls._compute_market_breadth(df)
        custom_matrix = affordability_df.merge(
            market_breadth_df, on='YEAR', how='left'
        )

        custom_matrix.to_csv(trgt_dir / file_name, index=False)
        return custom_matrix