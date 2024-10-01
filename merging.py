"""
Merging dataframes and analysing the regression 2012=100
@author: fawdywahyu
"""


import pandas as pd
import numpy as np

df_pdrb_adhb = pd.read_excel('Data/PDRB Lapangan Usaha ADHB 2010 2019 82 Kab Kota.xlsx')
df_pdrb_adhk = pd.read_excel('Data/PDRB Lapangan Usaha ADHK 2010 2019 82 Kab Kota.xlsx')

df_pdrb_merge = pd.merge(df_pdrb_adhb, df_pdrb_adhk,
                         on=['kab_kota', 'kode_bps', 'tahun'],
                         suffixes=('_adhb', '_adhk'),
                         how = 'inner')
df_pdrb_merge['deflator_industri'] = df_pdrb_merge['industri_adhb'] / df_pdrb_merge['industri_adhk']
df_pdrb_merge['deflator_pertanian'] = df_pdrb_merge['pertanian_adhb'] / df_pdrb_merge['pertanian_adhk']
df_pdrb_merge['deflator_perdagangan'] = df_pdrb_merge['perdagangan_adhb'] / df_pdrb_merge['perdagangan_adhk']
df_pdrb_merge['deflator_penyediaan_akomodasi'] = df_pdrb_merge['penyediaan_akomodasi_adhb'] / df_pdrb_merge['penyediaan_akomodasi_adhk']

df_pdrb_merge['share_industri'] = df_pdrb_merge['industri_adhk']*100 / df_pdrb_merge['pdrb_total_adhk']
df_pdrb_merge['share_pertanian'] = df_pdrb_merge['pertanian_adhk']*100 / df_pdrb_merge['pdrb_total_adhk']
df_pdrb_merge['share_perdagangan'] = df_pdrb_merge['perdagangan_adhk']*100 / df_pdrb_merge['pdrb_total_adhk']
df_pdrb_merge['share_penyediaan_akomodasi'] = df_pdrb_merge['penyediaan_akomodasi_adhk']*100 / df_pdrb_merge['pdrb_total_adhk']

df_pdrb_merge['log_pdrb'] = np.log(df_pdrb_merge['pdrb_total_adhk'])
df_pdrb_merge.columns

# Menghitung pertumbuhan deflator
# Convert 'Date' column to datetime type
df_pdrb_merge['tahun_datetime'] = pd.to_datetime(df_pdrb_merge['tahun'].astype(str) + '-01-01')

# Sort data by 'kab_kota' and 'tahun'
df_pdrb_merge_sort = df_pdrb_merge.sort_values(by=['kab_kota', 'tahun_datetime'])

# Calculate the percentage change of the deflator for each city
df_pdrb_merge_sort['deflator_industri_growth'] = df_pdrb_merge_sort.groupby('kab_kota')['deflator_industri'].pct_change() *100
df_pdrb_merge_sort['deflator_pertanian_growth'] = df_pdrb_merge_sort.groupby('kab_kota')['deflator_pertanian'].pct_change() *100
df_pdrb_merge_sort['deflator_perdagangan_growth'] = df_pdrb_merge_sort.groupby('kab_kota')['deflator_perdagangan'].pct_change() *100
df_pdrb_merge_sort['deflator_penyediaan_akomodasi_growth'] = df_pdrb_merge_sort.groupby('kab_kota')['deflator_penyediaan_akomodasi'].pct_change() *100

df_pdrb_merge_sort = df_pdrb_merge_sort[['kab_kota', 'kode_bps', 'tahun',
                                         'deflator_industri', 'deflator_pertanian',
                                         'deflator_perdagangan', 'deflator_penyediaan_akomodasi',
                                         'deflator_industri_growth', 'deflator_pertanian_growth',
                                         'deflator_perdagangan_growth', 'deflator_penyediaan_akomodasi_growth',
                                         'share_industri', 'share_pertanian', 'share_perdagangan',
                                         'share_penyediaan_akomodasi', 'log_pdrb']]

# Calculate percentile for each city within each year, based on share of agriculture
df_pdrb_merge_sort['percentile'] = df_pdrb_merge_sort.groupby('tahun')['share_pertanian'].rank(pct=True) * 100

# Create percentile groups
def categorize_percentile(row):
    if row['percentile'] <= 25:
        return 'Q1'
    elif row['percentile'] <= 50:
        return 'Q2'
    elif row['percentile'] <= 75:
        return 'Q3'
    else:
        return 'Q4'

df_pdrb_merge_sort['percentile_group_pertanian'] = df_pdrb_merge_sort.apply(categorize_percentile, axis=1)

def export_df(str_input):
    
    # str_input: 'median' atau 'trend'
    if str_input=='median':
        str_ext = 'Dummy median'
    elif str_input=='trend':
        str_ext = 'Dummy trend'
    else:
        raise ValueError("str_input must be median or trend")
    
    df_ch_ihk = pd.read_excel(f'Data/Curah Hujan dan IHK 2012=100 {str_ext}.xlsx')

    df_merge = pd.merge(df_ch_ihk, df_pdrb_merge_sort,
                        on=['kode_bps', 'tahun'],
                        how='inner')

    df_merge.to_excel(f'Data/panel data long 2012=100 {str_ext}.xlsx', index=False)

    # Define custom aggregation functions
    agg_functions = {
        'kota_low': 'first',
        'dummy_kota': 'first',
        'bobot': 'first',
        
        'curah_hujan_low': 'mean',
        'curah_hujan_high': 'mean',
        'curah_hujan_diff': 'mean',
        
        'temperature_low': 'mean',
        'temperature_high': 'mean',
        'temperature_diff': 'mean',
        
        'composite_low': 'mean',
        'composite_high': 'mean',
        'composite_diff': 'mean',
        
        'food_low': 'mean',
        'food_high': 'mean',
        'food_diff': 'mean',
        
        'processed_food_low': 'mean',
        'processed_food_high': 'mean',
        'processed_food_diff': 'mean',
        
        'housing_low': 'mean',
        'housing_high': 'mean',
        'housing_diff': 'mean',
        
        'clothing_low': 'mean',
        'clothing_high': 'mean',
        'clothing_diff': 'mean',
        
        'health_low': 'mean',
        'health_high': 'mean',
        'health_diff': 'mean',
        
        'education_recreation_sport_low': 'mean',
        'education_recreation_sport_high': 'mean',
        'education_recreation_sport_diff': 'mean',
        
        'transportation_communication_finance_low': 'mean',
        'transportation_communication_finance_high': 'mean',
        'transportation_communication_finance_diff': 'mean',
        
        'deflator_industri': 'mean',
        'deflator_pertanian': 'mean',
        'deflator_perdagangan': 'mean',
        'deflator_penyediaan_akomodasi': 'mean',
        
        'deflator_industri_growth': 'mean',
        'deflator_pertanian_growth': 'mean',
        'deflator_perdagangan_growth': 'mean',
        'deflator_penyediaan_akomodasi_growth': 'mean',
        
        'share_industri': 'mean',
        'share_pertanian': 'mean',
        'share_perdagangan': 'mean',
        'share_penyediaan_akomodasi': 'mean',
        'log_pdrb': 'mean'
    }


    df_gb = df_merge.groupby('kode_bps').agg(agg_functions)
    df_gb.to_excel(f'Data/cross section data 2012=100 {str_ext}.xlsx', index=False)
    
    dict_result = {
        'df_gb': df_gb,
        'df_merge': df_merge}
    
    return(dict_result)

median_export = export_df('median')
trend_export = export_df('trend')








