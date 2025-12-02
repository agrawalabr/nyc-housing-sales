import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from pathlib import Path

plt.style.use('default')
sns.set_theme()

class Visualizer:
    '''
    dogtag: Visualizer-v1.0
    description: Publication-quality visualization engine for NYC housing metrics, producing clear, journal-ready figures and analyses for urban housing trends.
    '''

    FIGSIZE_LANDSCAPE = (12, 7)
    DEFAULT_OUTDIR = Path('data/v')
    YEARS = list(range(2015, 2026))
    BOROUGH_ORDER = ['MANHATTAN', 'BRONX', 'BROOKLYN', 'QUEENS', 'STATEN ISLAND']

    @staticmethod
    def _find_col(df, colname):
        '''
        dogtag: Visualizer._find_col-v1.0
        description: Return DataFrame column matching colname (case-insensitive); raise if not found.
        '''
        for c in df.columns:
            if str(c) == colname or str(c).lower() == colname.lower():
                return c
        raise KeyError(f'Column "{colname}" not found (tried case-insensitive match)')

    @staticmethod
    def _format_millions(x, _):
        '''
        dogtag: Visualizer._format_millions-v1.0
        description: Formats numeric value in millions as a dollar string (e.g., $1.5M).
        '''
        return f'${x/1e6:.1f}M'

    @classmethod
    def savefig(cls, fig, name, outdir=None):
        '''
        dogtag: Visualizer.savefig-v1.0
        description: Saves a matplotlib figure to the specified output directory with high DPI resolution.
        '''
        outdir = Path(outdir) if outdir else cls.DEFAULT_OUTDIR
        outdir.mkdir(exist_ok=True, parents=True)
        fig.savefig(str(outdir / name), dpi=300, bbox_inches='tight')
        plt.close(fig)

    @classmethod
    def _prepare_boroughs(cls, df, borough_col):
        '''
        dogtag: Visualizer._prepare_boroughs-v1.0
        description: Prepares borough list from DataFrame, maintaining consistent ordering according to BOROUGH_ORDER.
        '''
        boroughs = df[borough_col].dropna().str.upper().unique()
        # Maintain consistent ordering
        return [b for b in cls.BOROUGH_ORDER if b in boroughs] + [b for b in boroughs if b not in cls.BOROUGH_ORDER]

    @classmethod
    def create_borough_trajectories(cls, df, price_col='MEDIAN SALE PRICE', year_col='YEAR', borough_col='BOROUGH NAME', figsize=None):
        '''
        dogtag: Visualizer.create_borough_trajectories-v1.0
        description: Creates a line plot showing median sale price trajectories over time for each NYC borough, with markers for key years.
        '''
        figsize = figsize or cls.FIGSIZE_LANDSCAPE
        price_col = cls._find_col(df, price_col)
        year_col = cls._find_col(df, year_col)
        borough_col = cls._find_col(df, borough_col)
        fig, ax = plt.subplots(figsize=figsize)

        boroughs = cls._prepare_boroughs(df, borough_col)
        colors = sns.color_palette('tab10', len(boroughs))
        df[borough_col] = df[borough_col].str.upper()

        for i, bor in enumerate(boroughs):
            mask = df[borough_col] == bor
            group = (df[mask].groupby(year_col)[price_col].median()).reindex(cls.YEARS)
            ax.plot(cls.YEARS, group, label=bor.title(), marker='o', linewidth=2, markersize=7, color=colors[i])
            for mark_year, size in [(2019, 75), (2020, 75), (2025, 95)]:
                price = group.get(mark_year, np.nan)
                if pd.notna(price):
                    ax.scatter(mark_year, price, s=size, marker='D', color=colors[i], edgecolor='black', zorder=5)

        ax.axvline(2020, color='gray', linestyle='--', alpha=0.6, lw=2, label='2020 (COVID)')
        ax.axvline(2017, color='purple', linestyle=':', alpha=0.6, lw=2, label='2017 (Prior Peak)')
        ax.set_xlabel('Year', fontsize=13, fontweight='bold')
        ax.set_ylabel('Median Sale Price ($)', fontsize=13, fontweight='bold')
        ax.set_title('NYC Borough Median Sale Price Trajectories (2015–2025)\nMarkers: Pre-COVID, COVID, and 2025', fontsize=15, fontweight='bold', pad=15)
        ax.legend(title='Borough', ncol=2)
        ax.grid(True, alpha=0.4)
        ax.set_xticks(cls.YEARS)
        ax.yaxis.set_major_formatter(plt.FuncFormatter(cls._format_millions))
        return fig

    @classmethod
    def create_affordability_index_plot(cls, df, borough_col='BOROUGH NAME', affordability_col='AFFORDABILITY INDEX', year_col='YEAR', figsize=None):
        '''
        dogtag: Visualizer.create_affordability_index_plot-v1.0
        description: Creates a plot showing borough entry-level affordability index (25th percentile of median sale price) over time with annotations for steepest declines.
        '''
        figsize = figsize or cls.FIGSIZE_LANDSCAPE
        affordability_col = cls._find_col(df, affordability_col)
        year_col = cls._find_col(df, year_col)
        borough_col = cls._find_col(df, borough_col)
        fig, ax = plt.subplots(figsize=figsize)

        boroughs = cls._prepare_boroughs(df, borough_col)
        colors = sns.color_palette('tab10', len(boroughs))
        df[borough_col] = df[borough_col].str.upper()

        declines = []
        df[year_col] = pd.to_numeric(df[year_col], errors='coerce')
        for i, bor in enumerate(boroughs):
            mask = df[borough_col] == bor
            data_ = df[mask].groupby(year_col)[affordability_col].median().reindex(cls.YEARS)
            ax.plot(cls.YEARS, data_, label=bor.title(), marker='o', linewidth=2, markersize=7, color=colors[i])
            v_2019, v_2025 = data_.get(2019, np.nan), data_.get(2025, np.nan)
            if pd.notna(v_2019) and v_2019 != 0 and pd.notna(v_2025):
                declines.append((bor, 100 * (1 - v_2025 / v_2019)))

        # Annotate steepest decline
        if declines:
            steepest_bor, steepest = max(declines, key=lambda x: x[1])
            y = df[(df[borough_col] == steepest_bor) & (df[year_col] == 2025)][affordability_col].median()
            ax.annotate(f'Steepest decline: {steepest_bor.title()}\nDrop: {steepest:.1f}%',
                        xy=(2025, y), xytext=(2022, y*0.8 if y > 0 else 0.9),
                        arrowprops=dict(arrowstyle='->', color='red', lw=1.5),
                        fontsize=12, color='red', fontweight='bold', backgroundcolor='white'
            )

        ax.set_xlabel('Year', fontsize=13, fontweight='bold')
        ax.set_ylabel('Affordability Index ($)', fontsize=13, fontweight='bold')
        ax.set_title('Borough Entry-level Affordability (25th Percentile, 2015-2025)', fontsize=15, fontweight='bold', pad=15)
        ax.legend(title='Borough')
        ax.grid(True, alpha=0.4)
        ax.set_xticks(cls.YEARS)
        ax.yaxis.set_major_formatter(plt.FuncFormatter(cls._format_millions))
        for year, color_, label_ in [(2019, 'grey', 'Pre-COVID (2019)'), (2020, 'black', '2020 (COVID)'), (2025, 'blue', '2025')]:
            ax.axvline(year, color=color_, linewidth=1.5, linestyle='--', alpha=0.45, label=label_)
        return fig

    @classmethod
    def create_market_breadth_plot(cls, df, year_col='YEAR', breadth_col='MARKET BREADTH', figsize=(11, 6)):
        '''
        dogtag: Visualizer.create_market_breadth_plot-v1.0
        description: Creates a plot showing the percentage of NYC neighborhoods with YoY median price growth over time.
        '''
        year_col = cls._find_col(df, year_col)
        breadth_col = cls._find_col(df, breadth_col)
        df = df.copy()
        df[year_col] = pd.to_numeric(df[year_col], errors='coerce')
        valid_years = [y for y in cls.YEARS if y in df[year_col].values]
        if not valid_years:
            valid_years = sorted(df[year_col].dropna().unique())
        values = (df.groupby(year_col)[breadth_col].mean().reindex(valid_years).values) * 100
        x = np.array(valid_years)
        fig, ax = plt.subplots(figsize=figsize)
        color = sns.color_palette('deep')[0]
        ax.plot(x, values, 'o-', linewidth=2.5, markersize=8, color=color, alpha=0.88, zorder=2)
        ax.fill_between(x, values, alpha=0.17, color=color)
        ax.axhline(50, color='red', linestyle='--', linewidth=1.25, alpha=0.55, label='50% Threshold')

        # Markers for special years
        special_years = {2020: dict(marker='D', s=120, color='black', edgecolor='red', label='2020 (COVID)'),
                         2025: dict(marker='D', s=135, color='blue', edgecolor='black', label='2025')}
        for yr, opts in special_years.items():
            if yr in x:
                idx = np.where(x == yr)[0][0]
                ax.scatter(yr, values[idx], **opts, zorder=5)

        handles, labels = ax.get_legend_handles_labels()
        if handles:
            ax.legend(handles, labels, loc='upper right', fontsize=10, frameon=True)
        ax.set(xlabel='Year', ylabel='Market Breadth (% of Neighborhoods)',
               title='Market Breadth: % of NYC Neighborhoods with YoY Median Price Growth',
               ylim=(0, 100), xlim=(cls.YEARS[0], cls.YEARS[-1]))
        ax.set_xlabel(ax.get_xlabel(), fontsize=13, fontweight='bold')
        ax.set_ylabel(ax.get_ylabel(), fontsize=13, fontweight='bold')
        ax.set_title(ax.get_title(), fontsize=15, fontweight='bold', pad=15)
        ax.set_xticks(cls.YEARS)
        ax.grid(True, alpha=0.3, linestyle='-')
        fig.tight_layout()
        return fig

    @classmethod
    def create_2025_snapshot(cls, df, price_col='MEDIAN SALE PRICE', neighborhood_col='NEIGHBORHOOD', year_col='YEAR', top_n=10, figsize=(14, 8)):
        '''
        dogtag: Visualizer.create_2025_snapshot-v1.0
        description: Creates horizontal bar charts showing top and bottom NYC neighborhoods by median sale price in 2025, with reference markers for 2019 and 2017 values.
        '''
        price_col_actual = cls._find_col(df, price_col)
        year_col_actual = cls._find_col(df, year_col)
        neighborhood_col_actual = cls._find_col(df, neighborhood_col)
        dfc = df[[year_col_actual, price_col_actual, neighborhood_col_actual]].copy()
        dfc[year_col_actual] = pd.to_numeric(dfc[year_col_actual], errors='coerce')
        df_2025 = dfc[dfc[year_col_actual] == 2025]
        if df_2025.empty:
            fig, ax = plt.subplots(figsize=figsize)
            ax.text(0.5, 0.5, 'No 2025 data available', ha='center', va='center', fontsize=18)
            ax.axis('off')
            return fig

        medians_2025 = df_2025.groupby(neighborhood_col_actual)[price_col_actual].median().dropna()
        top = medians_2025.nlargest(top_n)
        bottom = medians_2025.nsmallest(top_n)

        def bar_plot(neigh_data, title, ref2019, ref2017, color, ref2019_color, ref2017_color, y_label):
            ref_marker_map = {'2019': 'o', '2017': 's'} 
            fig, ax = plt.subplots(figsize=(figsize[0] * 0.93, figsize[1] * 1.01), dpi=110)
            bars = ax.barh(
                neigh_data.index[::-1], 
                neigh_data.values[::-1]/1e6, 
                color=color, edgecolor='black', alpha=0.89, height=0.75, zorder=2
            )
            for i, name in enumerate(neigh_data.index[::-1]):
                v = neigh_data[name]
                ax.text(
                    v/1e6 + 0.035, i, f'${v/1e6:,.2f}M',
                    va='center', ha='left', fontsize=13, fontweight='bold',
                    color='#203040', zorder=5,
                    bbox=dict(facecolor='white', alpha=0.6, boxstyle='round,pad=0.10', linewidth=0)
                )

                for ref, ref_color, yr, dx in [
                    (ref2019.get(name), ref2019_color, '2019', 0.05),
                    (ref2017.get(name), ref2017_color, '2017', 0.10),
                ]:
                    if pd.notna(ref):
                        ax.scatter(ref/1e6, i, marker=ref_marker_map[yr], color=ref_color, edgecolor='black', s=70, zorder=6)

            ax.set_xlabel('Median Sale Price (Million $)', fontsize=13, fontweight='bold', labelpad=10)
            ax.set_title(title, fontsize=16, fontweight='bold', pad=12)
            ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'${x:,.1f}M'))
            ax.tick_params(axis='y', labelsize=12, width=0)
            ax.tick_params(axis='x', labelsize=12)
            for spine in ['top', 'right', 'left']:
                ax.spines[spine].set_visible(False)
            ax.grid(axis='x', alpha=0.18, linestyle='--', linewidth=1, zorder=1)
            ax.set_axisbelow(True)
            ax.set_ylim(-0.5, len(neigh_data)-0.5)
            if y_label:
                ax.set_ylabel('Neighborhood', fontweight='bold', fontsize=13, labelpad=8)
            else:
                ax.set_ylabel('')

            handles = [
                plt.Line2D([0], [0], color=ref2019_color, marker=ref_marker_map['2019'], linestyle='', markersize=9, markeredgecolor='black', label='2019'),
                plt.Line2D([0], [0], color=ref2017_color, marker=ref_marker_map['2017'], linestyle='', markersize=9, markeredgecolor='black', label='2017'),
            ]
            ax.legend(handles=handles, loc='best', fontsize=11, title='Reference Years', frameon=True)
            fig.tight_layout()
            return fig

        df_ref = dfc[dfc[year_col_actual].isin([2017, 2019])]
        neighborhoods_top = top.index
        neighborhoods_bottom = bottom.index
        if not df_ref.empty:
            ref_medians = df_ref.groupby([neighborhood_col_actual, year_col_actual])[price_col_actual].median().unstack()
            old2019_top = ref_medians.get(2019, pd.Series(dtype=float)).reindex(neighborhoods_top)
            old2017_top = ref_medians.get(2017, pd.Series(dtype=float)).reindex(neighborhoods_top)
            old2019_bottom = ref_medians.get(2019, pd.Series(dtype=float)).reindex(neighborhoods_bottom)
            old2017_bottom = ref_medians.get(2017, pd.Series(dtype=float)).reindex(neighborhoods_bottom)
        else:
            old2019_top = pd.Series(index=neighborhoods_top, dtype=float)
            old2017_top = pd.Series(index=neighborhoods_top, dtype=float)
            old2019_bottom = pd.Series(index=neighborhoods_bottom, dtype=float)
            old2017_bottom = pd.Series(index=neighborhoods_bottom, dtype=float)

        top_color = sns.color_palette('YlOrRd', 10)[-3]
        bottom_color = sns.color_palette('PuBu', 10)[3]
        ref2017_color = '#955cc6'
        ref2019_color = '#4aac4a'

        fig2 = bar_plot(bottom, '2025: Bottom NYC Neighborhoods by Median Price\n(Markers: 2019 and 2017 values)', old2019_bottom, old2017_bottom, bottom_color, ref2019_color, ref2017_color, y_label=True)
        fig2.tight_layout(rect=[0, 0, 1, 0.96])

        fig1 = bar_plot(top, '2025: Top NYC Neighborhoods by Median Price\n(Markers: 2019 and 2017 values)', old2019_top, old2017_top, top_color, ref2019_color, ref2017_color, y_label=True )
        fig1.tight_layout(rect=[0, 0, 1, 0.96])
        return [fig1, fig2]