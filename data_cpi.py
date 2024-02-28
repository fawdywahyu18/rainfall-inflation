"""
Merapikan data inflasi 82 Kabupaten/Kota di Indonesia
@author: Fawdy
"""


import pandas as pd

id_bps_82 = pd.read_excel('Data/82 Kota dan ID BPS.xlsx')
data_ihk = pd.read_excel('Data/Inflasi/Kompilasi IHK 2008 2019.xlsx',
                         sheet_name='2008')
colnames = data_ihk.columns

data_ihk_long = pd.melt(data_ihk, id_vars='kota_kab', var_name='tanggal', value_name='cpi')

tahun_list = ['2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019'] 
def compile_ihk(list_tahun):
    # list_tahun: list
    
    for y in list_tahun:
        data_ihk = pd.read_excel('Data/Inflasi/Kompilasi IHK 2008 2019.xlsx',
                                 sheet_name=y)
        data_ihk_long = pd.melt(data_ihk, id_vars='kota_kab', var_name='tanggal', value_name='cpi')
        
        if y==list_tahun[0]:
            data_append = data_ihk_long
        else:
            data_append = pd.concat([data_append, data_ihk_long], axis=0)
    
    return data_append

long_kompilasi = compile_ihk(tahun_list)
long_kompilasi['tanggal_pandas'] = pd.to_datetime(long_kompilasi['tanggal'])
long_kompilasi['tahun'] = long_kompilasi['tanggal_pandas'].dt.year
long_kompilasi['kota_kab'] = long_kompilasi['kota_kab'].str.lower()

df_merge = pd.merge(long_kompilasi, id_bps_82,
                    left_on='kota_kab',
                    right_on='nama_wilayah',
                    how='right')

df_extract = df_merge[['kota_kab', 'kode_bps', 'tahun', 'tanggal_pandas',
                       'cpi']]

df_extract.to_excel('Data/Inflasi/Long Format CPI 82 Kab 2010 2019.xlsx', index=False)
