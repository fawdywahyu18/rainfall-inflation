"""
Merapikan data Curah Hujan dan IHK tahun dasar 2012
@author: fawdywahyu
"""

import pandas as pd
from datetime import date

# Curah Hujan
df_ch = pd.read_excel('Data/Data Curah Hujan 82 Kabupaten Kota ID BPS.xlsx',
                      sheet_name='Bulanan 2009-2023')
colnames_ch = list(df_ch.columns)
colnames_bulan_ch = colnames_ch[3:]

# Temperature
df_suhu = pd.read_excel('Data/Data Temperature 82 Kabupaten Kota ID BPS.xlsx',
                        sheet_name='Bulanan 2009-2023')
colnames_suhu = list(df_suhu.columns)
colnames_bulan_suhu = colnames_suhu[3:]


def get_month_dates(month_list):
  """
  This function converts a list of integers (1-144) to corresponding date objects 
  representing the start of each month, starting from January 2009.

  Args:
      month_list: A list of integers between 1 and 144.

  Returns:
      A list of date objects representing the start of each month.
  """
  start_date = date(2009, 1, 1)  # Start date (January 1st, 2009)
  month_dates = []
  for month_num in month_list:
    # Calculate the year based on the month number (offset by 1 for 0-based indexing)
    year = start_date.year + (month_num - 1) // 12
    # Calculate the month within the year (1-based indexing)
    month = (month_num - 1) % 12 + 1
    month_dates.append(date(year, month, 1))
  return month_dates

# Example usage on Curah Hujan
month_list_ch = range(1, len(colnames_bulan_ch)+1)  # List of integers from 1 to 144 (inclusive)
month_dates_ch = get_month_dates(month_list_ch)

new_column_names_ch = colnames_ch[:3] + month_dates_ch
df_ch.columns = new_column_names_ch

pd_melt_ch = pd.melt(df_ch, id_vars=['kode_bps', 'kota_low', 'dummy_kota'], value_vars=month_dates_ch,
                     ignore_index=True, value_name='curah_hujan', var_name='bulan')

# Example usage on Temperature
month_list_suhu = range(1, len(colnames_bulan_suhu)+1)  # List of integers from 1 to 144 (inclusive)
month_dates_suhu = get_month_dates(month_list_suhu)

new_column_names_suhu = colnames_suhu[:3] + month_dates_suhu
df_suhu.columns = new_column_names_suhu

pd_melt_suhu = pd.melt(df_suhu, id_vars=['kode_bps', 'kota_low', 'dummy_kota'], value_vars=month_dates_suhu,
                       ignore_index=True, value_name='temperature', var_name='bulan')


# Merge data curah hujan, temperature, dan cpi
ihk = pd.read_excel('Data/Inflasi/Long Format CPI 82 Kab 2014 2023 2012=100.xlsx')
ihk['bulan'] = ihk['bulan'].dt.date
ihk = ihk[['kode_bps', 'kota_low', 'bobot', 'bulan', 'tahun', 'composite', 'food', 'processed_food', 'housing']]

# Hapus Bungo dari data karena Bungo tidak muncul di data setelah 2019
ihk = ihk[ihk['kota_low'] != 'bungo']


pd_melt_merge = pd.merge(pd_melt_ch, pd_melt_suhu[['kode_bps', 'kota_low', 'bulan', 'temperature']],
                         on=['kode_bps', 'kota_low', 'bulan'],
                         how = 'inner')

merge_all = pd.merge(pd_melt_merge, ihk,
                     on=['kode_bps', 'kota_low', 'bulan'],
                     how = 'inner')
len(merge_all[merge_all['tahun']==2023]['kota_low'].unique()) == 81 # Kalau jumlahnya 81, berarti olah datanya benar

# Penentuan awal musim hujan
# Badan Meteorologi Klimatologi dan Geofisika (BMKG) menetapkan awal musim hujan adalah 
# kejadian 3 kali dasarian dengan hujan ≥ 50 mm berurutan.
# 1 dasarian adalah 10 hari, 3 kali dasarian adalah 1 bulan.
# artinya, ketika 1 bulan punya curah hujan >=50 mm, dianggap sebagai awal mulai musim hujan

import numpy as np
merge_all['dummy_rainy'] = np.where(merge_all['curah_hujan']>=50, 1, 0)

# Penentuan musim hujan berdasarkan median curah hujan dalam satu tahun
percentile_50 = merge_all.groupby(['kota_low', 'tahun']).agg({'curah_hujan':'median'}).reset_index()
percentile_50.columns = ['kota_low', 'tahun', 'median_curah_hujan']

# Penentuan musim hujan berdasarkan curah hujan di bawah atau di atas trend
trend_ch = merge_all[['kota_low', 'bulan', 'curah_hujan', 'tahun']]
trend_ch['bulan'] = pd.to_datetime(trend_ch['bulan'])
trend_ch.set_index('bulan', inplace=True)

from statsmodels.tsa.filters.hp_filter import hpfilter

city = trend_ch['kota_low'].unique()

for c in city:
    
    trend_ch_c = trend_ch[trend_ch['kota_low']==c]
    cyclical_c, trend_c = hpfilter(trend_ch_c['curah_hujan'], lamb=14400)
    merge_cy_trend = trend_ch_c.merge(trend_c, left_index=True, right_index=True).merge(cyclical_c, left_index=True, right_index=True)
    merge_cy_trend_reset = merge_cy_trend.reset_index()
    merge_cy_trend_reset['bulan'] = merge_cy_trend_reset['bulan'].dt.date
    
    if c==city[0]:
        df_append = merge_cy_trend_reset
    else:
        df_append = pd.concat([df_append, merge_cy_trend_reset], ignore_index=True)

df_merge_median = pd.merge(merge_all, percentile_50,
                           on=['kota_low', 'tahun'],
                           how='inner')
df_merge_median['dummy_rainy'] = np.where(df_merge_median['curah_hujan']>=df_merge_median['median_curah_hujan'], 1, 0)

result_median = df_merge_median.groupby(['kode_bps', 'kota_low', 'tahun', 'dummy_rainy']).agg({'dummy_kota': 'first',
                                                                                               'bobot': 'first',
                                                                                               'curah_hujan': 'mean',
                                                                                               'temperature': 'mean',
                                                                                               'composite': 'mean',
                                                                                               'food': 'mean',
                                                                                               'processed_food': 'mean',
                                                                                               'housing': 'mean'}).reset_index()

df_merge_trend = pd.merge(merge_all, df_append[['bulan', 'kota_low', 'tahun', 'curah_hujan_cycle', 'curah_hujan_trend']],
                          on=['bulan', 'kota_low', 'tahun'],
                          how='inner')
df_merge_trend['dummy_rainy'] = np.where(df_merge_trend['curah_hujan_cycle']>0, 1, 0)

result_trend = df_merge_trend.groupby(['kode_bps', 'kota_low', 'tahun', 'dummy_rainy']).agg({'dummy_kota': 'first',
                                                                                                   'bobot': 'first',
                                                                                                   'curah_hujan': 'mean',
                                                                                                   'temperature': 'mean',
                                                                                                   'composite': 'mean',
                                                                                                   'food': 'mean',
                                                                                                   'processed_food': 'mean',
                                                                                                   'housing': 'mean'}).reset_index()

def rename_columns(df_input, suffix_input):
    
    columns_to_rename = df_input.columns[6:]
    new_column_names = {col: col + suffix_input for col in columns_to_rename}
    df_renamed = df_input.rename(columns=new_column_names)

    return df_renamed

def export_dataframe(str_input):
    
    # str_input = 'trend'
    
    # str_input: 'median' atau 'trend'
    if str_input=='median':
        result = result_median
    elif str_input=='trend':
        result = result_trend
    else:
        raise ValueError("str_input must be median or trend")
    
    result_low = rename_columns(result[result['dummy_rainy']==0], '_low')
    result_high = rename_columns(result[result['dummy_rainy']==1], '_high')


    result_merge = pd.merge(result_low.drop('dummy_rainy', axis=1),
                            result_high.drop('dummy_rainy', axis=1),
                            on=['kode_bps', 'kota_low', 'tahun', 'dummy_kota', 'bobot'],
                            how='inner')


    result_merge['curah_hujan_diff'] = (result_merge['curah_hujan_high'] - result_merge['curah_hujan_low'])*100 / result_merge['curah_hujan_low'] 
    result_merge['curah_hujan_mean'] = (result_merge['curah_hujan_high'] + result_merge['curah_hujan_low'])/2

    result_merge['temperature_diff'] = (result_merge['temperature_high'] - result_merge['temperature_low'])*100 / result_merge['temperature_low'] 
    result_merge['temperature_mean'] = (result_merge['temperature_high'] + result_merge['temperature_low'])/2

    result_merge['composite_diff'] = (result_merge['composite_high'] - result_merge['composite_low'])*100 / result_merge['composite_low'] 
    result_merge['composite_mean'] = (result_merge['composite_high'] + result_merge['composite_low'])/2

    result_merge['food_diff'] = (result_merge['food_high'] - result_merge['food_low'])*100 / result_merge['food_low'] 
    result_merge['food_mean'] = (result_merge['food_high'] + result_merge['food_low'])/2

    result_merge['processed_food_diff'] = (result_merge['processed_food_high'] - result_merge['processed_food_low'])*100 / result_merge['processed_food_low'] 
    result_merge['processed_food_mean'] = (result_merge['processed_food_high'] + result_merge['processed_food_low'])/2

    result_merge['housing_diff'] = (result_merge['housing_high'] - result_merge['housing_low'])*100 / result_merge['housing_low'] 
    result_merge['housing_mean'] = (result_merge['housing_high'] + result_merge['housing_low'])/2

    result_merge['composite_lag1'] = result_merge.groupby('kode_bps')['composite_mean'].shift(1)
    result_merge['inflasi_t'] = (result_merge['composite_mean'] - result_merge['composite_lag1'])*100 / result_merge['composite_lag1'] 
    result_merge['inflasi_lag1'] = result_merge.groupby('kode_bps')['inflasi_t'].shift(1)
    
    result_merge[['inflasi_t', 'inflasi_lag1']]
    result_merge.to_excel(f'Data/Curah Hujan dan IHK 2012=100 Dummy {str_input} 2014 2023.xlsx', index=False)
    
    return(result_merge)

df_median_result = export_dataframe('median')
df_trend_result = export_dataframe('trend')

